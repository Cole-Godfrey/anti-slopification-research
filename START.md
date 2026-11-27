# Start here

## Copy into a new project

From the new project's directory:

```sh
gh api repos/Cole-Godfrey/generalized-auto-research/tarball/advanced-mode | tar -xz --strip-components=1
```

## Setup once

Start a setup session and paste:

```text
Read the setup section of LOOP.md. My objective is:

[REPLACE THIS WITH YOUR ABSTRACT GOAL]

Ask me questions, then draft a short goal.md describing the desired result.
Prepare the baseline on main.
```

Answer its questions, then run the pilot in `PILOT.md`.

## 1. Start a fresh session with the `MODELS.md` builder.

```text
/goal Read LOOP.md and start a new attempt from main to move the project closer
to goal.md. Create a branch, make your initial implementation, commit it, and
prepare a review request. Finish when the request is ready.
```

## 2. Open a fresh session for each judge.

Start judge `<n>` from `MODELS.md` in its folder. With Claude Code:

```sh
cd .loop/judge/<n> && claude --safe-mode --model <model>  # no CLAUDE.md, skills, plugins, hooks, or MCP
```

Paste:

```text
Read JUDGE.md and follow it.
```

## 3. Return to the same builder session.

```text
/goal Read the reviews in .loop/judge/*/result.json and follow LOOP.md for this attempt.
Choose whether to merge, abandon, or revise. If revising, commit your changes
and request another review.
```

Repeat steps 2 and 3 while working on that branch. After MERGED or ABANDONED,
return to step 1 in a fresh builder session. A review score above 90 completes
the project; return to the builder to finalize the reviewed commit.

## Progress

Open `.loop/progress.svg`. To regenerate it yourself:

```sh
python3 plot.py
```
