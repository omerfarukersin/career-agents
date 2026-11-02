# Lessons learned

This system was built and used for a real graduate job search: 180+ postings tracked, dozens of tailored applications, online tests and interviews. These are the lessons from that run that changed the design. Most are now rules in the agent files.

## Truth and quality
- **Estimates drift into results.** A writer presented a projected saving from a model as if it were the measured result of the project. The critic now flags any estimate written as a measured result.
- **Trimming introduces errors.** Cutting a CV to one page brought back a wrong job title that had been fixed earlier. Rule: after every trim, re-check titles, names and dates against the career bank.
- **Don't tailor from the old CV.** An early CV built before the career bank was finished carried skills the user had since ruled out. Finish the career bank first.
- **Check every date against a transcript.** Dates in questionnaire answers can be wrong; compare them with transcripts or contracts.
- **"Never list" lists matter.** Users touch tools they can't defend in an interview. A per-user "never list" in `me/profile.md` is respected by the analyst, the writers and the critic.
- **Don't promise a start date.** A letter promised a start date that the candidate's work rights didn't yet guarantee. Availability now uses the exact wording in the profile.

## Applications and employers
- **Postings close before their deadline.** Several top-fit roles were pulled days early. Apply to top fits in the first week, and re-check liveness before every application day.
- **Aggregators lag employer systems.** A job board showed no deadline for programmes that had already closed on the employer's own ATS. Always open the employer link.
- **Application limits are real.** Some employers accept one application per cycle, or only count the first role applied for. The analyst now looks for this before you choose a role.
- **Eligibility wording screens people out.** Clauses such as "permanent right to work" or graduation-date windows can screen candidates out automatically, so the analyst quotes them and checks them against the profile.
- **Some ATS reject PDFs with links.** SAP SuccessFactors rejected a CV as "active content" because hyperref adds link annotations and an open action. `make_upload_pdf.py` strips them; always upload that copy.
- **Respect "no AI" requests.** Some employers ask candidates not to use AI for application answers or tests. The user writes those; the system only checks facts.
- **The bottleneck is drafting, not finding.** At one point 22 analysed jobs closing within two weeks had no drafts. Before any new search, check that every analysed job with a near deadline has a draft.

## Running many agents
- **Save as you go.** Scouts that collected results in memory were cut off after 10 minutes with nothing saved. Scouts now write each job folder immediately and keep a run log.
- **Too many agents at once hits rate limits.** Twelve parallel agents lost several analyses. Batches of about six, with compact outputs, work reliably.
- **One writer for shared files.** Parallel scouts editing the same CSV caused conflicts; now they return rows and the orchestrator merges them.
- **Parallel writers need one house style.** Two writers revised the same name in opposite directions at the same time. The orchestrator now fixes house style in every brief.
- **Subagents may be blocked from writing.** The ```` ```file:<path> ```` fallback came from this.
- **Copy IDs, don't retype them.** A retyped tracker ID created a duplicate Airtable record. IDs are always copied from the CSV.
- **Check the weekday.** Deadlines were once listed with the wrong weekday. The orchestrator runs `date` before stating weekdays.
- **Retry official pages before doubting the user.** An official page returned 403 and the system labelled a correct user claim "unconfirmed". Retrying with browser headers loaded it.
