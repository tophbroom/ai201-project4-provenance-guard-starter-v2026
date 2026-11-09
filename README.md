# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

A writer (or a script) sends text to `POST /submit` and gets back a guess, a
score and a plain-language label. The path:

1. **Request arrives** at `app.py::submit` as JSON with `text` and `creator_id`.
2. **Input check** (`app.py::submit`): a missing, empty or non-string field is a
   400, text over 20,000 characters is a 413. Each rejection is logged.
3. **Signal one** (`detector.py::model_signal`): GPT-2 measures how predictable
   the text is and returns a 0-1 `model_score`, higher meaning more AI-like.
4. **Signal two** (`stylometry.py::style_signal`): measures the shape of the text
   (sentence-length variation, vocabulary variety, punctuation) and returns a
   0-1 `style_score`, same direction.
5. **Combine** (`scoring.py::combine_signals`): the two scores become one
   `confidence`, using the weights and agreement rule in `config.py`.
6. **Label** (`scoring.py::score_to_label`): the score maps to `human`, `unsure`
   or `ai` and to the full sentence a reader sees.
7. **Log and respond** (`audit.py::log_decision`): one line is appended to
   `logs/audit.jsonl` and the JSON response returns the `content_id`, both
   signal scores, the confidence, the guess and the label.

`POST /appeal` takes a `content_id` and the writer's reasoning, appends an
`under_review` entry to the log next to the original decision, and confirms. It
never re-scores. `GET /log` reads the log back.


---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** how predictable the text is to GPT-2 (perplexity, over the
first 400 tokens), squashed to 0-1 by `detector.py::model_signal`. Higher means
more predictable, so more AI-like.

**Why that might differ between human and AI writing:** a language model writes
by picking likely next words, so its output is easy for another model to
predict. Human writing wanders: odd word choices, abrupt turns, the specific
rather than the typical.

**What it can't see:** predictable is not the same as machine-written. Plain
words in short ordinary sentences score as AI-like, and many real people write
that way (second-language writers, younger writers, anyone writing plainly). It
also misses AI text that is ornate or full of rare words, and it reads only the
first ~400 tokens, so anything after roughly 300 words is invisible.

### Signal two — the style signal

**What it measures:** the shape of the text without reading it
(`stylometry.py::style_signal`): sentence-length variation (weight 0.60),
type-token ratio over the first 100 words (0.25) and punctuation other than full
stops per word (0.15). Each is scaled to 0-1 so that low values read AI-like.
Below 20 words it returns 0.5, meaning no idea.

**Why that might differ between human and AI writing:** generated prose leans
toward even, mid-length sentences and a narrower vocabulary. Human writing is
lumpier, such as a three-word sentence next to a forty-word one.

**What it can't see:** meaning. It cannot read, so anything that changes the
shape without changing the substance moves it: typos, chopped or merged
sentences, pasted quotations. Short texts make it unstable, and genres like
lists or poems have odd shape for reasons unrelated to authorship.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:** a weighted average of the two signals, with the style signal
trusted more, then a rule about agreement: a piece can only reach the
high-confidence AI score if *both* signals lean AI. If either signal is below
0.5, the combined score is capped just under the AI threshold. I chose this
because wrongly accusing a writer costs more than missing some AI text, so
accusing requires both signals to agree.

**The numbers:**
- Weights (`config.py`): model signal 0.4, style signal 0.6. Style gets more
  because on my three samples it ranked them correctly (human, then mixed, then
  AI) while the model signal did not.
- Agreement line: 0.5 (`AGREEMENT_LINE`). Cap: `AI_THRESHOLD` − 0.01 = 0.64
  (`AGREEMENT_CAP_MARGIN`).
- Thresholds, still the starter's: human below 0.35, AI above 0.65.
- The weights rest on three samples, so they are a starting point.

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

`confidence` in the response is this combined score: how likely the text is AI,
not how sure the guess is, so a human guess has a low number.

**A case where my two signals split, and what my rule does with it:**

My human-written sample (`samples/human.txt`) scored 0.6548 on the model signal
(AI-like) and 0.4243 on the style signal (human-like). The rule combines them
to 0.5165, which is in the unsure band, and the agreement cap doesn't change
it because the average is already below 0.64. On these three samples the cap
never made a difference; it matters only when the average would otherwise
cross 0.65 while one signal is below 0.5. The AI sample scored 0.5727 and the
mixed one 0.5073, so none of the three reaches a high-confidence label.



---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 – 0.35 | We think this was probably written by a person. |
| unsure | 0.35 – 0.65 | We can't tell whether this was written by a person or with the help of AI. That isn't a judgment against you. If you wrote it yourself, there's nothing you need to do, and you can ask us to take another look at any time. |
| high-confidence AI | 0.65 – 1.00 | Our check thinks this may have been written with the help of AI. Checks like ours can be wrong, especially with plain, simple writing. If you wrote this yourself, please tell us and a person will take a look. |

The ranges come from `scoring.label_ranges()`: a score of exactly 0.35 gets the
human label and exactly 0.65 gets the AI label (`score_to_label` uses `<=` and
`>=`).

