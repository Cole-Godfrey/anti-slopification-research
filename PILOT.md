# Pilot

Run once after setup. Each candidate makes a submission, then judges all the
others in one session. The results pick the builder and judges. Sessions in the
same step can run in parallel.

1. List at least four candidates in `MODELS.md`.
2. Start a fresh session with each candidate and paste, with its name from
   `MODELS.md`:

   ```text
   /goal Read goal.md. Make your best attempt at the goal on a new branch,
   pilot/<name>, in its own worktree at .loop/pilot/<name>. Commit it without
   naming your model in the project, then finish.
   ```

3. In a fresh session with any model, paste:

   ```text
   /goal Read LOOP.md. For each candidate in MODELS.md, build a judge folder
   .loop/judge/<name>/ as in the review handoff, holding every other pilot/
   branch in projects/<label>/ in random order. List each judge, label, and
   branch in .loop/pilot.tsv, then finish.
   ```

4. Start each candidate in its judge folder, as in START.md step 2.
5. Back in that session, paste:

   ```text
   /goal Remove the pilot worktrees. Add the scores to .loop/pilot.tsv and rank
   the submissions by mean score. In MODELS.md, make the top model the builder
   and the next three the judges. Record the top submission as a trial scored by
   the judges' mean and merge it if it gains 1.0. Archive every unmerged
   submission.
   ```

Then continue with START.md step 1.
