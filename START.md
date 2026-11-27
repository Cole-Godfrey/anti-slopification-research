# Start here

## Copy into a new project

From the new project's directory:

```sh
gh api repos/Cole-Godfrey/generalized-auto-research/tarball/main | tar -xz --strip-components=1
```

## Setup once

Start a setup session and paste:

```text
Read the setup section of LOOP.md. My objective is:

[REPLACE THIS WITH YOUR ABSTRACT GOAL]

Ask me questions, then draft a short goal.md describing the desired result.
Prepare the baseline on main and request its initial review.
```

Answer its questions, then use the judge prompt in step 2 to score the baseline.

## 1. Start a fresh builder session from the baseline.

```text
/goal Read LOOP.md and start a new attempt from main to move the project closer
to goal.md. Create a branch, make your initial implementation, commit it, and
prepare a review request. Finish when the request is ready.
```

## 2. Open a fresh judge session in `.loop/judge/`.

From the project, start the judge in its folder. Safe mode turns off CLAUDE.md,
skills, plugins, hooks, and MCP servers, so only `JUDGE.md` and `goal.md` steer
it. Use a separate model if available.

```sh
cd .loop/judge && claude --safe-mode
```

Paste:

```text
Read JUDGE.md and judge this packet. Write result.json, then finish.
```

## 3. Return to the same builder session.

```text
Log the judge's review and follow LOOP.md for this attempt. Choose whether to
merge, abandon, or revise. If revising, commit your changes and request
another review.
```

Repeat steps 2 and 3 while working on that branch. After MERGED or ABANDONED,
return to step 1 in a fresh builder session. A judge score above 90 completes
the project; return to the builder to finalize the reviewed commit.

## Progress

Open `.loop/progress.svg`. To regenerate it yourself:

```sh
python3 plot.py
```
