# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->

A user types a plain-language request such as "vintage graphic tee under $30, size M". FitFindr searches a set of secondhand listings for the best match within the price and size limits, then suggests one or two outfits that combine the find with pieces from the user's wardrobe (or general styling advice if the wardrobe is empty). Finally it writes a short caption the user could post about the find. If nothing matches, it stops early and tells the user which limit to loosen instead of making up an outfit.


---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:** 
     
     It search the listings data for items matching a description, and optionally a size and a price ceiling.

- **Inputs:** <!-- name and type each: `max_price` (float), not "a price" -->

     1. `description` (string): Keywords describing what the user wants
     2. `size` (string | None): A size string to filter by, or None to skip size filtering. 
          **Size match rule:** matching is case-insensitive and by whole token, not substring. The listing's size is split on `/` and whitespace into tokens, and the requested size must equal one token exactly. So `"M"` matches `"S/M"`, `"S"` does not match `"US 9"`, and `"L"` does not match `"XL"`.
     3. `max_price` (float | None): Maximum price inclusively, or None to skip price filtering.

- **Returns:**
     
     A list of full listing dicts (id, title, description, category, style_tags, size, condition, price, colors, brand, platform), best keyword-overlap score first, at most `config.SEARCH_RESULT_LIMIT` of them. Every result satisfies the price ceiling and the size rule above.

- **When it has nothing:**
     
     An *empty list* will be returned when nothing matches. It should not return *None* or an *exception* when nothing matches.

### `suggest_outfit`

- **What it does:**

     Given an item and the user's wardrobe, the function will suggest one or two outfits.

- **Inputs:**

     1. `new_item` (dict): the item that the user is considering, which is represented as a listing dict.
     2. `wardrobe` (dict): a wardrobe dict with an 'items' key holding a listof items. It **may be empty**, and we need to handle it. 

- **Returns:**

     If the given wardrobe is non-empty, we should return a **non-empty string** with outfit suggestions. 

- **When it has nothing:**

     If the wardrobe is empty, we should return a general styling advice rather than raising an exception or returning an empty string "".

### `create_fit_card`

- **What it does:**

     The function write a short caption someone would actually post about the find.

- **Inputs:**

     1. `outfit` (string): the outfit suggestion from `suggest_outfit()`
     2. `new_item` (dict): the listing dict for the item.

- **Returns:**

     The funciton returns a two-to-four sentence caption.

- **When it has nothing:**

     If `outfit` is empty or whitespace, the function should still return a descriptive message rather than raising an exception.

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:**

     If `search_listings` returns an empty list, put a message in the session and stop. Otherwise take the first result and go to `suggest_outfit`.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** <!-- regex, string splitting, or asking the model — say which -->

     The query is parsed by string splitting. To be more specific, A user inputs keywords describing what he/she wants, so we can simply use string spliting to extract keywords from the user input.

**What moves through the session:** <!-- which fields, in what order -->

     1. User input keywords describe what he/she wants.

     2. Agent invoke `search_listings()` tool to search a list of matching items.

     3. If the return listing is empty, the session should stop here. Otherwise, agent will pick the first item and pass it to `suggest_outfit()` to generate a suggestion for the user.

     4. After the suggestion is generated, the agent will invoke `create_fit_card()` to generate a short caption that user can post about the find.

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask 'vintage graphic tee under $30'
  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   **Outfit 1: Casual Y2K Streetwear**
Pair the Y2K Baby Tee with your baggy straight-leg jeans for a classic early 2000s silhouette. Layer the black cropped zip hoodie over top for easy warmth, and finish the look with chunky white sneakers and the black crossbody bag. 

**Outfit 2: Effortless Retro Contrast**
Tuck the Y2K Baby Tee into your wide-leg khaki trousers, secured with the brown leather belt to define the waist. Throw on the vintage black denim jacket as outerwear and complete the outfit with chunky white sneakers for a cool, balanced mix of edgy and neutral tones.

  Fit card: scored this butterfly baby tee for just $18.00 on depop and i am officially living my 2000s pop star dream. the fit is *so* tiny and cute—totally leaning into that nostalgic, effortless streetwear vibe for class tomorrow.

0 model calls this session, 2 served from cache
```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
[{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_012', 'title': 'Oversized Crewneck Sweatshirt — Vintage Navy', 'description': 'Perfectly faded navy crewneck. Genuinely vintage — not manufactured distressed. Ribbed cuffs and hem. No graphics, clean.', 'category': 'tops', 'style_tags': ['vintage', 'basics', 'oversized', 'classic'], 'size': 'XL (fits oversized)', 'condition': 'good', 'price': 20.0, 'colors': ['navy'], 'brand': None, 'platform': 'thredUp'}, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'}]
```

```
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
**Outfit 1: Casual & Cool**
Pair the vintage Levi's 501 jeans with the **White ribbed tank top** tucked in, layered under the **Oversized grey crewneck sweatshirt**. Accessorize with the **Brown leather belt** and **Black crossbody bag**, and finish the look with the **Chunky white sneakers**. 

**Outfit 2: Edgy Streetwear**
Combine the vintage Levi's 501 jeans and the **Brown leather belt** with the **Black cropped zip hoodie**. Throw on the **Vintage black denim jacket** as outerwear, slip into the **Black combat boots**, and complete the outfit using the **Black crossbody bag**.
```

```
$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
scored these vintage Levi's 501 jeans on depop for just $38.00 and I'm obsessed with the knee fading. honestly the ultimate relaxed 90s vibe, especially paired with crisp white sneakers.
```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:* I gave Claude my README spec and my draft criteria.md and asked it to review the criteria I'd written so far.
- *What came back:* It pointed out that criterion 3 ("something about state") was wrong in two ways. It said I'd pass the whole list from `search_listings` to `suggest_outfit`, which contradicts my own branch rule (take the first result), and "returns a non-empty string" is a tool contract, not state.
- *What I changed:* I rewrote criterion 3 so it compares ids: `session["selected_item"]["id"]` must equal `search_results[0]["id"]` and the id of the item that actually reached `suggest_outfit` and `create_fit_card`, 5 of 5 tries. I also had it help me draft criteria 4 (price and platform in the card, 2-4 sentences) and 5 (price and size filters), and wrote my size matching rule into the Tool Inventory so criterion 5 has something to check against.

**Moment 2**

- *What I asked for:* I asked Claude to implement the three tools in tools.py, using `load_listings()` and `generate()`, following my Tool Inventory (including the whole-token size rule).
- *What came back:* Its first edit was applied through a shell script and the prompt strings in `suggest_outfit` were broken by newline escaping, so `import tools` failed with `SyntaxError: unterminated f-string literal`.
- *What I changed:* I had it `git checkout tools.py` and re-apply the same edit from a script file. Then I tested instead of trusting it: `search_listings(size='S')` returned only S, S/M sizes (no "US 9"), `size='L'` returned L and L/XL (no "XL"), an impossible query returned `[]`, and with `AI201_CACHE=0` three runs of `create_fit_card` on the same item gave three different captions, so temperature 0.9 is working.

**Moment 3 (unit 4)**

- *What I asked for:* After the model kept returning 503, I asked Claude to run my `before` eval on Haiku through my Pro plan.
- *What came back:* It told me the Gemini adapter can't call Haiku, then found that `claude -p --model haiku` works with my plan, and added an optional `AI201_PROVIDER=claude` branch to `generate.py` (default still Gemini). It also said there is no "Haiku 5.5"; the latest Haiku is 4.5.
- *What I changed:* I kept the change but made sure it is off by default and wrote it up honestly at the bottom of this README, including that `config.TEMPERATURE` doesn't apply to the Haiku runs. I also noticed my first plan (just editing `AI201_MODEL`) would not have worked, and the model listing Claude pulled showed `gemini-2.5-flash` isn't available on my key.

**Moment 4 (unit 4)**

- *What I asked for:* I asked Claude to argue against my own verdict that criterion 5 was MET.
- *What came back:* It pointed out that my test query (`'tee size L under $25'`) returned the same two items with a plain substring size check as with my whole-token rule, so the PASS proved nothing about the size rule, and then it showed me a query that could tell them apart.
- *What I changed:* I replaced that scenario with `'top size S under $30'` (a substring check also returns `XL (oversized)` and `US 9` for it), added a `--criterion` flag to `run_eval.py` so I could re-run just that one, re-ran it, and wrote the old test's weakness into the README instead of hiding it.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Matching query completes all three tools and returns a fit card | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Impossible query stops before `suggest_outfit`, message names what to change | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. `selected_item` id equals the id that reached `suggest_outfit` and `create_fit_card` | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4a. Fit card contains the item's price and platform | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4b. Fit card is 2 to 4 sentences | 4 of 5 | PASS | PASS | PASS | FAIL | PASS | MET (4/5) |
| 5. Every search result is within `max_price` and matches `size` (re-run, see below) | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

