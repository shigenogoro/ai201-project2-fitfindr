# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:**
<!-- Why 4 of 5 and not 5 of 5? Something about your search, probably —
     "my search is a plain keyword match and some phrasings will miss" is a
     real answer. -->

My search strategy is plain keyword matching, and the query is parsed by string splitting, and some phrasings will miss.

---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:**
<!-- Why is 5 of 5 reasonable here when criterion 1 isn't? What's different
     about this path? -->

Since I've already stated clearly that if there is no matching item, in other words, the `search_listings` returns an empty list, the agent should put a message in the session and stop. Therefore, it should never invoke `suggest_outfit` in this case.

Unlike criterion 1, this path is deterministic: it is a plain `if not results` check on the output of `search_listings`, which doesn't call the model. Nothing about phrasing or model output can change the branch, so there is no reason to allow a miss. The message is also checkable: it must name the filter(s) the user can change (the price ceiling, the size, or the keywords).

---

## 3. The selected item is the same item all the way through

Given a query that matches at least one listing, `session["selected_item"]["id"]`
equals `search_results[0]["id"]`, and also equals the `id` of the item that
actually reached `suggest_outfit` and `create_fit_card` — 5 of 5 tries.

**Why this target:**

Passing the selected item along is plain variable passing with no model in the
way, so there is no excuse for a miss. If this fails, it is a loop or session
bug (the loop re-fetched a different listing, or the item was mutated along the
way), not a tool problem, and 5 of 5 is what exposes it.

---

## 4. Something about the fit card

Across 5 tries, each fit card (a) contains the item's price and platform name,
in 5 of 5 tries, and (b) is 2 to 4 sentences long, in at least 4 of 5 tries.

**Why this target:**

The price and platform come straight from the listing and the prompt asks for
them explicitly, so a missing one means the prompt or the tool is wrong, and I
can check it with a string match. Sentence count depends on the model's wording,
which varies run to run (and the caption is never word-for-word the same), so I
allow one miss in five.

---

## 5. Your choice
Given 5 queries that each include a `max_price` and a `size`, every result
`search_listings` returns has `price <= max_price` and a size that matches under
my size rule (so "S" never returns "US 9", and "L" never returns "XL") — 5 of 5
queries, with zero violating results.

**Why this target:**

Search is the one tool that doesn't call the model, so it is fully deterministic
and there is no reason to allow a miss. The size field mixes clothing sizes and
shoe sizes, and a plain substring test would let wrong items through, which
reads to the user like a broken search.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Capstone criteria (Unit 9) — hardening FitFindr

Written after Milestone 3's measurement run and **before any capstone test
results exist**. The Unit 3 criteria above are left as they were.

**Setup used by every criterion.** The server is started with
`AI201_CACHE=0 python serve.py` (plus the `AI201_FAULT` value the criterion
names), and requests are sent with `bench.py` to `http://127.0.0.1:5000/ask`.
"Duration" always means the `duration_ms` field in `logs/runs.jsonl`, the
server-side time for the request, not what the client measured. One **trial**
is one full pass of the requests listed under the criterion. Each criterion
is run as three trials, with nothing changed between them.

Criteria 1 to 4 are about the extension (retries, giving up, input checks,
the log). Criterion 5 is about the system as it already worked, to show the
hardening didn't make the normal path worse.

## C1. A transient model failure is recovered from, not passed to the user

With the server started under `AI201_FAULT=503:2` (every model call fails
twice with a 503 before the real call is allowed through), 5 requests for
`'denim jacket under $50'` per trial. **Target: 5 of 5 requests return a
non-empty fit card, each with `retries` = 4 in its log record (2 per model
call), and each with a duration under 30 s.**

**Why this target:** This is the failure that sank my Unit 4 runs, and the
retry exists only for it. Two failures per call is well inside the 5
attempts allowed, so a correct retry should recover every time; 4 of 5 would
mean one user still got an apology for a failure the code is supposed to
absorb. `retries` = 4 is checked so that a pass can't come from the fault
switch silently not being on. 30 s, because the backoff adds about 6 s
(1 s + 2 s per call) to a normal run whose slowest measured case was 20.6 s;
a user waiting past 30 s for a caption has usually left.

## C2. When the model never comes back, the user hears so quickly and clearly

With the server started under `AI201_FAULT=503:99` (every model attempt
fails), 3 requests for `'denim jacket under $50'` per trial. **Target: 3 of 3
return HTTP 200 (not 500) with an `error` containing "couldn't be reached",
`fit_card` null, a log record with `outcome` = `model_unavailable`, and a
duration under 20 s.**

**Why this target:** Giving up is the bad path the retry creates: the more
patient the retry, the longer a user waits to hear that nothing is coming.
20 s is the slowest *successful* normal run I measured in Milestone 3
(20.6 s, rounded down). An answer that says "failed" should not take longer
than the slowest answer that worked. A 500 or a missing sentence would mean
the agent's existing `ModelUnavailable` handler was bypassed, which is what
happened before this unit when retries ran out (it raised `RuntimeError`).

## C3. Malformed input gets a 400, never a 500

No fault. Six bodies per trial, sent with `bench.py --raw`: an empty body,
`hello` (not JSON), `[1, 2]`, `{"query": 42}`, `{"query": "   "}`, and a
query of 400 `a` characters. **Target: 6 of 6 return HTTP 400 with a JSON
`error` message, and 0 return 500.**

**Why this target:** These are checked by plain code before the agent runs,
with no model involved, so there is no randomness to allow for. One 500 is a
bug, not bad luck: before this unit, two of these six crashed into a 500.

## C4. Every request leaves exactly one complete log record

Across all the requests sent for C1, C2, C3 and C5 in a trial (5 + 3 + 6 + 10
= 24). **Target: the number of new lines in `logs/runs.jsonl` equals the
number of requests sent (24 of 24), every new line parses as JSON, and every
one has all 15 fields (`ts`, `input`, `http_status`, `outcome`, `error`,
`n_results`, `item_id`, `fit_card_chars`, `duration_ms`, `model_calls`,
`retries`, `prompt_tokens`, `output_tokens`, `fault`, `model`) with a known
`outcome` value, and `http_status` matching what `bench.py` printed for
that request.**

**Why this target:** The log is the only way to answer a question about a
past run without re-running it. A log that drops failed requests is worse
than none, because it makes the system look healthier than it is. That's why
the count must be exact, not "most". Matching `http_status` against what the
client saw checks that the log records what happened and not what the code
meant to happen.

## C5. The normal path is still fast and still cheap

No fault. 10 requests per trial: the five example queries
(`'vintage graphic tee under $30'`, `'90s track jacket in size M'`,
`'silk slip dress in midi length under $40'`, `'platform sneakers size 8'`,
`'denim jacket under $50'`), twice each. **Target: 10 of 10 return a fit
card, at least 9 of 10 have a duration under 15 s, and the average
`prompt_tokens + output_tokens` is at most 1,000 per request.**

**Why this target:** This is the original system, and the hardening touched
every model call it makes (timeout, empty-reply check, retry
classification). If any of that misfires on a healthy call (say a real
reply gets treated as transient and retried), it shows up here as extra time
and extra tokens. 15 s is about twice the median I measured in Milestone 3
(7.8 s). 9 of 10 rather than 10 of 10 because one in ten of those runs was
slower than 15 s with no fault at all (the model's own variance), and I don't
want this criterion to be about Gemini's slowest moment. 1,000 tokens is
about 40% above the measured average (704), room for a longer caption but
not for a hidden third model call.
