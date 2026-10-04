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
