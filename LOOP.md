# Goal loop

## Setup

Inspect the project, then interview the user about the goal. Ask questions until the intended result is clear.

Write a short `goal.md` with the objective, required outcomes, and essential
constraints. Leave implementation choices open.

Initialize Git if needed. Establish the project as the baseline on `main` without
discarding user work. Commit the initial project. Keep `goal.md` out of Git.
Create `.loop/` and `.loop/results.tsv` with this tab-separated header:

```text
series	experiment	branch	revision	score	status	description
```

Record a `baseline` row for the `main` commit with score 0.0 and end the setup
session.

## Start an attempt

In a fresh builder session:

1. Read `goal.md`, the current `main` commit, and its recorded baseline score.
   The latest `baseline` or `merge` row identifies that baseline. Check the
   history for relevant failed approaches and inspect their archives when useful.
2. Create `try/001-description` from `main`, using the next unused attempt number.
3. Choose and implement an improvement. You decide the approach and scope.
4. Commit the initial attempt and write a candidate review request.
5. Report REVIEW_READY and end the turn. Leave the commit unchanged for review.

## Respond to a review

Continue in the same builder session for this branch. Read the completed review
for the requested commit and choose one action:

- Merge: allowed only when the candidate's score is at least **1.0 higher** than
  the recorded score of the current baseline. Switch to `main`, fast-forward it
  to the reviewed commit, record a `merge` row, and delete the working branch.
  That commit and score become the new baseline. Report MERGED and end the session.
- Abandon: archive the attempt as described below, record an `abandon` row, return
  to `main`, and delete the working branch. Report ABANDONED and end the session.
- Revise: use the findings to improve this branch, commit the changes, and request
  another review. Report REVIEW_READY and end the turn. Keep using this builder
  session while the attempt continues.

Keep reviewed commits in the attempt's history. A low score can lead to another
revision on the same branch. If `main` changes during an attempt, update the
attempt and obtain a new baseline score and review before deciding to merge.

After a merge or abandonment, the user starts a fresh builder session from `main`.

A review score **above 90.0** completes the project. Finalize that reviewed commit
and report COMPLETE with its branch, commit, and score. Merge it first if it meets
the 1.0-point gain rule; otherwise leave it available on its branch.

Run `python3 plot.py` after recording a review, merge, or abandonment. Keep the
goal fixed within a scoring series. A changed goal or judge model starts a new
series and baseline review.

## Archive

Before abandoning an attempt, commit its remaining work. Create an annotated tag
at the branch tip, replacing `try/` with `archive/`. Include a short note with:

- Starting baseline commit and score.
- Best reviewed commit and score, if reviewed.
- What was tried and why the approach was abandoned.

Then switch to `main` and delete the working branch. For example:

```sh
git tag -a archive/001-description try/001-description -m "attempt summary"
git switch main
git branch -D try/001-description
```

The tag preserves the branch history. Browse it with:

```sh
git tag -l 'archive/*'
git show archive/001-description
```

## Judge

Each judge in `MODELS.md` works blind in `.loop/judge/<n>/` and follows
`JUDGE.md`. A review's score is the mean of theirs. Judges see only `goal.md`
and the snapshot, so keep comments and docs about reviews out of the project.

## Score history

Record each review in `.loop/results.tsv`. Increment `experiment` for each review,
starting at 0 for the baseline. Keep the same series ID until the goal or judge
model changes. Use the attempt branch name for its rows and `main` for a baseline.

Use these statuses:

- `baseline`: a review establishing the score of `main`.
- `trial`: a reviewed commit on an attempt branch.
- `merge`: promotion of a reviewed commit to `main`.
- `abandon`: an attempt archived without merging.

The builder appends all rows and records each review before acting on it.
Merge and abandon rows reuse the latest review number. For a merge, record the
promoted commit's judged score. For an abandonment, record the tip's score if that
commit was reviewed; otherwise leave score empty. Mention the archive tag and
reason in the description. Keep descriptions short, without tabs or newlines.
Append complete newline-ended rows. The graph uses the latest scoring series.

## Review handoff

Overwrite `.loop/review.json` for each request, with these fields:

```text
kind: baseline or candidate
branch: main or the attempt branch
revision: exact commit to judge
```

Then rebuild the judges' folders:

```sh
rm -rf .loop/judge
for n in 1 2 3; do  # one folder per judge in MODELS.md
  mkdir -p .loop/judge/$n/projects/a
  git archive <revision> | tar -x -C .loop/judge/$n/projects/a
  cp goal.md JUDGE.md .loop/judge/$n/
  git init -q .loop/judge/$n  # hides project history from the judge
done
```

Keep one outstanding request at a time. `.loop/review.json` holds the current
request, `.loop/judge/*/result.json` its review, `.loop/results.tsv` the history,
and `.loop/progress.svg` the graph. Archived code and attempt notes live in Git
tags.