Criterion 4 has two clauses with different targets in `criteria.md`, so it gets two rows (4a, 4b). Rows 1 to 4 come from `python run_eval.py --label before` with caching off; the raw output is in `results/run_2026-10-13_2336_before.md`. Row 5 was re-run on its own with `python run_eval.py --label before_c5 --criterion 5` (raw output in `results/run_2026-10-13_2355_before_c5.md`) because my first scenario for it could not fail: see the Verdicts section. The agent was not changed between the two runs, only that scenario's query. This run used Haiku through `claude -p`, not Gemini — see "Model availability problem" at the bottom of this file.

How I decided each try: 1 = a fit card came back; 2 = the trace stops at the `branch` step with no `suggest_outfit` step and the message names the filters; 3 = the `id` in the `select item`, `suggest_outfit` and `create_fit_card` steps is the same; 4a = the item's price (`$30` or `$30.00`) and platform name both appear in the card; 4b = I counted sentences by hand; 5 = I checked every result's `price` and `size` by re-running `search_listings` with the parsed arguments (the results file only records titles); all five tries returned the same three items, all `S/M`, priced $18, $15 and $22. The one 4b miss (try 4) is a single run-on sentence with no full stop: "found this delicate floral silk slip on depop for $30.00 and it's already become my favorite layering piece—…which wasn't even the plan".

**Real output from one try per criterion**, pasted as text, naming the file and function that produced it:

**Criterion 1 — matching query completes (`agent.py::run_agent`, `tools.py::create_fit_card`)**

```
$ python app.py ask 'vintage graphic tee under $30' --trace   (try 1)
[1] parse query
      in:  vintage graphic tee under $30
      out: {'description': 'vintage graphic tee', 'size': None, 'max_price': 30.0}
[2] search_listings (via MCP)
      in:  {'description': 'vintage graphic tee', 'size': None, 'max_price': 30.0}
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
[3] select item
      in:  10 results
      out: id lst_002 Y2K Baby Tee — Butterfly Print
[4] suggest_outfit
      in:  id lst_002 Y2K Baby Tee — Butterfly Print, wardrobe of 10 items
      out: # Outfit Ideas for Your Y2K Baby Tee  **Outfit 1: Classic Y2K** Pair the Y2K Baby Tee with your **Baggy straig…
[5] create_fit_card
      in:  id lst_002 Y2K Baby Tee — Butterfly Print
      out: just scored this adorable y2k butterfly baby tee on depop for $18.00 and i'm absolutely obsessed 🦋 the butterf…

Fit card: just scored this adorable y2k butterfly baby tee on depop for $18.00 and i'm absolutely obsessed 🦋 the butterfly graphic is straight-up early 2000s perfection and the fitted crop works with literally everything. already planning to wear it with my baggy jeans AND dress it up with trousers because that's the vibe we're going for.
```

**Criterion 2 — impossible query stops early (`agent.py::run_agent`, the branch)**

```
$ python app.py ask 'designer ballgown size XXS under $5' --trace   (try 1)
[1] parse query
      in:  designer ballgown size XXS under $5
      out: {'description': 'designer ballgown', 'size': 'XXS', 'max_price': 5.0}
[2] search_listings (via MCP)
      in:  {'description': 'designer ballgown', 'size': 'XXS', 'max_price': 5.0}
      out: [] (empty)
[3] branch
      →    search returned nothing -> stopping, suggest_outfit not called

Session error: No listings matched keywords 'designer ballgown', size XXS, under $5. Try raising the price limit, dropping the size, or using broader keywords.
```

**Criterion 3 — selected item reaches suggest_outfit (`agent.py::run_agent`; the same `id` appears at steps 3, 4 and 5)**

```
$ python app.py ask '90s track jacket in size M' --trace   (try 1)
[1] parse query
      in:  90s track jacket in size M
      out: {'description': '90s track jacket in', 'size': 'M', 'max_price': None}
[2] search_listings (via MCP)
      in:  {'description': '90s track jacket in', 'size': 'M', 'max_price': None}
      out: 3 items: 90s Track Jacket — Navy/White Stripe, 90s Silk Slip Dress — Floral, Midi Length, 90s Leather Bomber — Black
[3] select item
      in:  3 results
      out: id lst_004 90s Track Jacket — Navy/White Stripe
[4] suggest_outfit
      in:  id lst_004 90s Track Jacket — Navy/White Stripe, wardrobe of 10 items
      out: # Outfit Ideas for Your Track Jacket  **Outfit 1: Classic 90s Vibe** Layer your **White ribbed tank top** unde…
[5] create_fit_card
      in:  id lst_004 90s Track Jacket — Navy/White Stripe
      out: just scored this champion 90s track jacket on poshmark for $45 and i'm literally obsessed 😍 the navy/white str…

Fit card: just scored this champion 90s track jacket on poshmark for $45 and i'm literally obsessed 😍 the navy/white stripe detail is everything and the weight is perfect for layering into fall. this piece is going to be on repeat with literally everything in my closet.
```

**Criterion 4 — fit card has price and platform (`tools.py::create_fit_card`)**

```
$ python app.py ask 'silk slip dress in midi length under $40' --trace   (try 1)
[1] parse query
      in:  silk slip dress in midi length under $40
      out: {'description': 'silk slip dress in midi length', 'size': None, 'max_price': 40.0}
[2] search_listings (via MCP)
      in:  {'description': 'silk slip dress in midi length', 'size': None, 'max_price': 40.0}
      out: 2 items: 90s Silk Slip Dress — Floral, Midi Length, Silk Button-Down — Sage Green
[3] select item
      in:  2 results
      out: id lst_013 90s Silk Slip Dress — Floral, Midi Length
[4] suggest_outfit
      in:  id lst_013 90s Silk Slip Dress — Floral, Midi Length, wardrobe of 10 items
      out: **Outfit 1: Casual-Cool 90s Vibe** Layer your **Vintage black denim jacket** over the slip dress, pair with **…
[5] create_fit_card
      in:  id lst_013 90s Silk Slip Dress — Floral, Midi Length
      out: found this 90s floral slip dress on depop for $30 and literally wore it the next day. there's a tiny snag on t…

Fit card: found this 90s floral slip dress on depop for $30 and literally wore it the next day. there's a tiny snag on the side seam that nobody will ever see, but honestly it just adds to the vintage charm at this point. paired it with my black denim jacket and suddenly i'm having a whole grunge moment—this dress is the vibe.
```

**Criterion 5 — price and size filters hold (`tools.py::search_listings`, called via `mcp_server.py`)** — from `results/run_2026-10-13_2355_before_c5.md`, the re-run described below

```
$ python app.py ask 'top size S under $30' --trace   (try 1)
[1] parse query
      in:  top size S under $30
      out: {'description': 'top', 'size': 'S', 'max_price': 30.0}
[2] search_listings (via MCP)
      in:  {'description': 'top', 'size': 'S', 'max_price': 30.0}
      out: 3 items: Y2K Baby Tee — Butterfly Print, Mesh Long-Sleeve Top — Black, Crochet Halter Top — Cream
[3] select item
      in:  3 results
      out: id lst_002 Y2K Baby Tee — Butterfly Print
[4] suggest_outfit
      in:  id lst_002 Y2K Baby Tee — Butterfly Print, wardrobe of 10 items
      out: **Outfit 1: Casual Y2K** Pair the Y2K Baby Tee with your **Baggy straight-leg jeans, dark wash**. Layer with t…
[5] create_fit_card
      in:  id lst_002 Y2K Baby Tee — Butterfly Print
      out: found this butterfly baby tee on depop for $18 and i'm obsessed 🦋 the fitted crop is *chef's kiss* early 2000s…

Fit card: found this butterfly baby tee on depop for $18 and i'm obsessed 🦋 the fitted crop is *chef's kiss* early 2000s energy and already goes with everything. gonna be living in this all season
```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Matching query completes all three tools and returns a fit card | 4 of 5 | MET (5/5) | A fit card came back in all five tries of `'vintage graphic tee under $30'`, and none of the five stopped early. |
| 2 | Impossible query stops before `suggest_outfit`, message names what to change | 5 of 5 | MET (5/5) | All five traces end at the `branch` step with no `suggest_outfit` step and `fit_card` still `None`; every message listed the keywords, size and price I had asked for and what to change. |
| 3 | `selected_item` id equals the id that reached `suggest_outfit` and `create_fit_card` | 5 of 5 | MET (5/5) | The id printed at `select item`, `suggest_outfit` and `create_fit_card` was the same in all five traces. |
| 4a | Fit card contains the item's price and platform | 5 of 5 | MET (5/5) | I looked for the price (`$30` or `$30.00`) and `depop` in each card by hand; all five had both. |
| 4b | Fit card is 2 to 4 sentences | 4 of 5 | MET (4/5) | Four cards had 2 to 3 sentences. Try 4 was one long sentence with no full stop, so it failed; four of five is exactly the target. |
| 5 | Every search result is within `max_price` and matches `size` | 5 of 5 | MET (5/5), after fixing the test | Re-run with `'top size S under $30'`: all five tries returned the same three items (sizes `S/M`, prices $18, $15, $22). A substring size test returns six items for this query, adding `XL (oversized)`, `XL (fits oversized)` and `US 9`, so this scenario can tell the two apart. My first scenario (`'tee size L under $25'`) could not: I ran it with a deliberately wrong substring size test and it returned the same two items, so a PASS there proved nothing about the size rule. |

