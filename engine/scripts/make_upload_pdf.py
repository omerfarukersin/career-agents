#!/usr/bin/env python3
"""Make an upload-safe copy of a PDF: no links, no open actions, no scripts.

Some applicant tracking systems (e.g. SAP SuccessFactors) reject PDFs with
"active content". pdfTeX + hyperref adds link annotations and an /OpenAction,
which is enough to trigger that. The text is unchanged: URLs stay visible.

Usage: make_upload_pdf.py <in.pdf> [out.pdf]
Default output: <in>_upload.pdf next to the input.
"""
import os, sys
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject

ACTIVE_ROOT_KEYS = ['/OpenAction', '/AA', '/Names', '/AcroForm', '/JavaScript']

src = sys.argv[1]
dst = sys.argv[2] if len(sys.argv) > 2 else src[:-4] + '_upload.pdf'

reader = PdfReader(src)
writer = PdfWriter()
for page in reader.pages:
    for key in ('/Annots', '/AA'):
        if key in page:
            del page[NameObject(key)]
    writer.add_page(page)
for key in ACTIVE_ROOT_KEYS:
    if key in writer._root_object:
        del writer._root_object[NameObject(key)]
writer.add_metadata({'/Title': 'Cover Letter' if 'letter' in os.path.basename(src).lower() else 'Curriculum Vitae'})
with open(dst, 'wb') as f:
    writer.write(f)

# verify
check = PdfReader(dst)
bad = [k for k in ACTIVE_ROOT_KEYS if k in check.trailer['/Root']]
bad += [f'page {i} {k}' for i, p in enumerate(check.pages) for k in ('/Annots', '/AA') if k in p]
print(('OK: ' if not bad else 'STILL ACTIVE ' + str(bad) + ': ') + dst)
