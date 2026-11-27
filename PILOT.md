# Pilot

Run once after setup. Every candidate makes a submission and reviews the
others. The results score the baseline and pick the builder and judges.

1. List at least four candidates in `MODELS.md`.
2. One at a time, start a fresh session with each candidate and paste, with its
   name from `MODELS.md`:

   ```text
   /goal Read goal.md. Create pilot/<name> from main and make your best attempt
   at the goal. Commit it without naming your model in the project, then finish.
   ```

3. In a fresh session with any model, paste:

   ```text
   /goal Read LOOP.md. Each candidate in MODELS.md reviews main and every
   pilot/ branch but its own. Build a folder .loop/judge/<n>/ for each review
   as in the review handoff, list n, judge, and branch in .loop/pilot.tsv,
   then finish.
   ```

4. Run each folder's judge from `.loop/pilot.tsv`, as in START.md step 2.
5. Back in that session, paste:

   ```text
   /goal Add each score to .loop/pilot.tsv and rank the submissions by mean
   score. In MODELS.md, make the top model the builder and the next three the
   judges. Record main as the baseline and the top submission as a trial, both
   scored by the judges' mean. Merge the trial if it gains 1.0 and archive
   every unmerged submission.
   ```

Then continue with START.md step 1.
