#!/usr/bin/env python3
"""Update fields of tracker rows by folder or id.
Usage: tracker_set.py <folder-or-id> field=value [field=value ...]"""
import csv, os, sys
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tracker', 'tracker.csv')
key, pairs = sys.argv[1].rstrip('/'), dict(a.split('=', 1) for a in sys.argv[2:])
with open(path, newline='') as f:
    reader = csv.DictReader(f)
    fields, rows = reader.fieldnames, list(reader)
unknown = [k for k in pairs if k not in fields]
if unknown:
    sys.exit(f"unknown field(s): {', '.join(unknown)}. Valid: {', '.join(fields)}")
hit = [r for r in rows if r['id'] == key or r['folder'].rstrip('/') == key]
if not hit:
    sys.exit(f'no row for {key}')
for r in hit:
    r.update(pairs)
with open(path, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader(); w.writerows(rows)
print(f"updated {len(hit)} row(s): {key}")
