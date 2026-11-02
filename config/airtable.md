# Airtable sync (optional)

status: not configured
base_id:
table_id:

`tracker/tracker.csv` is always the local source of truth. When Airtable is configured (an Airtable MCP connector in Claude Code, plus the IDs above), every tracker change is mirrored to it, matching records on the ID field. Set `status: configured` once the base exists.

## Setup
1. Connect the Airtable connector in Claude Code.
2. Ask Claude: "create an Airtable base for the tracker using config/airtable.md". It creates the table with the schema below and fills in `base_id` and `table_id`.
3. Ask for a first sync: every row of tracker.csv is upserted.

## Schema (table "Applications")
| Field | Type |
|---|---|
| ID | single line text (primary): same as tracker.csv `id` |
| Company | single line text |
| Role | single line text |
| Location | single select (one option per city in config/search.md, plus Remote, Other) |
| Role type | single select (Graduate programme, Entry-level, Internship, Part-time) |
| URL | url |
| Source | single select (ats, inbox, board, web, manual, alert-email) |
| Date found | date |
| Deadline | date |
| Fit score | number |
| Status | single select (found, analysed, approved, drafted, final, applied, interview, offer, rejected, withdrawn, skipped) |
| Folder | single line text |
| Applied date | date |
| Next action | single line text |
| Next action date | date |
| Contacts | long text |
| Notes | long text |

## Rules
- Upsert on the ID field and copy IDs from tracker.csv. A retyped ID creates a duplicate record.
- Before overwriting a record's Notes, compare them with the CSV; the user may have added facts in Airtable.
- On conflicts, tracker.csv wins unless the user edited the Airtable record more recently; then ask.
