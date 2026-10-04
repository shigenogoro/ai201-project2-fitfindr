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
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```

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
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**



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

```

**Empty search**

```

```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



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

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
