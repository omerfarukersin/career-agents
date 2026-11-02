#!/usr/bin/env python3
"""Scan the files git would publish for personal data. Exit 1 if anything is found.

Checks:
  1. Terms from .privacy-terms (git-ignored), plus the contact details filled in me/profile.md.
     A line "!path" in .privacy-terms skips term matching for that file or folder (e.g. "!LICENSE"
     for your own name); the generic pattern checks still run there.
  2. Generic patterns: real-looking email addresses, phone numbers, Airtable IDs.
  3. Text inside committed PDFs (needs pypdf).

Usage: privacy_check.py [--all]   (--all also scans git-ignored files, to test the scanner)
Runs as a pre-commit hook after engine/scripts/init_workspace.sh.
"""
import os, re, subprocess, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
# Top-level workspace paths, git-ignored (see .gitignore)
IGNORED_DIRS = {'me', 'jobs', 'tracker', 'inbox'}
IGNORED_FILES = {'CHANGELOG.md', '.privacy-terms'}

PATTERNS = {
    'email': re.compile(r'[\w.+-]+@[\w-]+\.[\w.-]+'),
    'phone': re.compile(r'\+\d{1,3}[ -]?\(?\d{1,4}\)?[ -]?\d{3}[ -]?\d{3,4}'),
    'airtable id': re.compile(r'\b(?:app|tbl|rec|fld|viw)[A-Za-z0-9]{14}\b'),
}
SAFE_EMAIL = re.compile(r'@(example\.(com|org|net)|anthropic\.com|users\.noreply\.github\.com)$', re.I)


def placeholder(s):
    """True for values like +353 00 000 0000, +00 00 000 0000 or appXXXXXXXXXXXXXX."""
    groups = re.findall(r'\d+', s)
    if s.startswith('+') and len(groups) > 1 and all(set(g) == {'0'} for g in groups[1:]):
        return True
    body = re.sub(r'[^A-Za-z0-9]', '', s)
    for prefix in ('app', 'tbl', 'rec', 'fld', 'viw'):
        if body.startswith(prefix) and len(body) == 17:
            body = body[3:]
    return len(set(body.lstrip('+'))) <= 1


def files_to_scan(scan_all):
    os.chdir(ROOT)
    if not scan_all and os.path.isdir('.git'):
        out = subprocess.run(['git', 'ls-files', '--cached', '--others', '--exclude-standard', '-z'],
                             capture_output=True, text=True, check=True).stdout
        return [f for f in out.split('\0') if f]
    found = []
    for d, dirs, names in os.walk('.'):
        top = d == '.'
        dirs[:] = [x for x in dirs if x != '.git' and (scan_all or not top or x not in IGNORED_DIRS)]
        found += [os.path.relpath(os.path.join(d, n)) for n in names
                  if scan_all or not top or n not in IGNORED_FILES]
    return found


def load_terms():
    terms, skip = set(), set()
    if os.path.exists('.privacy-terms'):
        for line in open('.privacy-terms', encoding='utf-8'):
            line = line.strip()
            if line.startswith('!'):
                skip.add(line[1:].strip())
            elif line and not line.startswith('#'):
                terms.add(line.lower())
    if os.path.exists('me/profile.md'):
        text = open('me/profile.md', encoding='utf-8').read()
        for field in ('Name', 'Phone', 'Email', 'LinkedIn', 'GitHub / portfolio'):
            m = re.search(rf'^- {re.escape(field)}:\s*(.+)$', text, re.M)
            value = m.group(1).strip() if m else ''
            if (value and 'TODO' not in value and len(value) > 3 and 'example' not in value.lower()
                    and not placeholder(value)):
                terms.add(value.lower())
    return terms, skip


def read_text(path):
    if path.lower().endswith('.pdf'):
        try:
            from pypdf import PdfReader
            reader = PdfReader(path)
            meta = ' '.join(str(v) for v in (reader.metadata or {}).values())
            return meta + '\n' + '\n'.join(p.extract_text() or '' for p in reader.pages)
        except Exception as e:  # unreadable PDF: report rather than pass silently
            return f'[could not read PDF: {e}]'
    try:
        return open(path, encoding='utf-8').read()
    except (UnicodeDecodeError, IsADirectoryError):
        return ''


def main():
    scan_all = '--all' in sys.argv
    terms, skip = load_terms()
    problems = []
    for path in files_to_scan(scan_all):
        text = read_text(path)
        low = text.lower()
        skipped = any(path == s or path.startswith(s.rstrip('/') + '/') for s in skip)
        problems += [(path, 'term', t) for t in ([] if skipped else terms)
                     if re.search(r'(?<!\w)' + re.escape(t) + r'(?!\w)', low)]
        for name, rx in PATTERNS.items():
            for m in rx.finditer(text):
                hit = m.group(0)
                if name == 'email' and SAFE_EMAIL.search(hit):
                    continue
                if placeholder(hit):
                    continue
                problems.append((path, name, hit))
        if text.startswith('[could not read PDF'):
            problems.append((path, 'pdf', text))
    if problems:
        print('PRIVACY CHECK FAILED: personal data may be published')
        for path, kind, hit in problems:
            print(f'  {path}: {kind}: {hit}')
        print('Fix the files, or (for a false positive) adjust engine/scripts/privacy_check.py.')
        sys.exit(1)
    print(f'Privacy check passed ({len(terms)} personal terms checked).')


if __name__ == '__main__':
    main()
