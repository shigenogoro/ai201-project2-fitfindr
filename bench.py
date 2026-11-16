#!/usr/bin/env python3
"""
Send requests to a running `python serve.py` and time them. ← CAPSTONE

    python bench.py 'vintage graphic tee under $30'            one request
    python bench.py -n 10 'denim jacket under $50'             ten in a row
    python bench.py --raw '[1, 2]' '{"query": 42}' ''          raw bodies, for the 400 path

Prints one line per request and a summary. The server writes the real record
(logs/runs.jsonl); this only drives it and shows what the caller saw.
Stdlib only, so it runs anywhere serve.py does.
"""

import argparse
import json
import statistics
import time
import urllib.error
import urllib.request


def post(url: str, body: str, timeout: float) -> tuple[int, dict, float]:
    req = urllib.request.Request(url, data=body.encode("utf-8"),
                                 headers={"Content-Type": "application/json"}, method="POST")
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status, raw = resp.status, resp.read()
    except urllib.error.HTTPError as exc:  # 4xx / 5xx still carry a body
        status, raw = exc.code, exc.read()
    seconds = time.perf_counter() - started
    try:
        data = json.loads(raw)
    except ValueError:
        data = {"error": raw[:120].decode("utf-8", "replace")}
    return status, data, seconds


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="+", help="queries (or raw bodies with --raw)")
    ap.add_argument("-n", type=int, default=1, help="send each input this many times")
    ap.add_argument("--raw", action="store_true", help="send each input as the literal request body")
    ap.add_argument("--url", default="http://127.0.0.1:5000/ask")
    ap.add_argument("--timeout", type=float, default=180)
    args = ap.parse_args()

    times, statuses = [], []
    for text in args.inputs:
        body = text if args.raw else json.dumps({"query": text})
        for i in range(1, args.n + 1):
            status, data, secs = post(args.url, body, args.timeout)
            times.append(secs)
            statuses.append(status)
            if data.get("error"):
                what = f"error: {str(data['error'])[:90]}"
            else:
                what = f"fit card {len(data.get('fit_card') or '')} chars, item {(data.get('selected_item') or {}).get('id')}"
            print(f"{status}  {secs:6.2f}s  {text[:40]!r:44} #{i}  {what}", flush=True)

    counts = {s: statuses.count(s) for s in sorted(set(statuses))}
    ordered = sorted(times)
    p90 = ordered[max(0, round(0.9 * len(ordered)) - 1)]
    print(f"\n{len(times)} requests  status counts {counts}  "
          f"median {statistics.median(times):.2f}s  p90 {p90:.2f}s  max {max(times):.2f}s")


if __name__ == "__main__":
    main()