**Diagnoses**

I missed nothing against the Haiku run, so there is no miss to diagnose from it. I don't think that means the agent is done, so here is how I'd read it plainly.

*My targets were too easy in two places, and one test was too weak.*

- **Criterion 1** is the one I'd tighten. "Completes" only checks that a card came back, not that the item was the right one. The search ranks by keyword overlap only: `'graphic tee'` under $30 also returns a mesh long-sleeve top and a navy crewneck sweatshirt whose own description says "No graphics". Those got through because one word in their descriptions matched. A card for the wrong item would still have counted as a PASS. I'd add a clause: the selected item's category or style tags match the query.
- **Criterion 5** — the test, not the target. The first scenario I wrote for it (`'tee size L under $25'`) passed 5 of 5, but it would have passed with the wrong size rule too, so I replaced the query with `'top size S under $30'` and re-ran only that scenario. The agent itself did not change. This is a change to the scenario in `scenarios.py`, not to the criterion in `criteria.md`, whose wording and 5-of-5 target I left alone.
- **Criterion 3** is close to a tautology the way I measured it. The `id` printed in the trace comes from `session["selected_item"]`, which is also what the call is given, so the two can't disagree unless somebody rewrites the loop. A better test spies on the arguments `suggest_outfit` actually receives. I did that once by hand (a wrapper around `suggest_outfit` confirmed `received is session["selected_item"]` was `True`) but it isn't part of `run_eval.py`.

*Where the agent was actually weak.* Before I switched models, the same agent on the default `gemini-3.5-flash-lite` failed most of the time. Read against my targets, that evening's runs would have been MISSED on criteria 1, 3, 4 and 5 (for example `run_2026-10-13_2141_before.md`: every try that needed the model failed, 25 of 25). The mechanism is in the model's service plus one thing I can fix: `generate.py` only retries `429` and treats `503` as "model unavailable" straight away, so a transient `503` ends the run. The agent did the right thing when it happened (the Milestone 2 handler printed a clear message and nothing crashed), but that is graceful failure, not success. I'm reporting this as a finding, not counting it toward the Haiku verdicts, because the service problem and my agent are mixed together in those runs. The detail is in "Model availability problem" at the bottom of this file.

*Pattern.* If I had to name one problem, it's that every place my agent can fail on content (relevance of the search result, wording of the fit card) is judged only by whether something came back. The branch (criterion 2) and the filters (criterion 5) are deterministic and held. The model-dependent parts held too, but my criteria for them are the loosest ones.

*One thing I noticed in a passing try.* Try 4 of the fit-card scenario is a run-on: "found this delicate floral silk slip on depop for $30.00 and it's already become my favorite layering piece—the muted print screams quiet 90s but it actually plays so well with my edgier pieces, which wasn't even the plan". Place: the model's output. Mechanism: the prompt says "2-4 sentences" but nothing enforces it, so a one-sentence caption is possible about one run in five. It's the 4b miss I allowed myself and it landed exactly at the limit.

---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```
$ python app.py ask 'vintage graphic tee under $30' --trace
[1] parse query
      in:  vintage graphic tee under $30
      out: {'description': 'vintage graphic tee', 'size': None, 'max_price': 30.0}
[2] search_listings (via MCP)
      in:  {'description': 'vintage graphic tee', 'size': None, 'max_price': 30.0}
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
[3] select item
      in:  10 results
      out: Y2K Baby Tee — Butterfly Print ($18.0, depop)
[4] suggest_outfit
      in:  Y2K Baby Tee — Butterfly Print, wardrobe of 10 items
      out: **Outfit 1: Casual Y2K Streetwear** Pair the Y2K Baby Tee with your baggy straight-leg jeans for a classic ear…
[5] create_fit_card
      in:  Y2K Baby Tee — Butterfly Print
      out: scored this butterfly baby tee for just $18.00 on depop and i am officially living my 2000s pop star dream. th…
```

**Empty search**

```
$ python app.py ask 'designer ballgown size XXS under $5' --trace
[1] parse query
      in:  designer ballgown size XXS under $5
      out: {'description': 'designer ballgown', 'size': 'XXS', 'max_price': 5.0}
[2] search_listings (via MCP)
      in:  {'description': 'designer ballgown', 'size': 'XXS', 'max_price': 5.0}
      out: [] (empty)
[3] branch
      →    search returned nothing -> stopping, suggest_outfit not called
```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->

I registered `search_listings` in `mcp_server.py` and changed one line in `agent.py::run_agent` from `search_listings(**session["parsed"])` to `call_tool("search_listings", session["parsed"])`. Nothing behaved differently: I compared the MCP result with the direct call for `'graphic tee'` under $30 and the two lists were equal, and an impossible query still came back as `[]`. Both traces above show it as `search_listings (via MCP)`.

**The three failure modes**

