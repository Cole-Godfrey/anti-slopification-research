# Goal loop

## Setup

Inspect the project, then interview the user about the goal. Clarify who it is
for, the problem, required outcomes, scope, and constraints. Ask a few questions
at a time and follow up until the intended result is clear.

Write a short `goal.md` with the agreed objective, required outcomes, and essential
constraints. Leave implementation choices open.

Initialize Git if needed. Establish the project as the baseline on `main` without
discarding user work. Commit the initial project. Keep `goal.md` out of Git.
Create `.loop/` and `.loop/results.tsv` with this tab-separated header:

```text
series	experiment	branch	revision	score	status	description
```

Write a baseline review request for the `main` commit and end the setup session.
The judge scores it before the first attempt starts.

## Start an attempt

In a fresh builder session:

1. If `.loop/review.json` holds a judged baseline that isn't logged, log it.
   Read `goal.md`, the current `main` commit, and its recorded baseline score.
   The latest `baseline` or `merge` row identifies that baseline. Check the
   history for relevant failed approaches and inspect their archives when useful.
2. Create `try/001-description` from `main`, using the next unused attempt number.
3. Choose and implement an improvement. You decide the approach and scope.
4. Commit the initial attempt and write a candidate review request.
5. Report REVIEW_READY and end the turn. Leave the commit unchanged for review.

## Respond to a review

Continue in the same builder session for this branch. Log the completed review,
read it, and choose one action:

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

A judge score **above 90.0** completes the project. Finalize that reviewed commit
and report COMPLETE with its branch, commit, and score. Merge it first if it meets
the 1.0-point gain rule; otherwise leave it available on its branch.

Run `python3 plot.py` after logging a review or recording a merge or abandonment.
Keep the goal fixed within a scoring series. A changed goal or judge model starts
a new series and baseline review.

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

The judge is blind. It runs in a fresh session in `.loop/judge/` and follows
`JUDGE.md`. With Claude Code, start it with `--safe-mode`, which keeps CLAUDE.md
files, skills, plugins, hooks, and MCP servers out of its context. It sees
`goal.md` and a snapshot of the requested commit, and nothing else: no LOOP.md,
score log, past reviews, Git history, or hint of whether the commit is a
baseline or a candidate. It writes its result there, and the builder logs it.

The judge reads the snapshot, so keep review talk out of the project: no
comments, docs, or file names about reviews, scores, or feedback. Commit
messages are fine, since the snapshot leaves them out.

## Score history

Record each review in `.loop/results.tsv`. Increment `experiment` for each review,
starting at 0 for the baseline. Keep the same series ID until the goal or judge
model changes. Use the attempt branch name for its rows and `main` for a baseline.

Use these statuses:

- `baseline`: a review establishing the score of `main`.
- `trial`: a reviewed commit on an attempt branch.
- `merge`: promotion of a reviewed commit to `main`.
- `abandon`: an attempt archived without merging.

The builder appends every row, including review rows when it logs a review.
Merge and abandon rows reuse the latest review number. For a merge, record the
promoted commit's judged score. For an abandonment, record the tip's score if that
commit was reviewed; otherwise leave score empty. Mention the archive tag and
reason in the description. Keep descriptions short, without tabs or newlines.
Append complete newline-ended rows. The graph uses the latest scoring series.

## Review handoff

For each request, rebuild `.loop/judge/` with only what the judge needs:

```sh
rm -rf .loop/judge && mkdir -p .loop/judge/project
git archive <revision> | tar -x -C .loop/judge/project
cp goal.md JUDGE.md .loop/judge/
git init -q .loop/judge
```

The empty repo stops Git from walking up to the project's history.

Overwrite `.loop/review.json` with the request:

```text
kind: baseline or candidate
branch: main or the attempt branch
revision: exact commit to judge
result: null
```

The judge writes `.loop/judge/result.json`:

```text
score: 0.0–100.0
unmet_required: required outcomes still unmet
evidence: concrete observations
feedback: concise deficiencies for the next revision
```

To log a review, copy that file into `result`, append the review row to the
score log, run `python3 plot.py`, and delete `.loop/judge/`.

Keep one outstanding request at a time. `.loop/review.json` holds the current
handoff, `.loop/results.tsv` holds the history, and `.loop/progress.svg` holds the
graph. Archived code and attempt notes live in Git tags.
