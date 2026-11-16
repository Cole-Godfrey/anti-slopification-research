#!/usr/bin/env python3
"""Plot a goal loop's results.tsv as SVG. Python standard library only."""

import argparse
import csv
from html import escape
import math
from pathlib import Path
import sys


COLORS = {
    "main": "#187a59", "trial": "#367ac2", "merge": "#7a58b5",
    "abandon": "#a5adb7",
}


def read_results(path):
    rows = []
    with path.open(newline="") as stream:
        for row in csv.DictReader(stream, delimiter="\t"):
            try:
                score = float(row["score"]) if row["score"] else None
                experiment = int(row["experiment"])
                status = row["status"]
                series = row["series"]
                branch = row["branch"]
            except (KeyError, TypeError, ValueError):
                continue  # skip incomplete rows
            valid_score = (status == "abandon" and score is None) or (
                score is not None and math.isfinite(score) and 0 <= score <= 100
            )
            if (series and branch and valid_score and experiment >= 0
                    and status in {"baseline", "trial", "merge", "abandon"}):
                rows.append({**row, "score": score, "experiment": experiment})
    return [row for row in rows if row["series"] == rows[-1]["series"]] if rows else []


def render(rows):
    width, height = 1000, 560
    left, right, top, bottom = 76, 968, 100, 480
    last = max((row["experiment"] for row in rows), default=1) or 1
    x = lambda value: left + value / last * (right - left)
    y = lambda value: bottom - value / 100 * (bottom - top)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        '<title id="title">Goal loop progress</title>',
        '<desc id="desc">Main baseline and attempt scores by review, with archived attempts. A score above 90 completes the project.</desc>',
        '<style>text{font-family:system-ui,sans-serif;fill:#56616f;font-size:13px}</style>',
        '<rect width="1000" height="560" fill="#ffffff"/>',
        '<text x="76" y="38" style="font-size:24px;font-weight:600;fill:#17212b">Goal loop progress</text>',
    ]
    series = escape(str(rows[-1]["series"])) if rows else "Waiting for judged experiments"
    parts.append(f'<text x="76" y="65">{series}</text>')
    for value in range(0, 101, 20):
        parts.append(f'<path d="M{left},{y(value):.1f} H{right}" stroke="#e8ecf0"/>')
        parts.append(f'<text x="60" y="{y(value) + 5:.1f}" text-anchor="end">{value}</text>')
    parts.extend([
        f'<path d="M{left},{y(90):.1f} H{right}" stroke="#a16a13" stroke-dasharray="6 5"/>',
        f'<text x="{right}" y="{y(90) - 9:.1f}" text-anchor="end" style="fill:#a16a13">&gt;90 · completion</text>',
        '<text x="20" y="290" transform="rotate(-90 20 290)">Score</text>',
        '<text x="522" y="530" text-anchor="middle">Review</text>',
    ])
    ticks = sorted({round(last * index / 5) for index in range(6)})
    for value in ticks:
        parts.append(f'<text x="{x(value):.1f}" y="505" text-anchor="middle">{value}</text>')
    # main advances when an attempt merges
    baseline, line = None, []
    for row in rows:
        if row["status"] in {"baseline", "merge"}:
            if baseline is not None:
                line.append(f'L{x(row["experiment"]):.1f},{y(baseline):.1f}')
            line.append(f'{"M" if baseline is None else "L"}{x(row["experiment"]):.1f},{y(row["score"]):.1f}')
            baseline = row["score"]

    # group reviews by attempt; terminal events determine its final color
    attempts, outcomes = {}, {}
    for row in rows:
        if row["status"] == "trial":
            attempts.setdefault(row["branch"], []).append(row)
        elif row["status"] in {"merge", "abandon"}:
            outcomes[row["branch"]] = row["status"]
    for branch, reviews in attempts.items():
        color = COLORS[outcomes.get(branch, "trial")]
        points = " ".join(f'{x(row["experiment"]):.1f},{y(row["score"]):.1f}' for row in reviews)
        label = escape(f'{branch}: {outcomes.get(branch, "active")}')
        parts.append(f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="1.5" opacity="0.7"><title>{label}</title></polyline>')
    if line:
        line.append(f'L{x(last):.1f},{y(baseline):.1f}')
        parts.append(f'<path d="{" ".join(line)}" fill="none" stroke="{COLORS["main"]}" stroke-width="2.5"/>')
    for row in rows:
        if row["status"] in {"merge", "abandon"}:
            continue  # the review already supplies the point
        color = COLORS[outcomes.get(row["branch"], "trial")] if row["status"] == "trial" else COLORS["main"]
        label = escape(f'{row["branch"]} · {row["status"]}: {row["score"]:.1f} · {row.get("revision", "")} · {row.get("description", "")}')
        parts.append(f'<circle cx="{x(row["experiment"]):.1f}" cy="{y(row["score"]):.1f}" r="4" fill="{color}"><title>{label}</title></circle>')
    legend = [(76, "main", "Main baseline"), (270, "trial", "Active attempt"),
              (450, "merge", "Merged attempt"), (650, "abandon", "Archived attempt")]
    for position, kind, label in legend:
        color = COLORS[kind]
        parts.append(f'<circle cx="{position}" cy="552" r="4" fill="{color}"/><text x="{position + 12}" y="556">{label}</text>')
    parts.append('</svg>')
    return "\n".join(parts) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("results", nargs="?", type=Path, default=Path(".loop/results.tsv"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    output = args.output or args.results.with_name("progress.svg")
    if output.resolve() == args.results.resolve():
        parser.error("Output must differ from the score log.")
    rows = read_results(args.results)
    output.write_text(render(rows), encoding="utf-8")
    print(f"Updated {output} ({len(rows)} judgments)")


if __name__ == "__main__":
    try:
        main()
    except OSError as error:
        sys.exit(str(error))