- *Empty search* (`'designer ballgown size XXS under $5'`): the agent stopped at step 3 without calling `suggest_outfit`, and said: "No listings matched keywords 'designer ballgown', size XXS, under $5. Try raising the price limit, dropping the size, or using broader keywords." No handler was needed, this branch already worked.
- *Empty wardrobe* (`python app.py ask 'denim jacket under $50' --empty-wardrobe`): `suggest_outfit` returned general styling advice ("Here are two ways to style your Wrangler jacket: 1. Casual Contrast ... 2. Playful Texture ...") and the fit card was written from it. No crash and no empty string, so no handler was needed.
- *Model unavailable* (bad `GEMINI_API_KEY` set for one run, on a query I hadn't asked before): the first version printed the model error twice with duplicated advice, because my handler added its own sentence after the adapter's. I changed the handler in `agent.py::run_agent` to catch `ModelUnavailable` and say: "I found an item but can't write the outfit or fit card because the model couldn't be reached. The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com." The real service also returned a `503 UNAVAILABLE` (high demand) during testing, and the same handler reported it, so that was an unplanned second test of the same path.



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:** One prompt, in `tools.py::create_fit_card`. Before: "Write a 2-4 sentence caption ...". After: "Write a caption ... It must be exactly three sentences, and every sentence must end with a period, exclamation mark or question mark (no run-on single sentence, no trailing fragment)." Everything else in the prompt (mention the item, its price and its platform once each, sound like a real post, output only the caption) is unchanged. Nothing else changed between the two runs: same agent, same provider and model (`AI201_PROVIDER=claude`, `AI201_MODEL=haiku`), same scenarios, same caching-off setting.

**Which failure it was meant to fix:** Criterion 4b, the only try that failed in the `before` run. In try 4 of the fit-card scenario the model wrote one long sentence with no full stop. Place: the model's output. Mechanism: "2-4 sentences" is a range the model is free to ignore and nothing in the prompt said what a sentence boundary looks like, so a caption written as a single flowing line was allowed. It was also the criterion that scored exactly at its target (4 of 5), so one more miss would have turned it MISSED.

### Run Log — Before

Same numbers as the run log above (`results/run_2026-10-13_2336_before.md`, plus `results/run_2026-10-13_2355_before_c5.md` for row 5), repeated here so the two tables sit side by side.

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Matching query completes all three tools and returns a fit card | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Impossible query stops before `suggest_outfit`, message names what to change | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. `selected_item` id equals the id that reached `suggest_outfit` and `create_fit_card` | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4a. Fit card contains the item's price and platform | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4b. Fit card is 2 to 4 sentences | 4 of 5 | PASS | PASS | PASS | FAIL | PASS | MET (4/5) |
| 5. Every search result is within `max_price` and matches `size` | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

### Run Log — After

`python run_eval.py --label after`, raw output in `results/run_2026-10-14_0009_after.md`.

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Matching query completes all three tools and returns a fit card | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Impossible query stops before `suggest_outfit`, message names what to change | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. `selected_item` id equals the id that reached `suggest_outfit` and `create_fit_card` | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4a. Fit card contains the item's price and platform | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4b. Fit card is 2 to 4 sentences | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Every search result is within `max_price` and matches `size` | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

I judged the after run the same way as the before run (same checks, same by-hand counting; I also ran both files through one small script so the sentence count is the same rule for both: split on `.`, `!`, `?` and count the pieces that contain a word).

**Did it help, and how do I know:** Only on the one row it was aimed at, and only slightly. 4b went from 4 of 5 to 5 of 5: all five after-run cards are three sentences, each ending in punctuation (before: sentence counts 3, 3, 3, 1, 3). Nothing else moved, and nothing got worse: 4a still has the price and platform in all five, and the other rows are unchanged. I also read the five new cards and they still sound like posts and still differ from each other, so forcing "exactly three sentences" did not flatten them (one ends a sentence with "?" where a statement would read better: "i'm obsessed?").

The honest limit is the sample. One failure in five before and none in five after cannot tell a fix from luck: if the real miss rate had been 20% and the change did nothing, five clean tries would still come up about a third of the time (0.8^5 = 0.33). The prompt gives a concrete reason to expect the improvement (it now says what a sentence ends with, which is the thing the failing card lacked), but I haven't shown it with these numbers. To show it I'd need something like 20 tries on this scenario, not 5.

---

## What's Still Broken

No criterion is MISSED on the run I'm submitting (Haiku, `before` and `after`), so there is nothing "missed" to fix. That doesn't mean it works. This is what I know is still wrong, and why I stopped.

1. **It fails on the default model (the biggest one).** On `gemini-3.5-flash-lite` the same agent failed most of the time in the evening of 2026-10-13: 503 or "Server disconnected" on 12 to 25 of the model-using tries per run, and `gemini-3.5-flash` then hit a daily-quota 429. Read against my targets that would be MISSED on criteria 1, 3 and 4. The agent handles it gracefully (the Milestone 2 handler prints a clear message, nothing crashes), but it still gives the user nothing. What I'd do: make `generate.py` retry a `503` the way it retries a `429`, with a short backoff. Why I stopped: the quota on my key was used up, so I couldn't test a retry honestly, and putting it in would have changed the model layer between `before` and `after`, which the improvement rule says to avoid.
2. **Search relevance isn't measured, and it's weak.** `search_listings` ranks by keyword overlap only. `'graphic tee'` under $30 returns a mesh long-sleeve top and a navy crewneck sweatshirt (its own description says "No graphics"), and a user who sees them would call the search broken. Criterion 1 can't catch it because it only checks that a fit card came back. What I'd do: weight matches in `category` and `style_tags` above matches in free text, and add a criterion like "the selected item's tags match the query". Why I stopped: that is a new criterion plus a tool change, which is more than the one improvement allowed.
3. **Criterion 3 is measured by the trace, which can't really disagree with the session.** The `id` shown at each step comes from `session["selected_item"]`, so the check passes unless someone rewrites the loop. A spy on the arguments `suggest_outfit` actually receives would be a real test. I did it once by hand (`received is session["selected_item"]` was `True`) but didn't put it into `run_eval.py`. Why I stopped: it doesn't change any verdict today.
4. **The 4b improvement is not proven.** Four of five before, five of five after is within what luck can produce (about a one in three chance of five clean tries even if nothing changed). I'd run 20 tries on that one scenario. Why I stopped: each try costs two model calls and I'd already burned through a lot of quota on the failed runs.
5. **The query parser is plain string splitting.** It understands `$30`, `under 30` and `size M`. It can't handle "under thirty dollars", "S or M", or a size written the way the data writes it ("W30 L30", "US 8.5") unless the user types it exactly. Why I stopped: no criterion tests parsing, and the scenarios I wrote all use the supported forms, so I'd be fixing something my test can't see.
6. **My Haiku runs aren't reproducible by anyone else.** The `AI201_PROVIDER=claude` path shells out to the `claude` command on my machine and uses my own plan, with no temperature setting and about ten seconds per call. It is off unless the environment variable is set, and the default is still Gemini, but a grader running `python run_eval.py` with only a Gemini key will get the Gemini behaviour, not the numbers in this README.

**On the MCP move.** I registered `search_listings` in `mcp_server.py` and changed one line in `agent.py::run_agent` from `search_listings(**session["parsed"])` to `call_tool("search_listings", session["parsed"])`. Nothing behaved differently: the MCP result was equal to the direct call for `'graphic tee'` under $30, and an impossible query still came back as `[]`. What I did notice is the cost: `mcp_client.call_tool` starts and stops the server on every call, so each search now spawns a new process. For one search per run that's fine, but it is a seam I would not put inside a loop that searches repeatedly.

<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

## Model availability problem (Unit 4, Milestone 3)

I could not get a clean `before` run on the default model, so I want this on record.

- **What happened.** `python run_eval.py --label before` against `gemini-3.5-flash-lite` came back mostly with `503 UNAVAILABLE` ("This model is currently experiencing high demand") and `Server disconnected without sending a response`. I ran it four times and saved all four files in `results/`: 12, 14, 20 and 25 of the model-using tries failed (the first run was `run_2026-10-13_0843_before.md`, the last Gemini one `run_2026-10-13_2141_before.md`: every try that needed the model failed). Switching to a new API key changed nothing.
- **What I tried.** `gemini-2.5-flash` does not resolve for my key. `gemini-3.5-flash` answered a small prompt, but the full run (`run_2026-10-13_2318_before.md`) hit 502/503 on 10 tries and then `429` ("Still rate limited after 5 attempts") on 12 more, which looks like the daily quota for that key.
- **What I did.** I added an optional provider to `generate.py` (`AI201_PROVIDER=claude`, with `AI201_MODEL=haiku`), which sends the prompt through the local `claude -p` command instead of the Gemini API. The default is still Gemini and nothing changes unless that variable is set. All 30 tries in `run_2026-10-13_2336_before.md` completed. Anthropic's alias `haiku` resolves to whichever Haiku the CLI currently maps it to (Haiku 4.5 at the time of writing); there is no Haiku 5.5.
- **What this changes about my results.** My `before` numbers describe the agent running on Haiku, not on the model the course gives out. `claude -p` has no temperature setting, so `config.TEMPERATURE` does not apply to these runs, and token counts are not recorded. My "after" run must use the same provider and model, or it won't be comparable.
- **What it didn't fix.** The agent itself has no retry for `503`; `generate.py` only retries `429`. A real user on the default model would have seen the "model couldn't be reached" message from the Milestone 2 handler most of the time that evening.

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**

---

## Capstone

**What This Extends**

This extends FitFindr, my Unit 3–4 agent (parse the query → `search_listings` over MCP → `suggest_outfit` → `create_fit_card`). The agent already works when the model answers. What's new this unit is the model layer's behaviour when the model *doesn't* answer cleanly, plus a run path (`python serve.py`) and a structured log around every request.

The reason for picking this one is in my own Unit 4 write-up: on the default model (`gemini-3.5-flash-lite`) 12 to 25 of 30 tries failed with `503 UNAVAILABLE` or "Server disconnected", and `generate.py::generate` only retried `429`. So the first transient error ended the run, and the user got an apology instead of a fit card.

**The Shape**

Shape B — harden against failure. Everything that's new lives in the model layer (`generate.py`) and the HTTP front door (`serve.py`):

- Retry transient model errors (`500`/`502`/`503`/`504`, "unavailable", "overloaded", "Server disconnected", timeouts) with the same backoff `429` already gets. Errors that won't fix themselves (a bad key, a model name that doesn't resolve) still fail fast.
- A per-call timeout, so a hung request becomes a retry instead of a hang.
- An empty reply from the model counts as a failure and gets retried, so it can't reach the fit card as an empty string.
- When retries run out, the agent returns its readable "model couldn't be reached" message, not a crash and not a `500`.
- `POST /ask` rejects malformed input (no JSON, a missing or non-string `query`, an oversized one) with a `400`, never a `500`.
- A fault-injection switch (`AI201_FAULT`, off unless set) so I can trigger each failure on purpose and test the bad path instead of waiting for Gemini to have a bad night.

