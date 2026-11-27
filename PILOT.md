# Pilot

Run once after setup. Each candidate makes a submission, then judges all the
others in one session. The results pick the builder and judges. Sessions in the
same step can run in parallel.

1. List at least four candidates in `MODELS.md` and leave `Alias` blank.
2. Start a fresh session with each candidate and paste:

   ```text
   /goal Read goal.md and MODELS.md. Find your row in MODELS.md, pick a short
   unique lowercase alias (no model or harness name), and write it into only
   your row's Alias column. Make your best attempt at the goal on a new branch,
   pilot/<alias>, in its own worktree at .loop/pilot/<alias>. Commit it without
   naming your model or harness in the project, then finish.
   ```

3. In a fresh session with any model, paste:

   ```text
   /goal Read LOOP.md and MODELS.md. For each alias in MODELS.md, build a judge
   folder .loop/judge/<alias>/ as in the review handoff, holding every other
   pilot/ branch in projects/<label>/ in random order. List each judge alias,
   label, and branch in .loop/pilot.tsv, then finish.
   ```

4. Start each candidate in `.loop/judge/<alias>/` using its alias from
   `MODELS.md`, as in `START.md` step 2.
5. Back in the step 3 session, paste:

   ```text
   /goal Remove the pilot worktrees. Add the scores to .loop/pilot.tsv and rank
   the submissions by mean score. In MODELS.md, set Builder to the top alias
   and Judges to the next three aliases. Record the top submission as a trial
   scored by the judges' mean and merge it if it gains 1.0. Archive every
   unmerged submission.
   ```

Then continue with `START.md` step 1.
