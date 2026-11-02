#!/usr/bin/env bash
# Create the personal workspace (me/, tracker/, inbox/, jobs/, CHANGELOG.md) from the starter templates.
# Never overwrites an existing file. Installs the privacy pre-commit hook if this is a git repo.
# Usage: engine/scripts/init_workspace.sh
set -euo pipefail
root="$(cd "$(dirname "$0")/../.." && pwd)"
tpl="$root/engine/templates/workspace"
cd "$root"

created=0
while IFS= read -r -d '' src; do
  rel="${src#$tpl/}"
  if [ ! -e "$rel" ]; then
    mkdir -p "$(dirname "$rel")"
    cp "$src" "$rel"
    echo "created  $rel"
    created=$((created + 1))
  fi
done < <(find "$tpl" -type f -print0)
mkdir -p jobs inbox/processed

if [ ! -e .privacy-terms ]; then
  cat > .privacy-terms <<'EOF'
# Words that must never appear in files git would publish: your name, phone, email,
# handles, ID numbers, addresses. One per line, case-insensitive. This file is git-ignored.
# Contact details from me/profile.md are added automatically when they are filled in.
# A line starting with ! skips a file or folder for these terms (generic checks still run),
# e.g. !LICENSE if your name is in the licence on purpose.
!examples/demo/
EOF
  echo "created  .privacy-terms"
fi

if [ -d .git ]; then
  hook=.git/hooks/pre-commit
  if [ ! -e "$hook" ]; then
    printf '#!/usr/bin/env bash\nexec python3 engine/scripts/privacy_check.py\n' > "$hook"
    chmod +x "$hook"
    echo "installed privacy pre-commit hook"
  fi
else
  echo "note: not a git repo, so the privacy pre-commit hook was not installed; re-run this script after 'git init'"
fi

echo "Done: $created file(s) created. Next: put your CV in me/cv_original/, open Claude Code here and run /build-career-bank."