Run path, structured logging and the cost measurement come with every shape and are part of this too.

*Out of scope, on purpose:*

- **Search relevance.** `search_listings` still ranks by keyword overlap only. I know it's weak ("What's Still Broken" #2 from Unit 4), but changing it is shape C, not B.
- **The Claude provider.** The `AI201_PROVIDER=claude` path from Unit 4 stays as it is. I'm not hardening it or using it for this unit's runs; all capstone runs use Gemini, the default.
- **Hosting and a UI.** I'm taking Path B (local with logs). No host, no web page, no change to the MCP setup or to `serve.py`'s one-request-at-a-time lock.

*Stretch (declared before starting):* a latency breakdown of where one run's time goes. Optional, and only if the required parts are done first.

**Running It**

Path B, local with logs. `python serve.py` starts FitFindr as a local HTTP server on port 5000, and every `POST /ask` appends one record to `logs/runs.jsonl`. The exact command, the Python version, the pinned dependencies and the `.env` it needs are in [RUNNING.md](RUNNING.md), under "Capstone run path". There's no model file: the model is called over the network and the server uses about 98 MB (measured with `tasklist` while it was serving).

I tested RUNNING.md on myself by cloning the repo into a fresh folder, making a new 3.12 venv, `pip install -r requirements.txt`, copying `.env.example` to `.env` with my key, `python test.py` (10 passed), and `python serve.py` on port 5055. One request through `bench.py` came back `200` with a fit card. It didn't fail the first time, which I expected it to. What I did find while measuring is that `localhost` on Windows costs about 2 s per request (it tries IPv6 first): a `400` that took 0 ms inside the server took 2.1 s at the client. So RUNNING.md and `bench.py` both use `127.0.0.1`.

I didn't try a host. My system has no local model and would fit in 512 MB, so it isn't a memory problem; I took Path B because it's worth the same and lets me use `AI201_FAULT` to restart the server in different failure modes on my own machine.

**Instrumentation**

Every `/ask` request writes exactly one JSON line to `logs/runs.jsonl` (`serve.py::ask`, written by `serve.py::_write_log`), including requests that are rejected (`400`) or crash (`500`). A failure to write the log is printed and never fails the request. Fields:

| Field | What it holds |
|---|---|
| `ts` | UTC time the request arrived |
| `input` | the query; for a body that doesn't parse, the first 200 characters of the raw body |
| `http_status` | what the caller got: 200, 400 or 500 |
| `outcome` | `ok`, `no_match` (search found nothing), `model_unavailable` (an item was found but the model failed), `bad_input` (400), `crash` (500) |
| `error` | the message the caller saw, if any |
| `n_results`, `item_id` | how many listings search returned and which one was picked |
| `fit_card_chars` | length of the fit card (0 = none) |
| `duration_ms` | server-side time for the whole request |
| `model_calls`, `retries` | attempts made to the model during this request, and how many were retries (from `generate.call_count()` / `generate.retry_count()`, taken inside the request lock so they belong to this request only) |
| `prompt_tokens`, `output_tokens` | tokens Gemini reported for this request (`usage_metadata`) |
| `fault` | the `AI201_FAULT` value active, or `null` for a real run |
| `model` | model name from `config.MODEL` |

The first 15 records, pasted from `logs/runs.jsonl`. The first ten are ten normal requests (five example queries, twice each, cache off). Then a query that matches nothing, two malformed bodies, one request with the server started under `AI201_FAULT=503:99` (the model failed on every attempt), and the run from the clean-clone test:

```
{"ts": "2026-11-16T06:28:18.174+00:00", "input": "vintage graphic tee under $30", "http_status": 200, "outcome": "ok", "error": null, "n_results": 10, "item_id": "lst_002", "fit_card_chars": 293, "duration_ms": 13421, "model_calls": 2, "retries": 0, "prompt_tokens": 521, "output_tokens": 209, "fault": null, "model": "gemini-3.5-flash-lite"}
{"ts": "2026-11-16T06:28:33.640+00:00", "input": "vintage graphic tee under $30", "http_status": 200, "outcome": "ok", "error": null, "n_results": 10, "item_id": "lst_002", "fit_card_chars": 227, "duration_ms": 20576, "model_calls": 2, "retries": 0, "prompt_tokens": 518, "output_tokens": 191, "fault": null, "model": "gemini-3.5-flash-lite"}
{"ts": "2026-11-16T06:28:56.298+00:00", "input": "90s track jacket in size M", "http_status": 200, "outcome": "ok", "error": null, "n_results": 3, "item_id": "lst_004", "fit_card_chars": 262, "duration_ms": 13649, "model_calls": 2, "retries": 0, "prompt_tokens": 490, "output_tokens": 170, "fault": null, "model": "gemini-3.5-flash-lite"}
{"ts": "2026-11-16T06:29:12.032+00:00", "input": "90s track jacket in size M", "http_status": 200, "outcome": "ok", "error": null, "n_results": 3, "item_id": "lst_004", "fit_card_chars": 292, "duration_ms": 14142, "model_calls": 2, "retries": 0, "prompt_tokens": 500, "output_tokens": 193, "fault": null, "model": "gemini-3.5-flash-lite"}
{"ts": "2026-11-16T06:29:28.250+00:00", "input": "silk slip dress in midi length under $40", "http_status": 200, "outcome": "ok", "error": null, "n_results": 2, "item_id": "lst_013", "fit_card_chars": 274, "duration_ms": 3717, "model_calls": 2, "retries": 0, "prompt_tokens": 509, "output_tokens": 180, "fault": null, "model": "gemini-3.5-flash-lite"}
{"ts": "2026-11-16T06:29:34.039+00:00", "input": "silk slip dress in midi length under $40", "http_status": 200, "outcome": "ok", "error": null, "n_results": 2, "item_id": "lst_013", "fit_card_chars": 261, "duration_ms": 9049, "model_calls": 2, "retries": 0, "prompt_tokens": 522, "output_tokens": 191, "fault": null, "model": "gemini-3.5-flash-lite"}
{"ts": "2026-11-16T06:29:45.141+00:00", "input": "platform sneakers size 8", "http_status": 200, "outcome": "ok", "error": null, "n_results": 1, "item_id": "lst_019", "fit_card_chars": 278, "duration_ms": 3956, "model_calls": 2, "retries": 0, "prompt_tokens": 536, "output_tokens": 213, "fault": null, "model": "gemini-3.5-flash-lite"}
{"ts": "2026-11-16T06:29:51.175+00:00", "input": "platform sneakers size 8", "http_status": 200, "outcome": "ok", "error": null, "n_results": 1, "item_id": "lst_019", "fit_card_chars": 260, "duration_ms": 6514, "model_calls": 2, "retries": 0, "prompt_tokens": 553, "output_tokens": 228, "fault": null, "model": "gemini-3.5-flash-lite"}
{"ts": "2026-11-16T06:29:59.751+00:00", "input": "denim jacket under $50", "http_status": 200, "outcome": "ok", "error": null, "n_results": 6, "item_id": "lst_007", "fit_card_chars": 311, "duration_ms": 6300, "model_calls": 2, "retries": 0, "prompt_tokens": 481, "output_tokens": 169, "fault": null, "model": "gemini-3.5-flash-lite"}
{"ts": "2026-11-16T06:30:08.102+00:00", "input": "denim jacket under $50", "http_status": 200, "outcome": "ok", "error": null, "n_results": 6, "item_id": "lst_007", "fit_card_chars": 325, "duration_ms": 6624, "model_calls": 2, "retries": 0, "prompt_tokens": 488, "output_tokens": 178, "fault": null, "model": "gemini-3.5-flash-lite"}
{"ts": "2026-11-16T06:30:22.874+00:00", "input": "designer ballgown size XXS under $5", "http_status": 200, "outcome": "no_match", "error": "No listings matched keywords 'designer ballgown', size XXS, under $5. Try raising the price limit, dropping the size, or using broader keywords.", "n_results": 0, "item_id": null, "fit_card_chars": 0, "duration_ms": 1472, "model_calls": 0, "retries": 0, "prompt_tokens": 0, "output_tokens": 0, "fault": null, "model": "gemini-3.5-flash-lite"}
{"ts": "2026-11-16T06:30:26.824+00:00", "input": "[1, 2]", "http_status": 400, "outcome": "bad_input", "error": "Send a JSON object with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "n_results": null, "item_id": null, "fit_card_chars": 0, "duration_ms": 0, "model_calls": 0, "retries": 0, "prompt_tokens": 0, "output_tokens": 0, "fault": null, "model": "gemini-3.5-flash-lite"}
{"ts": "2026-11-16T06:30:28.901+00:00", "input": "{\"query\": 42}", "http_status": 400, "outcome": "bad_input", "error": "'query' must be a non-empty string, e.g. {\"query\": \"vintage graphic tee under $30\"}", "n_results": null, "item_id": null, "fit_card_chars": 0, "duration_ms": 0, "model_calls": 0, "retries": 0, "prompt_tokens": 0, "output_tokens": 0, "fault": null, "model": "gemini-3.5-flash-lite"}
{"ts": "2026-11-16T06:30:44.985+00:00", "input": "denim jacket under $50", "http_status": 200, "outcome": "model_unavailable", "error": "I found an item but can't write the outfit or fit card because the model couldn't be reached. The model kept failing after 5 attempts, so I stopped trying. Wait a minute and try again. Last error: 503 UNAVAILABLE. The model is overloaded. (injected by AI201_FAULT)", "n_results": 6, "item_id": "lst_007", "fit_card_chars": 0, "duration_ms": 20647, "model_calls": 5, "retries": 4, "prompt_tokens": 0, "output_tokens": 0, "fault": "503:99", "model": "gemini-3.5-flash-lite"}
{"ts": "2026-11-16T06:34:13.757+00:00", "input": "platform sneakers size 8", "http_status": 200, "outcome": "ok", "error": null, "n_results": 1, "item_id": "lst_019", "fit_card_chars": 274, "duration_ms": 19643, "model_calls": 2, "retries": 0, "prompt_tokens": 521, "output_tokens": 195, "fault": null, "model": "gemini-3.5-flash-lite"}
```

