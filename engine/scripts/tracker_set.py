#!/usr/bin/env python3
"""Update fields of tracker rows by folder or id.
Usage: tracker_set.py <folder-or-id> field=value [field=value ...]
Writes to a temporary file and replaces tracker.csv only on success, so a crash never truncates it."""
import csv, os, sys
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tracker', 'tracker.csv')
key, pairs = sys.argv[1].rstrip('/'), dict(a.split('=', 1) for a in sys.argv[2:])
with open(path, newline='') as f:
    reader = csv.DictReader(f)
    fields, rows = reader.fieldnames, list(reader)
unknown = [k for k in pairs if k not in fields]
if unknown:
    sys.exit(f"unknown field(s): {', '.join(unknown)}. Valid: {', '.join(fields)}")
broken = [r['id'] for r in rows if None in r]
if broken:
    sys.exit(f"rows with more cells than the header (fix the quoting first): {', '.join(broken)}")
hit = [r for r in rows if r['id'] == key or r['folder'].rstrip('/') == key]
if not hit:
    sys.exit(f'no row for {key}')
for r in hit:
    r.update(pairs)
tmp = path + '.tmp'
with open(tmp, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader(); w.writerows(rows)
os.replace(tmp, path)
print(f"updated {len(hit)} row(s): {key}")
