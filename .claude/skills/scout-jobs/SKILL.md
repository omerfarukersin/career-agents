---
name: scout-jobs
description: Run a job-search sweep - scout all sources for new roles matching config/search.md, analyse every new job in parallel, and present a ranked digest for the user to choose which to tailor. Use for "find jobs", "scout", "anything new?", or the scheduled 2-3 day run.
argument-hint: [optional focus, e.g. "consulting only" or "deadlines this month"]
---

> Whenever a subagent returns ```file:<path>``` blocks (it was blocked from writing), save each block verbatim to that path before continuing.

# /scout-jobs

Focus (optional): $ARGUMENTS

1. Launch **job-scout** in scout mode (pass the focus, if any).
2. For every new folder it created, launch **job-analyst** — in parallel, batches of up to 6.
3. Present a digest sorted by fit score (descending), deadline as a tiebreaker:

   | Fit | Company | Role | City | Deadline | Top gap | Folder |

   Put anything with a deadline within 14 days at the top under **URGENT**.
   Below the table: jobs under threshold in one line each, and a count of rejected postings.
4. Ask which jobs to tailor (multi-select). For each chosen job run the `/add-job` flow starting from step 3 (checkpoint already satisfied by their choice) — the build steps of different jobs can run in parallel.
5. If running unattended (scheduled run with no user), stop after step 3, write the digest to `tracker/digest_<YYYY-MM-DD>.md`, and send a push notification if available: "N new jobs, top: <Company> <Role> (<fit>)".

Also report follow-ups due today from `tracker/tracker.csv` (`next_action_date` ≤ today).