The failed runs are lines 11–14. Line 14 is the one I most wanted on record: the item was found (`n_results: 6`, `item_id: lst_007`), five model attempts were made with four retries between them, and the user got a sentence, not a crash, after 20.6 s. Without the log that request would only show up as "no fit card".

**What It Costs**

*Measured:* I ran ten normal requests with the cache off (`AI201_CACHE=0`), the first ten lines above, and averaged the token counts the server logged. Those counts come from Gemini's own `usage_metadata` on each response, summed per request by `generate.py::_record_tokens`.

| | Average per run (10 runs) | Range |
|---|---|---|
| Prompt tokens | 511.8 | 481–553 |
| Output tokens | 192.2 | 169–228 |
| Model calls | 2 | 2–2 |
| Time (server side) | 9.8 s (median 7.8 s) | 3.7–20.6 s |

*In money:* on my key this is the free tier, so what I actually paid was $0. At the paid rate for `gemini-3.5-flash-lite` ($0.30 per 1M input tokens, $2.50 per 1M output tokens; I took these from aggregator sites, not Google's own page):

- input: 511.8 × $0.30 / 1,000,000 = $0.000154
- output: 192.2 × $2.50 / 1,000,000 = $0.000481
- **one run ≈ $0.00063**, about 6/100 of a cent. Output is three quarters of it.

*For a hundred people a day,* each asking once: 100 × $0.00063 = **$0.063 a day**, about $1.90 a month (× 30). On the free tier the money is $0, and the limit is pace instead: 15 requests a minute is about 7 runs a minute, so 100 people a day is fine but 100 people in the same minute is not.

*What this number doesn't include:* a no-match query costs nothing (no model calls, line 11), and a run with retries costs no more in tokens, because a failed attempt returns no tokens (line 14 shows 0). It costs time instead: 20.6 s for that one. Gemini bills "thinking" tokens as output, and `_record_tokens` reads only `candidates_token_count`, so I checked that I'm not missing any: on a direct call `thoughts_token_count` came back `None` and `total_token_count` equalled prompt + candidates (8 + 7 = 15). This model isn't thinking by default, so the count above is the whole bill.

*Checked against the test runs.* The 60 normal-path requests in the six trials (C5, before and after) average 519.2 prompt + 201.8 output = 721 tokens (range 634–927), which is **$0.00066 a run**. That's within 5% of the ten-run number above, so I'm keeping $0.00063 to $0.00066 as the per-run cost and **about $0.07 a day for 100 people** (100 × $0.00066 = $0.066). The time cost is less tidy: the median request took 3.5 s, but 7 of those 60 took over 15 s, almost all because of the free tier's 15-a-minute pacing (see the diagnosis below).

**Run Log and Verdicts**

Three trials of all five criteria from `criteria.md` ("Capstone criteria"), with nothing changed between them: `python capstone_trials.py --label before`. Each trial starts `serve.py` three times (under `AI201_FAULT=503:2`, under `503:99`, and with no fault), drives it with `bench.py`, and counts from the log lines that trial added. Raw output, including every log line, is in `results/capstone_before_trial1.txt`, `..._trial2.txt` and `..._trial3.txt`, with the counts in `results/capstone_before_summary.md`. Cache off, real Gemini (`gemini-3.5-flash-lite`), 72 requests in all.

| Criterion | Target (per trial) | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| C1. Injected 503×2 per call is recovered: fit card, `retries`=4, under 30 s | 5 of 5 | 4/5 | 4/5 | 4/5 | MISSED |
| C2. Model never answers: 200, "couldn't be reached", no card, `model_unavailable`, under 20 s | 3 of 3 | 2/3 | 3/3 | 3/3 | MISSED |
| C3. Six malformed bodies get 400, none get 500 | 6 of 6 | 6/6 | 6/6 | 6/6 | MET |
| C4. One complete log record per request, status matches the client | 24 of 24 | 24/24 | 24/24 | 24/24 | MET |
| C5. Normal path: fit card 10/10, ≥9/10 under 15 s, avg tokens ≤ 1,000 | all three parts | 10/10, 9/10, 723 | 10/10, 9/10, 718 | 10/10, 9/10, 713 | MET |

*How each was read.* C1: every one of the 15 requests recovered and got a fit card with exactly `retries`=4, so the retry itself never failed. The miss is time: the **third** request of every trial took 45.1, 48.0 and 47.7 s. C2: every request got the right answer (200, the "couldn't be reached" sentence, no card, `model_unavailable`). The miss is time again, the **first** request of trial 1 at 22.8 s (the other eight were 16.1–18.7 s). The target has to hold in every trial, so 2/3 in one trial is MISSED. C5 met all three parts, but its 9/10 is exactly at the limit in every trial, and the one slow request is the **eighth** every time (40.0, 39.4, 24.1 s). The misses (and C5's near-miss) all sit at fixed positions in the sequence, not at random ones. That is the first thing I'll look at in the diagnosis.

**Real output, one trial per criterion** (all from `results/capstone_before_trial1.txt`)

*C1 — `bench.py` against `serve.py::ask` → `agent.py::run_agent` → `generate.py::generate` with `AI201_FAULT=503:2`:*

```
$ AI201_FAULT=503:2 python bench.py 'denim jacket under $50' (x5)
200   14.95s  'denim jacket under $50'                     #1  fit card 313 chars, item lst_007
200   11.17s  'denim jacket under $50'                     #1  fit card 343 chars, item lst_007
200   45.11s  'denim jacket under $50'                     #1  fit card 351 chars, item lst_007
200   10.06s  'denim jacket under $50'                     #1  fit card 359 chars, item lst_007
200   12.62s  'denim jacket under $50'                     #1  fit card 311 chars, item lst_007

{"ts": "2026-11-16T06:39:09.283+00:00", "input": "denim jacket under $50", "http_status": 200, "outcome": "ok", "error": null, "n_results": 6, "item_id": "lst_007", "fit_card_chars": 351, "duration_ms": 45089, "model_calls": 6, "retries": 4, "prompt_tokens": 494, "output_tokens": 182, "fault": "503:2", "model": "gemini-3.5-flash-lite"}
```

*C2 — same path, `AI201_FAULT=503:99`; the sentence comes from `agent.py::run_agent`'s `ModelUnavailable` handler:*

```
$ AI201_FAULT=503:99 python bench.py 'denim jacket under $50' (x3)
200   22.83s  'denim jacket under $50'                     #1  error: I found an item but can't write the outfit or fit card because the model couldn't be reach
200   16.35s  'denim jacket under $50'                     #1  error: I found an item but can't write the outfit or fit card because the model couldn't be reach
200   16.09s  'denim jacket under $50'                     #1  error: I found an item but can't write the outfit or fit card because the model couldn't be reach

{"ts": "2026-11-16T06:40:18.453+00:00", "input": "denim jacket under $50", "http_status": 200, "outcome": "model_unavailable", "error": "I found an item but can't write the outfit or fit card because the model couldn't be reached. The model kept failing after 5 attempts, so I stopped trying. Wait a minute and try again. Last error: 503 UNAVAILABLE. The model is overloaded. (injected by AI201_FAULT)", "n_results": 6, "item_id": "lst_007", "fit_card_chars": 0, "duration_ms": 22755, "model_calls": 5, "retries": 4, "prompt_tokens": 0, "output_tokens": 0, "fault": "503:99", "model": "gemini-3.5-flash-lite"}
```

*C3 — `serve.py::_ask` input checks, no model involved:*

```
$ python bench.py --raw '' hello '[1, 2]' '{"query": 42}' '{"query": "   "}' '{"query": "aaaa...(400 chars)"}'
400    0.05s  ''                                           #1  error: Send a JSON object with a 'query' field, e.g. {"query": "vintage graphic tee under $30"}
400    0.01s  'hello'                                      #1  error: Send a JSON object with a 'query' field, e.g. {"query": "vintage graphic tee under $30"}
400    0.00s  '[1, 2]'                                     #1  error: Send a JSON object with a 'query' field, e.g. {"query": "vintage graphic tee under $30"}
400    0.01s  '{"query": 42}'                              #1  error: 'query' must be a non-empty string, e.g. {"query": "vintage graphic tee under $30"}
400    0.02s  '{"query": "   "}'                           #1  error: 'query' must be a non-empty string, e.g. {"query": "vintage graphic tee under $30"}
400    0.00s  '{"query": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaa'   #1  error: 'query' is 400 characters; keep it under 300. Describe the item, its size and a price.
```

*C4 — `serve.py::_write_log`; the count line is from `capstone_trials.py::score`, and one of the six `bad_input` records shows a rejected request is still logged:*

```
C4: 24 of 24  24 new lines for 24 requests, 24 complete, statuses match: True

{"ts": "2026-11-16T06:41:14.901+00:00", "input": "", "http_status": 400, "outcome": "bad_input", "error": "Send a JSON object with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "n_results": null, "item_id": null, "fit_card_chars": 0, "duration_ms": 0, "model_calls": 0, "retries": 0, "prompt_tokens": 0, "output_tokens": 0, "fault": null, "model": "gemini-3.5-flash-lite"}
```

*C5 — the normal path, no fault (`(fit_card_chars, duration_ms, tokens)` per request from `capstone_trials.py::score`):*

```
$ python bench.py -n 2 'vintage graphic tee under $30' '90s track jacket in size M' 'silk slip dress in midi length under $40' 'platform sneakers size 8' 'denim jacket under $50'
200    5.26s  'vintage graphic tee under $30'              #1  fit card 285 chars, item lst_002
200    4.08s  'vintage graphic tee under $30'              #2  fit card 283 chars, item lst_002
200    3.08s  '90s track jacket in size M'                 #1  fit card 261 chars, item lst_004
200    2.60s  '90s track jacket in size M'                 #2  fit card 212 chars, item lst_004
200    3.13s  'silk slip dress in midi length under $40'   #1  fit card 328 chars, item lst_013
200    3.73s  'silk slip dress in midi length under $40'   #2  fit card 283 chars, item lst_013
200    2.91s  'platform sneakers size 8'                   #1  fit card 297 chars, item lst_019
200   40.04s  'platform sneakers size 8'                   #2  fit card 352 chars, item lst_019
200    3.61s  'denim jacket under $50'                     #1  fit card 347 chars, item lst_007
200    2.98s  'denim jacket under $50'                     #2  fit card 325 chars, item lst_007

C5: (10, 9, 723) of 10  [(285, 5217, 729), (283, 4079, 783), (261, 3079, 647), (212, 2575, 634), (328, 3112, 771), (283, 3712, 787), (297, 2894, 748), (352, 40024, 719), (347, 3583, 721), (325, 2964, 690)]
```

*Diagnosis of each miss*

**C1 (MISSED, 4/5 in all three trials).** Every request recovered; the one that failed was always the third, at 45–48 s. Stage: `generate.py::_wait_for_slot`, the 15-requests-a-minute pacer that came with the starter. Mechanism: `generate()` appends to `_call_times` *before* my fault injection fires, so every fake 503 takes a pacing slot even though it never reaches Google. Under `503:2` one request is 2 model calls × 3 attempts = 6 slots, so requests 1 and 2 use 12 of the 15, and request 3's second call finds the minute full and sleeps until the oldest slot is 60 s old. I confirmed it rather than inferring it. I re-ran the first three C1 requests with the server's stderr captured (the trial script discards it), and the pacer's own message appears in request 3, after exactly 15 attempts:

```
11:   [retry] transient error: '503 UNAVAILABLE. The model is overloaded. (injected by AI201_FAULT)'. Waiting 2s (attempt 2 of 5).
12:   [rate limit] 15 requests used this minute. Waiting 26s. This is normal.
13:   [retry] transient error: '503 UNAVAILABLE. The model is overloaded. (injected by AI201_FAULT)'. Waiting 1s (attempt 1 of 5).
```

The real-world version of this isn't fake: a real 503 *does* reach Google, so with real failures every retry spends real per-minute quota too. The retry triples the slots a request needs exactly when the service is struggling. My 30 s target assumed retries cost only backoff time; they also cost pacing time, and on the free tier's 15 a minute that's the bigger of the two.

**C2 (MISSED, 2/3 in trial 1).** Only the first request after the server started was over 20 s (22.8 s; the first requests of trials 2 and 3 were also the slowest, at 18.7 and 18.2 s, against 16.1–16.3 s for the rest). Stage: the first model call in a fresh server process. Mechanism: `generate.py::_get_client` imports `google.genai` and builds the client lazily, on the first call, so the first user after every start pays that one-time cost inside their request. I timed it in a fresh process three times: **5.7, 11.1 and 9.2 s** for the import and client (Windows, cold disk cache; it varies a lot). On top of a give-up path that is already 15 s of fixed backoff sleep (1 + 2 + 4 + 8 s), that leaves only about 4 s of headroom under 20 s, and a cold import can eat all of it.

**C5 (MET, but at the limit).** Not a miss, but it has the same cause as C1: the slow request was the 8th of 10 in every trial (40.0, 39.4, 24.1 s). Two calls a request means request 8's second call is the 16th in the minute. The pacer is doing its job here (15 is the real free-tier limit), so this is the cost of the quota, not a bug. I set "9 of 10" thinking the one slow run in Milestone 3 was Gemini's variance; it was mostly this.

*Pattern.* Two of the three slow-request problems (C1 and C5) are one problem: the pacer's 60-second window, which makes a fixed request in each sequence wait 25–35 s. It shows up at a fixed position, not at random, and that's how I found it. C2 is a separate, smaller problem (cold start). Nothing failed on correctness: in 72 requests every fit card that should have come back came back, every failure gave the right sentence, every bad body got a 400, and every request was logged.

*One more thing the run log shows:* one real Gemini 503 ("This model is currently experiencing high demand") during the diagnosis re-run was retried and recovered (`[retry] transient error: "503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently exp". Waiting 4s (attempt 3 of 5`), and another real transient error recovered in the after-run (below). Before this unit, both of those users would have got an apology.

**The Improvement**

*What I changed.* One change, in `serve.py`: the Gemini client is built when the server starts (`generate._get_client()` at module load, with its time printed), instead of inside the first request. No API call is made at start-up, and if it fails (no key) the server still starts and the first request reports the error the way it did before. Nothing else changed between the two runs: same criteria, same `capstone_trials.py`, same model, cache off.

*Why this one.* It follows the C2 diagnosis: the miss was a one-time import cost landing on the first user's request. I didn't pick the C1 fix (stop fake attempts from taking pacing slots) because it changes only what my test switch costs, not anything a real user experiences. With real 503s the slots are really spent. Under the server's start-up message the cost moved where I wanted it: `[serve] model client ready in 5.7s` is printed before the server accepts requests.

*Run log, before* (from `results/capstone_before_*`, same as above):

| Criterion | Target (per trial) | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| C1. Injected 503×2 per call is recovered: fit card, `retries`=4, under 30 s | 5 of 5 | 4/5 | 4/5 | 4/5 | MISSED |
| C2. Model never answers: 200, "couldn't be reached", no card, `model_unavailable`, under 20 s | 3 of 3 | 2/3 | 3/3 | 3/3 | MISSED |
| C3. Six malformed bodies get 400, none get 500 | 6 of 6 | 6/6 | 6/6 | 6/6 | MET |
| C4. One complete log record per request, status matches the client | 24 of 24 | 24/24 | 24/24 | 24/24 | MET |
| C5. Normal path: fit card 10/10, ≥9/10 under 15 s, avg tokens ≤ 1,000 | all three parts | 10/10, 9/10, 723 | 10/10, 9/10, 718 | 10/10, 9/10, 713 | MET |

*Run log, after* (`python capstone_trials.py --label after`; raw output in `results/capstone_after_trial1.txt` to `..._trial3.txt`, counts in `results/capstone_after_summary.md`):

| Criterion | Target (per trial) | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| C1. Injected 503×2 per call is recovered: fit card, `retries`=4, under 30 s | 5 of 5 | 4/5 | 4/5 | 4/5 | MISSED |
| C2. Model never answers: 200, "couldn't be reached", no card, `model_unavailable`, under 20 s | 3 of 3 | 3/3 | 3/3 | 3/3 | MET |
| C3. Six malformed bodies get 400, none get 500 | 6 of 6 | 6/6 | 6/6 | 6/6 | MET |
| C4. One complete log record per request, status matches the client | 24 of 24 | 24/24 | 24/24 | 24/24 | MET |
| C5. Normal path: fit card 10/10, ≥9/10 under 15 s, avg tokens ≤ 1,000 | all three parts | 10/10, 9/10, 716 | 10/10, **8/10**, 713 | 10/10, 9/10, 744 | MISSED |

*Did it help?* On the criterion it was aimed at, yes: C2 went from MISSED to MET. The first give-up answer after a start now takes 16.7, 16.0 and 18.2 s (before: 22.8, 18.7, 18.2), and all nine C2 requests were under 20 s. Honestly, the margin is still thin. Trial 3's first request was 18.2 s both before and after, so the warm-up didn't remove every first-request cost (the first MCP search still spawns a fresh process). The 15 s of backoff sleep, which this change doesn't touch, is most of the time.

C1 didn't move, as expected: the same request (the third) hit the pacer in every trial (42.8, 47.1, 47.2 s).

C5 got worse, from MET to MISSED, but not because of this change. Trial 2 had two requests over 15 s. One was the 8th again (21.0 s, the pacer), and the other was the 10th, at 55.7 s. Its log record shows why:

```
07:02:06 denim jacket under $50         55675 calls 3 retries 1
```

No fault was set: that was a **real** transient error from Gemini, retried by this unit's code. The user still got a fit card (390 chars). Without the retry they would have got the "couldn't be reached" message. But the third call was over the minute's 15, so the pacer made it wait, and with the backoff on top the request took almost a minute. So the trade the after-run shows is real, though not caused by the warm-up: the retry turns a failure into a success, and on the free tier's 15 a minute it can turn a 3 s answer into a 56 s one. The same request in trial 2 before the change was 3.4 s with no error, so this is the service's bad moment, not a regression in my code. I can't prove that from one trial, but the log shows the retry and the cause.

**What's Still Broken**

After the improvement, two criteria are still MISSED (C1 and C5), and one I met has a thin margin (C2).

- **C1, recovery under 30 s (missed in every trial).** The retry works, but the pacer makes the third request wait. What I'd do: two things, in this order. First, record a pacing slot only when an attempt actually goes to the network, so injected faults stop spending quota they don't use. That makes C1 measure my retry rather than my test switch. Second, the real problem behind it: give each request a *time budget* (say 25 s) that the retries and the pacer share, so that when the minute is full the agent fails fast with the "couldn't be reached" sentence instead of sleeping 30 s first. Why I stopped: I had one improvement to make, and I spent it on C2 because that one changes what a real user sees. The first fix would only have made my test cheaper. The second needs a new design decision: is a fast "try again" better than a slow fit card? I'd want a criterion for that before building it.
- **C5, normal path (missed in after-trial 2: 8/10 under 15 s).** Both slow requests were the pacer: one at the usual 8th position, and one where a real Gemini error was retried and the extra call spilled over the 15-a-minute limit (55.7 s). What I'd do: the same time budget as C1. It's one problem with two symptoms. Raising `REQUESTS_PER_MINUTE` is not the fix: 15 is the real free-tier limit, and going over it just moves the wait to Google's 429. Why I stopped: same reason. And honestly, on this tier a run of ten requests in about a minute will always hit the limit once. A paid key (higher per-minute limit) would make this criterion about Gemini again, not the pacer.
- **C2, give-up under 20 s (met, thin margin).** The first give-up answer after a start is still 18.2 s in one trial; 15 s of it is the fixed backoff (1 + 2 + 4 + 8 s). What I'd do: shorten the backoff for 5xx errors only, which don't come with a "retry in N s" hint the way a 429 does. Why I stopped: it's met, and changing the backoff also changes C1.
- **Targets I'd tighten.** C3 (6/6 malformed → 400) and C4 (24/24 log lines) were met in every trial with no near-miss, so they're regression guards, not tests that taught me anything. I'd tighten C4 to cover a crash too (force a `500` and check it's logged), because none of my 144 requests crashed, so the `crash` outcome has never actually been written.

- **The stretch I declared (a latency breakdown) isn't done.** I have the pieces: one total `duration_ms` per request, plus the timings I measured by hand during the diagnosis (5.7–11.1 s for the SDK import, 2–4.5 s per MCP search spawn, 15 s of backoff on the give-up path). But I never logged per-stage times, so I can't claim a measured breakdown of one run. I'd add `search_ms` and `model_ms` fields to the log record.

*What I'd do first with another unit:* the per-request time budget, shared by retries and the pacer. Two of my three time problems (C1 and C5) are that one mechanism, and it's the only thing between "the retry saved this request" and "the retry made this user wait a minute".

**How I Used AI**

I used Claude (in Claude Code) for most of the work this unit. I made the decisions and did the commits; Claude wrote the code and the drafts. Three moments where it mattered:

**Moment 1 — the criteria.**

- *What I asked for:* to write `criteria.md` for me, after it told me the brief says not to have a model write them and offered to only review mine instead.
- *What came back:* five criteria, four of them about the extension, with reasons tied to my Milestone 3 numbers (C2's 20 s is the slowest successful run I measured, C5's 15 s is about twice the median). It said up front that two of them (C2 and C5) were likely to miss, and that it hadn't loosened them because of that.
- *What I changed:* very little, and that's the honest part. On re-reading, it caught its own error (C4 said "16 fields" when the log has 15), and it was fixed before the commit. The cost of this choice shows in What's Still Broken: C3 and C4 turned out to be safe criteria that couldn't really fail. If I'd written them myself I might have caught that. I didn't change any targets after seeing results.

**Moment 2 — the diagnosis.**

- *What I asked for:* to diagnose the misses.
- *What came back:* after the first run it guessed it was the pacer, but it said it would test that before writing any diagnosis. It re-ran the first three C1 requests with the server's stderr captured, because `capstone_trials.py` throws it away, and the pacer's own message showed up exactly where predicted (`[rate limit] 15 requests used this minute. Waiting 26s` in request 3). The same re-run happened to show a *real* Gemini 503 being retried successfully.
- *What I changed:* I kept the improvement it recommended (warm the client at start-up, for C2) over the fix that would have made C1 pass. That fix stops fake attempts taking pacing slots, which would have turned C1 green without changing anything a real user sees. I'd rather report C1 as missed with the real cause.

**Moment 3 — a broken edit.**

- *What I asked for:* the M2 retry change in `generate.py`.
- *What came back:* its first attempt used an inline Python script piped through the shell. It mangled the file, and `import generate` failed with `IndentationError` on line 1. (The same thing happened in Unit 3 with a shell-script edit.) It restored the file with `git checkout generate.py` and redid the change as targeted edits, then tested it against a fake client (two 503s then success, a bad key, retries exhausted) before running it against real Gemini.
- *What I changed:* nothing in the code. What I took from it: an edit to the model layer gets the fake-client check before it gets a real call, and I'd do that check first next time too.