**Why I worded the "unsure" one this way:**
It's the one most people will see, and the person reading it may well have
written every word themselves. So it says plainly that we can't tell, says it
isn't a judgment against them, and tells them they don't need to do anything.
It avoids the word "threshold" and any score.



---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "Here I am, sitting upon a flat surface with no control of the world\naround me. I could be bent, crumpled, or broken, but I have no say\nin the matter. I am but an inanimate piece of four-by-six paper,\nripped out from a student'\''s notebook.\nThere is nothing written upon me. I am a blank slate, waiting for\nsomeone to take a palette and illustrate something upon me.\nOh, how I long to have something written upon my blank skin, like a\ntattoo with sentimental value larger than words. Any sort of marking,\neven just the single stroke of a pencil line, will give me meaning and\npurpose.\nOr perhaps I could shift forms. I could be transformed into an\nairplane and soar across the room. What great heights will I see?\nHow will it feel to have the air hit me as I accelerate higher and\nhigher until gravity finally intervenes and lowers me? I wait in\nanticipation for something to happen.\nBut alas, there is no life for me. I am still as blank as a night sky\nwithout stars. Anything would be better than lying here against this\ntable, dead to the world, and paralyzed", "creator_id": "devin"}'
```

```json
{
  "confidence": 0.5165,
  "content_id": "00ac39f3-5ebf-4d9b-bd8c-168dcb157533",
  "guess": "unsure",
  "label": "We can't tell whether this was written by a person or with the help of AI. That isn't a judgment against you. If you wrote it yourself, there's nothing you need to do, and you can ask us to take another look at any time.",
  "model_score": 0.6548,
  "status": "decided",
  "style_score": 0.4243
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "00ac39f3-5ebf-4d9b-bd8c-168dcb157533", "reasoning": "I wrote this myself for a class assignment."}'
```

```json
{
  "content_id": "00ac39f3-5ebf-4d9b-bd8c-168dcb157533",
  "message": "Thanks. We've recorded your appeal and a person will review it.",
  "status": "under_review"
}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json
{
  "count": 2,
  "entries": [
    {
      "combined_score": 0.5165,
      "content_id": "00ac39f3-5ebf-4d9b-bd8c-168dcb157533",
      "creator_id": "devin",
      "guess": "unsure",
      "label": "We can't tell whether this was written by a person or with the help of AI. That isn't a judgment against you. If you wrote it yourself, there's nothing you need to do, and you can ask us to take another look at any time.",
      "model_score": 0.6548,
      "status": "decided",
      "style_score": 0.4243,
      "timestamp": "2026-11-09T10:05:15+00:00"
    },
    {
      "content_id": "00ac39f3-5ebf-4d9b-bd8c-168dcb157533",
      "creator_id": "devin",
      "event": "appeal",
      "reasoning": "I wrote this myself for a class assignment.",
      "status": "under_review",
      "timestamp": "2026-11-09T10:05:15+00:00"
    }
  ]
}
```

---

## How I Used AI

<!-- DRAFT: Moment 2 and the "what I asked" lines were reconstructed from the
     code and notes. Check them against what actually happened, then delete
     this comment. -->

**Moment 1: the `/submit` route (`app.py::submit`)**

- *What I asked for:* the `/submit` function, following the starter's
  milestones: read `text` and `creator_id`, call both signals, combine them,
  map the score to a label, log the decision and return the JSON.
- *What came back:* a working route that validates the body, calls
  `detector.model_signal` and `stylometry.style_signal`, combines them with
  `scoring.combine_signals`, writes a `decided` log entry and returns all six
  required fields. It also handled the bad-input cases (not a JSON object,
  missing or empty fields, text over 20,000 characters, text too short, detector
  unavailable) with a 400, 413 or 503, and logged each one as a rejection.
- *What I changed:* I read it against the Milestone 1 contract in
  my project 7 notes and checked the response against the README's required
  fields (`content_id`, `guess`, `confidence`, `label`, `model_score`,
  `style_score`). I also set the length cap in `config.py` (`MAX_TEXT_CHARS`),
  since that number was my decision and not the code's.

**Moment 2: the combining rule (`scoring.py::combine_signals`)**

- *What I asked for:* a combining rule for the two signals that reflects my
  Milestone 1 decision that wrongly accusing a writer costs more than missing AI
  text.
- *What came back:* a weighted average, plus a rule that caps the score just
  under the AI threshold unless both signals lean AI.
- *What I changed:* I moved the weights from the starter's 0.5/0.5 to 0.4 model
  and 0.6 style, because on my samples the style signal ranked human, mixed, AI
  in the right order and the model signal didn't. I then checked the rule against
  the four samples in my project 7 notes. The cap never changed a result
  there, and all four scores landed between 0.50 and 0.58, so I wrote that down
  in Signals and Scoring as a limit and did not claim the rule had been proven.

**Also: the AI sample.** I had AI write an AI version of my human text
(`samples/human.txt`), which became `samples/ai.txt`. Both are on the same topic
and about the same length, so the calibration in my project 7 notes compares
like with like. The AI sample is generated text, not something I wrote.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
