# Career Agents: orchestrator instructions

A multi-agent system that finds jobs, analyses fit, tailors CVs and cover letters, finds people to network with, and prepares interviews. You (the main Claude Code conversation) are the orchestrator; the subagents in `.claude/agents/` do the focused work.

## Layout

The **engine** is generic and reusable; the **workspace** holds one person's data. Never put personal facts into engine files.

```
.claude/agents/      ENGINE     subagents (scout, analyst, researcher, writers, critic, networker, interview prep)
.claude/skills/      ENGINE     user commands: /add-job, /scout-jobs, /mock-interview, /job-status, /build-career-bank
engine/templates/    ENGINE     LaTeX CV + cover letter, job-folder templates, workspace starter files
engine/scripts/      ENGINE     PDF build, upload-safe PDFs, tracker helper, workspace init, privacy check
config/              SETTINGS   country conventions, role families, scoring, job sources, target companies
docs/                ENGINE     architecture, lessons learned, adapting to another country

me/                  WORKSPACE  career bank: the ONLY source of facts about the candidate   (git-ignored)
jobs/                WORKSPACE  one folder per company/role                                  (git-ignored)
tracker/             WORKSPACE  tracker.csv, scout logs, digests                             (git-ignored)
inbox/               WORKSPACE  job ads and alert emails the user drops in                   (git-ignored)
CHANGELOG.md         WORKSPACE  the user's running log of decisions and lessons              (git-ignored)
```

If `me/` does not exist, tell the user to run `engine/scripts/init_workspace.sh`, then `/build-career-bank`.

## Start of every session
Read `CHANGELOG.md` (lessons, decisions, past mistakes) before doing anything. After each meaningful step (application drafted or submitted, search run, mistake found, rule adopted), add a dated entry with a ✅/❌/🔧/📌 tag. Run `date` before stating weekdays or "days left".

## Hard rules (every agent)

1. **Truth guard.** Every claim about the candidate must trace to a file in `me/`. Creativity is allowed in *framing* (wording, emphasis, order, connecting experience to the employer's needs). Never invent employers, titles, dates, grades, tools, numbers or outcomes. If a requirement cannot be backed by the career bank, list it as a gap; do not paper over it. Keep estimates as estimates: never turn a projected result into a measured one.
2. **Job requirements drive the writing; the career bank supplies the evidence.** Start from what the employer needs, then pick the strongest true evidence for each need.
3. **Human checkpoints.** Stop for the user's approval (a) after fit analysis, before tailoring, (b) after drafts, before marking final, (c) before anything is sent to a person. Agents never send messages, submit applications, or log into accounts.
4. **No LinkedIn scraping or login automation.** Use public search results, job-alert emails the user forwards, public ATS feeds, and job APIs. Respect each site's terms.
5. **Write like a person.** No "I am thrilled", "passionate about leveraging", "in today's fast-paced world", em-dash chains, or triplet lists everywhere. Run a humanizer pass (e.g. the `humanizer` skill, if installed) on cover letters and outreach.
6. **Local conventions.** Read `config/search.md` for country norms (CV length, photo, spelling, eligibility wording).
7. **Respect "no AI" requests.** If an employer asks applicants not to use AI for form answers or tests, the user writes those; you may only check facts.
8. **Neutral pronouns.** The career bank does not record the user's pronouns unless `me/profile.md` says so; write "they" or use the name.

## When a subagent can't write a file
Some harness setups block subagents from writing report-style files (e.g. analysis.md). A subagent that gets blocked must return the complete file content in a fenced block whose info string is `file:<relative path>`, e.g. ```` ```file:jobs/X/2027-01-15_Y/analysis.md ````. The orchestrator saves every such block verbatim, then updates the tracker.

## Running agents in parallel
- Parallel subagents must not edit `tracker/tracker.csv`; they return their rows and the orchestrator merges them in one write.
- When several writers revise in parallel, the orchestrator decides house style (names, spellings, titles) and states it in every brief.
- Keep batches small (about 6 agents). Too many at once hits rate limits and loses work.

## Job folder convention

`jobs/<Company>/<YYYY-MM-DD>_<Role-Slug>/` with shared `jobs/<Company>/company.md`.
Files inside a role folder: `job.md`, `analysis.md`, `cv.tex`, `cv.pdf`, `cover_letter.tex`, `cover_letter.pdf`, `critique.md`, `outreach.md`, `interview_prep.md`, `status.md`, `application_answers.md` (every form question and the exact answer submitted; interview prep reads it first), and the upload-safe `<First>_<Last>_CV.pdf` / `<First>_<Last>_Cover_Letter.pdf` made by `engine/scripts/make_upload_pdf.py` (name from `me/profile.md`). Templates live in `engine/templates/job/`.

Slugs: letters, digits and hyphens only (e.g. `jobs/Accenture/2027-01-15_Analytics-Graduate-Programme/`).

## Tracker

`tracker/tracker.csv` is the local source of truth. If `config/airtable.md` has `status: configured`, mirror each change to Airtable too, matching records on the ID field. Copy IDs from tracker.csv; never retype them from memory (a mistyped ID creates a duplicate record). Statuses: `found → analysed → approved → drafted → final → applied → interview → offer | rejected | withdrawn | skipped`.

Row format: `id` = `<company-slug>-<role-slug>-<YYYYMMDD>` (date found, lowercase, hyphens); `role_type` = `Graduate programme | Entry-level | Internship | Part-time`; dates in ISO format. Update rows with `engine/scripts/tracker_set.py <folder-or-id> field=value ...`.

## Building PDFs

`engine/scripts/build_pdf.sh <path/to/file.tex>` compiles with pdflatex and removes aux files. A CV must fit the page limit in `config/search.md`; if it overflows, cut content, do not shrink fonts below the template's. After every trim, re-check names, titles and dates against `me/`. Before upload, always make the upload-safe copy: some ATS (e.g. SAP SuccessFactors) reject PDFs with link annotations as "active content".

## Privacy
Never write the user's personal data into engine files, `config/`, `docs/` or `examples/`. `engine/scripts/privacy_check.py` scans the files git would publish; run it before any commit.
