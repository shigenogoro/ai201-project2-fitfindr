#!/usr/bin/env python3
"""
Run the capstone criteria (criteria.md, "Capstone criteria") as trials. ← CAPSTONE

    python capstone_trials.py --label before            three trials
    python capstone_trials.py --label after --trials 3

For each trial it starts `serve.py` once per fault setting (503:2 for C1,
503:99 for C2, none for C3 + C5), drives it with `bench.py`, stops it, and
then reads the log lines that trial added. Raw output for every trial goes to
results/capstone_<label>_trial<N>.txt; the per-criterion counts are printed and
written to results/capstone_<label>_summary.md.

The counts are computed from logs/runs.jsonl exactly as criteria.md words
them. Nothing here changes the system under test.
"""

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent
PY = sys.executable
LOG = ROOT / "logs" / "runs.jsonl"
URL = "http://127.0.0.1:5000"
FIELDS = ["ts", "input", "http_status", "outcome", "error", "n_results", "item_id",
          "fit_card_chars", "duration_ms", "model_calls", "retries", "prompt_tokens",
          "output_tokens", "fault", "model"]
OUTCOMES = {"ok", "no_match", "model_unavailable", "bad_input", "crash"}

C1 = ["denim jacket under $50"] * 5
C2 = ["denim jacket under $50"] * 3
C3_RAW = ["", "hello", "[1, 2]", '{"query": 42}', '{"query": "   "}', json.dumps({"query": "a" * 400})]
C5 = ["vintage graphic tee under $30", "90s track jacket in size M",
      "silk slip dress in midi length under $40", "platform sneakers size 8",
      "denim jacket under $50"]


def log_lines() -> list[dict]:
    if not LOG.exists():
        return []
    return [json.loads(l) for l in LOG.read_text(encoding="utf-8").splitlines() if l.strip()]


def with_server(fault: str | None, bench_args: list[list[str]], out) -> list[int]:
    """Start serve.py with this fault, run each bench command, stop it. Returns HTTP statuses in order."""
    env = {**os.environ, "AI201_CACHE": "0", "PYTHONIOENCODING": "utf-8"}
    env.pop("AI201_FAULT", None)
    if fault:
        env["AI201_FAULT"] = fault
    server = subprocess.Popen([PY, "serve.py"], cwd=ROOT, env=env,
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(60):
            try:
                urllib.request.urlopen(URL + "/health", timeout=2)
                break
            except OSError:
                time.sleep(0.5)
        statuses = []
        for args in bench_args:
            done = subprocess.run([PY, "bench.py", *args], cwd=ROOT, capture_output=True,
                                  text=True, encoding="utf-8", env=env)
            text = f"$ AI201_FAULT={fault or ''} python bench.py {' '.join(repr(a) if ' ' in a or not a else a for a in args)}\n{done.stdout}{done.stderr}\n"
            print(text, flush=True)
            out.write(text)
            statuses += [int(l.split()[0]) for l in done.stdout.splitlines() if l[:3].isdigit()]
        return statuses
    finally:
        server.terminate()
        server.wait(timeout=10)


def score(new: list[dict], sent_statuses: list[int]) -> dict:
    # Requests go out in a fixed order (5 C1, 3 C2, 6 C3, 10 C5), so records are
    # assigned by position. A missing line would shift these, and C4 catches that.
    a, b, c = len(C1), len(C1) + len(C2), len(C1) + len(C2) + len(C3_RAW)
    c1, c2, c3, c5 = new[:a], new[a:b], new[b:c], new[c:]
    tokens = [r["prompt_tokens"] + r["output_tokens"] for r in c5]
    complete = [r for r in new if set(FIELDS) <= set(r) and r["outcome"] in OUTCOMES]
    status_match = len(new) == len(sent_statuses) and all(
        r["http_status"] == s for r, s in zip(new, sent_statuses))
    return {
        "C1": (sum(1 for r in c1 if r["fit_card_chars"] > 0 and r["retries"] == 4 and r["duration_ms"] < 30000), len(c1),
               [(r["fit_card_chars"], r["retries"], r["duration_ms"]) for r in c1]),
        "C2": (sum(1 for r in c2 if r["http_status"] == 200 and "couldn't be reached" in (r["error"] or "")
                   and r["fit_card_chars"] == 0 and r["outcome"] == "model_unavailable" and r["duration_ms"] < 20000), len(c2),
               [(r["http_status"], r["outcome"], r["duration_ms"]) for r in c2]),
        "C3": (sum(1 for r in c3 if r["http_status"] == 400), len(c3),
               [r["http_status"] for r in c3]),
        "C4": (len(complete) if status_match else 0, len(sent_statuses),
               f"{len(new)} new lines for {len(sent_statuses)} requests, {len(complete)} complete, statuses match: {status_match}"),
        "C5": ((sum(1 for r in c5 if r["fit_card_chars"] > 0), sum(1 for r in c5 if r["duration_ms"] < 15000),
                round(sum(tokens) / len(tokens)) if tokens else None), len(c5),
               [(r["fit_card_chars"], r["duration_ms"], r["prompt_tokens"] + r["output_tokens"]) for r in c5]),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", required=True)
    ap.add_argument("--trials", type=int, default=3)
    args = ap.parse_args()
    (ROOT / "results").mkdir(exist_ok=True)

    summary = [f"# Capstone trials — {args.label}", "",
               "Produced by `capstone_trials.py`, counts read from `logs/runs.jsonl`.", ""]
    for t in range(1, args.trials + 1):
        before = len(log_lines())
        path = ROOT / "results" / f"capstone_{args.label}_trial{t}.txt"
        with path.open("w", encoding="utf-8") as out:
            out.write(f"# Capstone trial {t} ({args.label}), started {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            sent = with_server("503:2", [C1], out)
            sent += with_server("503:99", [C2], out)
            sent += with_server(None, [["--raw", *C3_RAW], ["-n", "2", *C5]], out)
            new = log_lines()[before:]
            out.write("## Log lines added in this trial\n\n")
            for r in new:
                out.write(json.dumps(r, ensure_ascii=False) + "\n")
            result = score(new, sent)
            out.write("\n## Counts\n\n")
            for k, v in result.items():
                out.write(f"{k}: {v[0]} of {v[1]}  {v[2]}\n")
        line = f"Trial {t}: " + "  ".join(f"{k} {v[0]}/{v[1]}" for k, v in result.items())
        print("\n" + line + "\n", flush=True)
        summary.append(f"- {line}  (raw: `{path.relative_to(ROOT).as_posix()}`)")
        for k, v in result.items():
            summary.append(f"    - {k}: {v[2]}")
    (ROOT / "results" / f"capstone_{args.label}_summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
