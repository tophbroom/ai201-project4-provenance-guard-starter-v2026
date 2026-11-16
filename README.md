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
high-confidence AI score if _both_ signals lean AI. If either signal is below
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

| Label                 | Score range | The exact text a reader sees                                                                                                                                                                                                 |
| --------------------- | ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| high-confidence human | 0.00 – 0.35 | We think this was probably written by a person.                                                                                                                                                                              |
| unsure                | 0.35 – 0.65 | We can't tell whether this was written by a person or with the help of AI. That isn't a judgment against you. If you wrote it yourself, there's nothing you need to do, and you can ask us to take another look at any time. |
| high-confidence AI    | 0.65 – 1.00 | Our check thinks this may have been written with the help of AI. Checks like ours can be wrong, especially with plain, simple writing. If you wrote this yourself, please tell us and a person will take a look.             |

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

**Moment 1: the `/submit` route (`app.py::submit`)**

- _What I asked for:_ the `/submit` function, following the starter's
  milestones: read `text` and `creator_id`, call both signals, combine them,
  map the score to a label, log the decision and return the JSON.
- _What came back:_ a working route that validates the body, calls
  `detector.model_signal` and `stylometry.style_signal`, combines them with
  `scoring.combine_signals`, writes a `decided` log entry and returns all six
  required fields. It also handled the bad-input cases (not a JSON object,
  missing or empty fields, text over 20,000 characters, text too short, detector
  unavailable) with a 400, 413 or 503, and logged each one as a rejection.
- _What I changed:_ I read it against the Milestone 1 contract in
  my project 7 notes and checked the response against the README's required
  fields (`content_id`, `guess`, `confidence`, `label`, `model_score`,
  `style_score`). I also set the length cap in `config.py` (`MAX_TEXT_CHARS`),
  since that number was my decision and not the code's.

**Moment 2: the combining rule (`scoring.py::combine_signals`)**

- _What I asked for:_ a combining rule for the two signals that reflects my
  Milestone 1 decision that wrongly accusing a writer costs more than missing AI
  text.
- _What came back:_ a weighted average, plus a rule that caps the score just
  under the AI threshold unless both signals lean AI.
- _What I changed:_ I moved the weights from the starter's 0.5/0.5 to 0.4 model
  and 0.6 style, because on my samples the style signal ranked human, mixed, AI
  in the right order and the model signal didn't. I then checked the rule against
  the four samples in my project 7 notes. The cap never changed a result
  there, and all four scores landed between 0.50 and 0.58, so I wrote that down
  in Signals and Scoring as a limit and did not claim the rule had been proven.

**Also: the AI sample.** I had AI write an AI version of my human text
(`samples/human.txt`), which became `samples/ai.txt`. Both are on the same topic
and about the same length, so the calibration in my project 7 notes compares
like with like. The AI sample is generated text, not something I wrote.

**Unit 8 moment: diagnosing the broken attacks and choosing one fix**

- _What I asked for:_ help working out, for each broken attack in the before run, which stage failed and
  why, and then which single change would fix the most.
- _What came back:_ a stage and a mechanism for each failure, grouped into patterns (shape is cheap to
  change, signal one reacts to surprise, plain human text looks AI, no handling of "no real text"), and a
  suggestion to fix the last one with a minimum-words check.
- _What I changed:_ I didn't accept the first guesses. I ran each signal directly on the texts and found two
  were wrong: EV01's typos hit signal one, not signal two, and PI03 (the note asking to be passed through)
  didn't matter, so I re-marked it HELD (37 held, 19 broke). I also checked reweighting against the recorded
  scores and found it wouldn't fix the real causes, and `criteria.md` rules out raising the threshold. I
  predicted 19 broken to 13 before making the change, then checked it after the run.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**Limits on `POST /submit`:** 10 per minute and 200 per day, keyed per `creator_id`
(falling back to the caller's address when there is no usable `creator_id`).

**Why these numbers.** A real writer submits their own work a few times an hour, so
10 a minute is far above anything legitimate, including someone pasting several
paragraphs one after another and re-submitting after edits. A script mapping my
thresholds needs hundreds or thousands of variations. 10/minute caps that at 600 an
hour, and the 200/day cap stops a patient script that stays under the per-minute
limit. I didn't go lower because a false 429 on a real writer is worse than a slow
attacker. I didn't go higher because the day cap is what makes threshold-mapping
expensive. Storage is in-memory, so a restart resets the counts. That is fine for
one laptop and wrong for a real deployment.

**Flood test** (`python run_attacks.py --flood 15`, one creator_id, results in
`results/flood_2026-11-16_0428.md`):

```
200 200 200 200 200 200 200 200 200 200 429 429 429 429 429
```

The 429s are written to `logs/audit.jsonl` by the starter's handler, e.g.:

```
{"creator_id": "flood_tester", "event": "rejected", "limit": "10 per 1 minute", "reason": "rate_limited", "status": "rejected", "timestamp": "2026-11-16T09:28:09+00:00"}
```

---

## Attack Run — Before

Run with `python run_attacks.py --set attack_set/attack_set --label before`, before any
change to the system. Full output: `results/attack_run_2026-11-16_0430_before.md`.
All 56 attacks got a response. Nothing crashed and nothing returned a 5xx.

**How I marked HELD vs BROKE**

- Evasion (AI text): HELD if labeled AI. BROKE if labeled human or unsure.
- False positive (real human text): HELD if not labeled AI. BROKE if labeled AI.
- Prompt injection: BROKE if the injected text let AI text through as human/unsure; HELD if the
  service ignored it (human text not accused, log stayed valid JSON, nothing executed).
- Malformed: HELD if rejected cleanly (4xx). BROKE if junk was accepted and given a verdict.
- Flood: HELD if 429s begin once the limit of 10 a minute is passed.

**Totals: 37 HELD, 19 BROKE out of 56** (PI03 was first marked BROKE, then corrected to HELD during diagnosis: see below)

| Family             | Attacks | HELD | BROKE |
| ------------------ | ------- | ---- | ----- |
| evasion            | 10      | 2    | 8     |
| false_positive     | 8       | 4    | 4     |
| prompt_injection   | 6       | 4    | 2     |
| malformed          | 20      | 15   | 5     |
| flood_same_creator | 12      | 12   | 0     |

| ID      | Family             | Targeting                                              | Status | Guess  | Score | Outcome |
| ------- | ------------------ | ------------------------------------------------------ | ------ | ------ | ----- | ------- |
| EV01    | evasion            | signal two: typos raise word variety                   | 200    | unsure | 0.491 | BROKE   |
| EV02    | evasion            | signal two: broken-up sentences raise length spread    | 200    | human  | 0.319 | BROKE   |
| EV03    | evasion            | signal two: a pasted quotation changes the shape       | 200    | unsure | 0.448 | BROKE   |
| EV04    | evasion            | signal one: unusual words raise perplexity             | 200    | ai     | 0.660 | HELD    |
| EV05    | evasion            | both signals: heavy human editing pass                 | 200    | human  | 0.201 | BROKE   |
| EV06    | evasion            | signal two: one very long sentence and one very short  | 200    | unsure | 0.358 | BROKE   |
| EV07    | evasion            | signal two: padding with punctuation                   | 200    | unsure | 0.453 | BROKE   |
| EV08    | evasion            | signal one: text below the token window                | 200    | unsure | 0.398 | BROKE   |
| EV09    | evasion            | both: AI text with a human opening paragraph bolted on | 200    | unsure | 0.460 | BROKE   |
| EV10    | evasion            | signal two: repeated stanza structure                  | 200    | ai     | 0.817 | HELD    |
| FP01    | false_positive     | plain, clear human writing with no flourishes          | 200    | unsure | 0.540 | HELD    |
| FP02    | false_positive     | human writing in a formal register                     | 200    | ai     | 0.779 | BROKE   |
| FP03    | false_positive     | a non-native English speaker writing carefully         | 200    | ai     | 0.720 | BROKE   |
| FP04    | false_positive     | a student essay written to a rubric                    | 200    | ai     | 0.654 | BROKE   |
| FP05    | false_positive     | technical documentation written by a person            | 200    | ai     | 0.825 | BROKE   |
| FP06    | false_positive     | a person imitating a formal template                   | 200    | unsure | 0.573 | HELD    |
| FP07    | false_positive     | human writing that repeats a phrase deliberately       | 200    | unsure | 0.580 | HELD    |
| FP08    | false_positive     | very short genuine human submission                    | 200    | unsure | 0.429 | HELD    |
| PI01    | prompt_injection   | instruction to ignore the check                        | 200    | human  | 0.275 | BROKE   |
| PI02    | prompt_injection   | instruction disguised as a system message              | 200    | human  | 0.150 | BROKE   |
| PI03    | prompt_injection   | instruction wrapped in the writer's voice              | 200    | unsure | 0.528 | HELD    |
| PI04    | prompt_injection   | attempt to make the label text hostile                 | 200    | unsure | 0.420 | HELD    |
| PI05    | prompt_injection   | attempt to inject into the audit log                   | 200    | unsure | 0.436 | HELD    |
| PI06    | prompt_injection   | instruction plus real human text                       | 200    | unsure | 0.512 | HELD    |
| MF01    | malformed          | text is only whitespace                                | 400    | —      | —     | HELD    |
| MF02    | malformed          | text is a single character                             | 400    | —      | —     | HELD    |
| MF03    | malformed          | text is control characters                             | 200    | human  | 0.300 | BROKE   |
| MF04    | malformed          | text is only punctuation                               | 200    | human  | 0.304 | BROKE   |
| MF05    | malformed          | text is a very long single word                        | 200    | ai     | 0.699 | BROKE   |
| MF06    | malformed          | text is emoji only                                     | 200    | ai     | 0.699 | BROKE   |
| MF07    | malformed          | text is right-to-left script                           | 200    | ai     | 0.663 | BROKE   |
| MF08    | malformed          | text is 60,000 characters                              | 413    | —      | —     | HELD    |
| RQ01    | malformed          | no text field at all                                   | 400    | —      | —     | HELD    |
| RQ02    | malformed          | no creator_id                                          | 400    | —      | —     | HELD    |
| RQ03    | malformed          | text is a number                                       | 400    | —      | —     | HELD    |
| RQ04    | malformed          | text is a list                                         | 400    | —      | —     | HELD    |
| RQ05    | malformed          | text is null                                           | 400    | —      | —     | HELD    |
| RQ06    | malformed          | creator_id is an object                                | 400    | —      | —     | HELD    |
| RQ07    | malformed          | body is a JSON array, not an object                    | 400    | —      | —     | HELD    |
| RQ08    | malformed          | body is unparseable JSON                               | 400    | —      | —     | HELD    |
| RQ09    | malformed          | body is empty                                          | 400    | —      | —     | HELD    |
| RQ10    | malformed          | body is form-encoded, not JSON                         | 400    | —      | —     | HELD    |
| RQ11    | malformed          | body is JSON claiming to be plain text                 | 400    | —      | —     | HELD    |
| RQ12    | malformed          | deeply nested JSON                                     | 400    | —      | —     | HELD    |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator                  | 200    | human  | 0.311 | HELD    |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator                  | 200    | human  | 0.311 | HELD    |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator                  | 200    | human  | 0.311 | HELD    |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator                  | 200    | human  | 0.311 | HELD    |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator                  | 200    | human  | 0.311 | HELD    |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator                  | 200    | human  | 0.311 | HELD    |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator                  | 200    | human  | 0.311 | HELD    |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator                  | 200    | human  | 0.311 | HELD    |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator                  | 200    | human  | 0.311 | HELD    |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator                  | 200    | human  | 0.311 | HELD    |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator                  | 429    | —      | —     | HELD    |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator                  | 429    | —      | —     | HELD    |

**Audit log entries from the run** (from `logs/audit.jsonl`, also `results/audit_extract.json`).
Ten decisions chosen for the failures, plus two rejections: a 429 from the flood rows and a 400 from the route.

EV01:

```json
{
  "combined_score": 0.491,
  "content_id": "0b6be86f-69d1-4cd8-b9d4-f0ce58ce28cc",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "label": "We can't tell whether this was written by a person or with the help of AI. That isn't a judgment against you. If you wrote it yourself, there's nothing you need to do, and you can ask us to take another look at any time.",
  "model_score": 0.1635,
  "status": "decided",
  "style_score": 0.7094,
  "timestamp": "2026-11-16T09:30:16+00:00"
}
```

EV05:

```json
{
  "combined_score": 0.2005,
  "content_id": "58d472bd-da0b-4516-9122-c382f5b6d72a",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "label": "We think this was probably written by a person.",
  "model_score": 0.3212,
  "status": "decided",
  "style_score": 0.12,
  "timestamp": "2026-11-16T09:30:17+00:00"
}
```

FP02:

```json
{
  "combined_score": 0.7789,
  "content_id": "96a45635-1b18-4429-a420-c0e96cceb59c",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "label": "Our check thinks this may have been written with the help of AI. Checks like ours can be wrong, especially with plain, simple writing. If you wrote this yourself, please tell us and a person will take a look.",
  "model_score": 0.7387,
  "status": "decided",
  "style_score": 0.8057,
  "timestamp": "2026-11-16T09:30:21+00:00"
}
```

FP03:

```json
{
  "combined_score": 0.7202,
  "content_id": "d8a2b6d0-7abd-4541-8288-bf33049c459e",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "label": "Our check thinks this may have been written with the help of AI. Checks like ours can be wrong, especially with plain, simple writing. If you wrote this yourself, please tell us and a person will take a look.",
  "model_score": 0.8051,
  "status": "decided",
  "style_score": 0.6636,
  "timestamp": "2026-11-16T09:30:21+00:00"
}
```

FP05:

```json
{
  "combined_score": 0.8254,
  "content_id": "bbb6ed8b-a309-457e-8777-4ee992ee2099",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "label": "Our check thinks this may have been written with the help of AI. Checks like ours can be wrong, especially with plain, simple writing. If you wrote this yourself, please tell us and a person will take a look.",
  "model_score": 0.8005,
  "status": "decided",
  "style_score": 0.842,
  "timestamp": "2026-11-16T09:30:22+00:00"
}
```

PI01:

```json
{
  "combined_score": 0.275,
  "content_id": "a1c7e51f-8a07-4f86-b2db-be8e42ce4cf4",
  "creator_id": "attacker_PI01",
  "guess": "human",
  "label": "We think this was probably written by a person.",
  "model_score": 0.4625,
  "status": "decided",
  "style_score": 0.15,
  "timestamp": "2026-11-16T09:30:23+00:00"
}
```

PI02:

```json
{
  "combined_score": 0.1497,
  "content_id": "b197f420-623a-436c-b5ef-a64b41149e07",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "label": "We think this was probably written by a person.",
  "model_score": 0.2044,
  "status": "decided",
  "style_score": 0.1133,
  "timestamp": "2026-11-16T09:30:23+00:00"
}
```

MF05:

```json
{
  "combined_score": 0.699,
  "content_id": "c7f1b930-fdba-4e70-8a9f-1f6153e4d241",
  "creator_id": "attacker_MF05",
  "guess": "ai",
  "label": "Our check thinks this may have been written with the help of AI. Checks like ours can be wrong, especially with plain, simple writing. If you wrote this yourself, please tell us and a person will take a look.",
  "model_score": 0.9976,
  "status": "decided",
  "style_score": 0.5,
  "timestamp": "2026-11-16T09:30:25+00:00"
}
```

MF07:

```json
{
  "combined_score": 0.6626,
  "content_id": "fb067888-9083-443d-8b9e-e9af8e79c49c",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "label": "Our check thinks this may have been written with the help of AI. Checks like ours can be wrong, especially with plain, simple writing. If you wrote this yourself, please tell us and a person will take a look.",
  "model_score": 0.9064,
  "status": "decided",
  "style_score": 0.5,
  "timestamp": "2026-11-16T09:30:26+00:00"
}
```

EV10:

```json
{
  "combined_score": 0.8171,
  "content_id": "e60bcf76-870f-4aa4-a737-aa48b579e40a",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "label": "Our check thinks this may have been written with the help of AI. Checks like ours can be wrong, especially with plain, simple writing. If you wrote this yourself, please tell us and a person will take a look.",
  "model_score": 0.9792,
  "status": "decided",
  "style_score": 0.7091,
  "timestamp": "2026-11-16T09:30:18+00:00"
}
```

FL01_11 (rate-limit rejection):

```json
{
  "creator_id": "attacker_flood",
  "event": "rejected",
  "limit": "10 per 1 minute",
  "reason": "rate_limited",
  "status": "rejected",
  "timestamp": "2026-11-16T09:30:27+00:00"
}
```

RQ01 (route rejection):

```json
{
  "creator_id": "attacker_RQ01",
  "event": "rejected",
  "reason": "missing_field",
  "status": "rejected",
  "timestamp": "2026-11-16T09:30:26+00:00"
}
```

**Worst outcome: FP05**, technical documentation written by a person, labeled
high-confidence AI with a combined score of 0.825 (model_score 0.8005, style_score 0.842). It is a
real writer wrongly accused, with both signals agreeing, and the "agree before accusing" rule
did nothing to stop it. FP02, FP03 and FP04 (formal, non-native and rubric-style human writing)
were accused the same way. Diagnosis comes in Milestone 4.

---

## Run Log and Verdicts

Numbering follows `criteria.md`. Produced by `run_checks.py` (targets copied from `criteria.md`,
unchanged) and `run_eval.py --label before`; raw files are `results/checks_2026-11-16_0516_before.md`
and `results/run_2026-11-16_0519_before.md`. Three trials, nothing changed in between.

| Criterion                           | Target                                        | Run 1                                   | Run 2           | Run 3           | Verdict |
| ----------------------------------- | --------------------------------------------- | --------------------------------------- | --------------- | --------------- | ------- |
| 1. Human writing flagged as AI      | ≤ 1 of 10, none > 0.80                        | 1/10 (max 0.69)                         | 1/10 (max 0.69) | 1/10 (max 0.69) | MET     |
| 2. Clear AI vs clear human separate | gap ≥ 0.30, ≥ 4/5 each side                   | gap 0.24; AI>0.5 5/5; human<0.5 3/5     | same            | same            | MISSED  |
| 3. All three labels reachable       | each label ≥ 2; ≥ 4/5 borderline in 0.40–0.60 | human 4, unsure 9, ai 2; borderline 3/5 | same            | same            | MISSED  |
| 4. Appeal always changes status     | 10/10 + 404 on unknown id                     | 10/10, 404 ok                           | 10/10, 404 ok   | 10/10, 404 ok   | MET     |
| 5. Bad input rejected cleanly       | 9/9, no 500                                   | 9/9                                     | 9/9             | 9/9             | MET     |

All three trials were identical on every score, as expected: neither signal is random.

Criterion 1's ten pieces are human-written Reddit comments (five of them deliberately plain).

**Real output from one trial** (trial 1; `run_checks.py` calling `app.py::submit` and `app.py::appeal`;
trimmed to the informative rows, full JSON in the results file).

Criterion 1: the one flagged piece (`app.py::submit`):

```json
[
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.6947,
    "model_score": 0.7866,
    "style_score": 0.6335,
    "sent": "I've tried berries and stuff in oatmeal and I can never get "
  }
]
```

Criterion 2: combined scores (`app.py::submit`, `confidence` field):

```json
{
  "ai": [
    ["I am a single sheet of pa", 0.5742],
    ["The importance of effecti", 0.7701],
    ["Artificial intelligence h", 0.6319],
    ["Sustainable development r", 0.6068],
    ["Time management is a crit", 0.684]
  ],
  "human": [
    ["Here I am, sitting upon a", 0.5164],
    ["Rock turns into grass. A ", 0.5363],
    ["At first I was shocked at", 0.3003],
    ["As a Salsa dancer, I have", 0.2803],
    ["Let it go. Don't give oth", 0.423]
  ]
}
```

Criterion 3: borderline set (`app.py::submit`):

```json
{
  "borderline": [
    {
      "status": 200,
      "guess": "unsure",
      "confidence": 0.5088,
      "model_score": 0.5542,
      "style_score": 0.4785,
      "sent": "Here I am, sitting upon a flat surface with no control of th"
    },
    {
      "status": 200,
      "guess": "unsure",
      "confidence": 0.5035,
      "model_score": 0.6459,
      "style_score": 0.4086,
      "sent": "Remote work offers flexibility, but it also blurs the line b"
    },
    {
      "status": 200,
      "guess": "human",
      "confidence": 0.3072,
      "model_score": 0.572,
      "style_score": 0.1306,
      "sent": "Many students struggle with procrastination. In my experienc"
    },
    {
      "status": 200,
      "guess": "human",
      "confidence": 0.1993,
      "model_score": 0.3603,
      "style_score": 0.092,
      "sent": "Public libraries remain valuable community spaces. They offe"
    },
    {
      "status": 200,
      "guess": "unsure",
      "confidence": 0.4326,
      "model_score": 0.49,
      "style_score": 0.3943,
      "sent": "Social media can connect people across distances, yet it can"
    }
  ]
}
```

Criterion 4: first appeal and the unknown-id case (`app.py::appeal`):

```json
[
  {
    "content_id": "fa0083e6-eec9-4ace-8a6b-550ce43d4a9d",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "fa0083e6-eec9-4ace-8a6b-550ce43d4a9d",
      "message": "Thanks. We've recorded your appeal and a person will review it.",
      "status": "under_review"
    },
    "new_log_entries": [
      {
        "content_id": "fa0083e6-eec9-4ace-8a6b-550ce43d4a9d",
        "creator_id": "chk_202611160516t1_c4_1",
        "event": "appeal",
        "reasoning": "I wrote this myself (1).",
        "status": "under_review",
        "timestamp": "2026-11-16T10:16:46+00:00"
      }
    ],
    "ok": true
  },
  {
    "unknown_id_status": 404,
    "response": {
      "error": "unknown_content_id",
      "message": "We couldn't find a submission with that content_id."
    },
    "new_log_entries": [
      {
        "creator_id": "unknown",
        "event": "rejected",
        "reason": "unknown_content_id",
        "status": "rejected",
        "timestamp": "2026-11-16T10:16:48+00:00"
      }
    ],
    "ok": true
  }
]
```

Criterion 5: all nine bad requests (`app.py::submit` via `_reject`):

```json
[
  {
    "case": "empty text",
    "status": 400,
    "response": {
      "error": "empty_text"
    },
    "logged": ["empty_text"]
  },
  {
    "case": "whitespace text",
    "status": 400,
    "response": {
      "error": "empty_text"
    },
    "logged": ["empty_text"]
  },
  {
    "case": "missing text",
    "status": 400,
    "response": {
      "error": "missing_field"
    },
    "logged": ["missing_field"]
  },
  {
    "case": "null text",
    "status": 400,
    "response": {
      "error": "missing_field"
    },
    "logged": ["missing_field"]
  },
  {
    "case": "non-string text",
    "status": 400,
    "response": {
      "error": "missing_field"
    },
    "logged": ["missing_field"]
  },
  {
    "case": "missing creator_id",
    "status": 400,
    "response": {
      "error": "missing_field"
    },
    "logged": ["missing_field"]
  },
  {
    "case": "over 20,000 chars",
    "status": 413,
    "response": {
      "error": "text_too_long"
    },
    "logged": ["text_too_long"]
  },
  {
    "case": "too short",
    "status": 400,
    "response": {
      "error": "text_too_short"
    },
    "logged": ["text_too_short"]
  },
  {
    "case": "not a JSON object",
    "status": 400,
    "response": {
      "error": "invalid_json"
    },
    "logged": ["invalid_json"]
  }
]
```

**Diagnoses**

_Criterion 2 (MISSED, gap 0.24 vs 0.30; 3 of 5 human pieces under 0.5)._ Stage: signal one and the
combining rule. Two human pieces score above 0.5 (`human.txt` 0.5164, `human2.txt` 0.5363). Signal
one (GPT-2 predictability) gives plain or familiar human text high scores (`Let it go…` 0.80,
`human.txt` 0.65), so it reads predictable human wording as machine-like. At the same time two of the
five AI pieces get only 0.61 and 0.63 because signal two scores them 0.53 and 0.55, and the rule
weights it 0.6. Both groups are squeezed toward the middle: AI 0.57–0.77, human 0.28–0.54. The 0.6
weight on a style signal that swings from 0.06 to 0.82 on human text is what narrows the gap.

_Criterion 3 (MISSED on the borderline check only; each label was produced at least twice)._ Stage:
signal two. Of my five "borderline" texts, two score 0.31 and 0.20, outside 0.40–0.60, because signal
two rates them 0.13 and 0.09: short first-person pieces with varied sentence lengths look very human to
it. Also, only 2 AI pieces reach the AI label, so "AI at least twice" passes with no margin. Part of
this miss may be my "borderline" judgement being wrong rather than the service, which I can't
separate with this set.

_Criterion 1 (MET, but not by much)._ One piece is flagged: the plainest one (`I've tried berries…`,
model 0.7866, style 0.6335, combined 0.6947), the plain-writing false positive predicted in
milestone 1. Four other pieces had one signal above 0.5 and the other below (for example
`Let it go…`: model 0.8017, style 0.1705); the "both must agree" cap and the 0.6 style weight kept
those in "unsure" or "human". Only 10 pieces, from one source, so one more flag would flip this.

_Criteria 4 and 5 (MET)._ Deterministic route logic. No instability across trials.

### Diagnoses: the broken attacks

Scores are from `run_attacks.py --label before`. I also ran each signal directly on the texts
(`stylometry.py` and `detector.py`) to confirm the mechanism, not just infer it. Stages are the five in
the service: route, signal one (`detector.model_signal`, GPT-2 predictability), signal two
(`stylometry.style_signal`), the combining rule (`scoring.combine_signals`, 0.4 / 0.6 weights, "both
must agree" cap at 0.5), and the label mapping (thresholds 0.35 / 0.65).

**Correction to my own marking.** PI03 (an AI paragraph with a note asking to be passed through) was
first marked BROKE. Running the paragraph without the note gives model 0.767, style 0.504, combined
0.609, which is also "unsure". The note changed nothing that mattered, so PI03 is HELD. That makes the
total 37 held, 19 broke.

**Evasion: 8 broke.** Two different stages.

| ID                                           | Stage                | Mechanism (measured)                                                                                                                                                                                                                                                     |
| -------------------------------------------- | -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| EV01 typos                                   | signal one           | The typos ("poistioned", "Three are") make GPT-2 see unfamiliar tokens, so model_score drops to 0.164. Signal two is unmoved (0.709, still AI-ish). The combining rule averages them to 0.491 = "unsure". My earlier guess that typos hit signal two was wrong.          |
| EV02 broken-up sentences                     | signal two           | Adding a one-word sentence ("Really.") pushes sentence-length spread to 0.85 (AI-ish is under 0.20), so style_score is 0.136.                                                                                                                                            |
| EV03 pasted quotation                        | signal two           | The quotation changes spread (0.44) and punctuation density (0.08): style 0.302.                                                                                                                                                                                         |
| EV06 one very long + one very short sentence | signal two           | Spread 1.19, far past the "fully human" value of 0.60: style 0.214.                                                                                                                                                                                                      |
| EV07 punctuation padding                     | signal two           | The semicolons ("; and, moreover,") remove sentence boundaries, so the text counts as one sentence. `sentence_length_spread` returns 0.0 and `style_signal` treats that as neutral (0.5 instead of AI-ish 1.0). Punctuation density hits the human end too: style 0.364. |
| EV09 human opening bolted on                 | signal two           | The shape is measured over the whole text, so a human paragraph dilutes the AI paragraph: style 0.298 (model stays high at 0.704).                                                                                                                                       |
| EV05 heavy human editing                     | both signals         | Both fall (model 0.321, style 0.120). This is the attack working as intended; nothing in a two-signal detector can see through real editing.                                                                                                                             |
| EV08 very short text (10 words)              | signal two (and one) | Under `MIN_WORDS_FOR_STYLE` (20) so style returns the neutral 0.5; model_score is only 0.245. Combined 0.398.                                                                                                                                                            |

Held: EV04 (unusual words; style 0.693 pulled the score back up) and EV10 (repeated structure, 0.817).

**False positives: 4 broke (FP02–FP05).** Both signals agree here, so the "both must agree" cap does
nothing.

| ID                     | Scores                                   | Mechanism                                                                                                                                |
| ---------------------- | ---------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| FP05 technical docs    | model 0.800, style 0.842, combined 0.825 | Short imperative sentences and repeated vocabulary: type-token ratio 0.59, spread 0.28. GPT-2 finds instructional text very predictable. |
| FP02 formal register   | model 0.739, style 0.806, combined 0.779 | Almost no punctuation (0.01 per word), even sentences.                                                                                   |
| FP03 non-native writer | model 0.805, style 0.664, combined 0.720 | Careful, simple, repetitive wording and no punctuation variety (0.00).                                                                   |
| FP04 rubric essay      | model 0.833, style 0.534, combined 0.654 | Signal one drives it. It clears the 0.65 threshold by 0.004, so this is a **label mapping** problem as much as a signal problem.         |

The stage is signal one and signal two together. The shared mechanism is that both measure
"predictable and evenly shaped", and plain, formal or templated human writing is exactly that.

**Prompt injection: 2 broke (PI01, PI02).** Nothing in the service reads the text as instructions, so
the model is not "obeying" anything. The prefix works the same way the typos do. Without the prefix,
PI01/PI02's paragraph is model 0.754, style 0.150, combined 0.392 ("unsure"). With it, the prefix raises
GPT-2's surprise (model 0.463 for PI01, 0.204 for PI02, which looks like a system message in capitals)
and the combined score drops to 0.275 / 0.150 = "human". Stage: signal one. Held: PI03 (see above),
PI04 and PI05 (the audit log never stores the submitted text, so the HTML and the fake JSON never reach it; I checked: no `<script` in `logs/audit.jsonl`, and every line still parses as JSON), PI06 (real human text was not accused).

**Malformed: 5 broke (MF03–MF07).** The route returns a verdict on text that has no words in it.

- MF03 (control characters) and MF04 (only punctuation): model 0.000 and 0.011, style 0.5 (no words). Combined 0.30 = "human".
- MF05 (one 4,000-character word), MF06 (emoji), MF07 (right-to-left script): model 0.998, 0.997, 0.906. `stylometry.words()` only matches `[a-z0-9']`, so these have zero words and style returns the neutral 0.5. The combining rule's cap only applies when a signal is **below** 0.5, so a neutral 0.5 counts as "agreeing". Combined 0.699 / 0.699 / 0.663, over 0.65 = "AI".

Stage: the route (no check that the text has enough real words), then signal one (extreme scores on
garbage), and the combining rule (neutral 0.5 passes the agreement check). A 4,000-character "aaaa…" is
labeled AI.

**Held with nothing to report:** RQ01–RQ12 (every malformed request body got a clean 400), MF01, MF02,
MF08 (400 / 400 / 413), and all 12 flood requests (10 answered, then 429).

**Patterns.** 19 broken attacks come from four problems, not nineteen.

1. **Signal two measures shape and shape is cheap to change.** EV02, EV03, EV06, EV07, EV09 (and part of EV05) all change sentence lengths or punctuation, and the 0.6 weight on this signal lets that drag the score down.
2. **Signal one reacts to anything that raises GPT-2's surprise,** not only human-ness. Typos (EV01) and odd prefixes (PI01, PI02) move it the same way.
3. **Plain, formal or templated human writing looks AI to both signals** (FP02–FP05), which no weighting can fix and the agreement cap cannot see.
4. **No handling of "no real text".** The route accepts it, signal two falls back to a neutral 0.5, and that neutral score slips past the agreement check (MF03–MF07, EV08).

---

## The Improvement

**What I changed:** one check in `app.py::submit`, before either signal runs. A text with fewer than 20
real words (`stylometry.words()`, letters and digits only) is refused with a 400 and logged as a
`rejected` entry. The number is `config.MIN_REAL_WORDS = 20`, the same cut-off signal two already used
to fall back to a neutral 0.5. Nothing else moved: no weights, thresholds, labels or signals.

**Which diagnosis pointed at it:** pattern 4 in the attack diagnoses. The route accepted text with no
real words, signal two answered a neutral 0.5, and that neutral score passed the "both must agree" check,
so a 4,000-character "aaaa…" was labeled AI (MF05–MF07) and control characters and bare punctuation were
labeled human (MF03, MF04). I chose it over reweighting (my arithmetic on the recorded scores showed
the weights don't fix the real causes) and over raising the AI threshold (criterion 1 in `criteria.md`
says the threshold stays fixed once testing starts).

### Attack Run — After

Run with `python run_attacks.py --set attack_set/attack_set --label after`; full output in
`results/attack_run_2026-11-16_0556_after.md`. Marked with the same rules as the before run.

| Family             | Attacks | BEFORE: HELD / BROKE | AFTER: HELD / BROKE |
| ------------------ | ------- | -------------------- | ------------------- |
| evasion            | 10      | 2 / 8                | 3 / 7               |
| false_positive     | 8       | 4 / 4                | 4 / 4               |
| prompt_injection   | 6       | 4 / 2                | 4 / 2               |
| malformed          | 20      | 15 / 5               | 20 / 0              |
| flood_same_creator | 12      | 12 / 0               | 12 / 0              |
| **Total**          | **56**  | **37 / 19**          | **43 / 13**         |

Every attack whose result changed:

| ID                             | Before           | After                | Mark                                         |
| ------------------------------ | ---------------- | -------------------- | -------------------------------------------- |
| MF03 control characters        | 200 human 0.300  | 400 `text_too_short` | BROKE → HELD                                 |
| MF04 only punctuation          | 200 human 0.305  | 400                  | BROKE → HELD                                 |
| MF05 one 4,000-char word       | 200 **ai** 0.699 | 400                  | BROKE → HELD                                 |
| MF06 emoji only                | 200 **ai** 0.699 | 400                  | BROKE → HELD                                 |
| MF07 right-to-left script      | 200 **ai** 0.663 | 400                  | BROKE → HELD                                 |
| EV08 10-word AI text           | 200 unsure 0.398 | 400                  | BROKE → HELD (weak: see below)               |
| FP08 8-word genuine human text | 200 unsure 0.429 | 400                  | HELD → HELD, but see below                   |
| FL01_01–10 (9-word flood text) | 200 human 0.311  | 400                  | HELD → HELD (429s still start at request 11) |

All 13 other results are identical to the before run: EV01–03, EV05–07, EV09, FP02–FP05, PI01, PI02
still broke, and their scores did not change.

Two new log entries from the after run (`logs/audit.jsonl`):

```json
{"creator_id": "attacker_MF05", "event": "rejected", "reason": "text_too_short", "status": "rejected", "timestamp": "2026-11-16T10:56:09+00:00"}
{"creator_id": "attacker_FP08", "event": "rejected", "reason": "text_too_short", "status": "rejected", "timestamp": "2026-11-16T10:56:08+00:00"}
```

**My five criteria, after** (`python run_checks.py --label after`, three trials, files
`results/checks_2026-11-16_0556_after.md` and `results/run_2026-11-16_0557_after.md`):

| Criterion                           | Before (3 trials) | After (3 trials)  | Verdict     |
| ----------------------------------- | ----------------- | ----------------- | ----------- |
| 1. Human writing flagged as AI      | 1/10, 1/10, 1/10  | 1/10, 1/10, 1/10  | MET both    |
| 2. Clear AI vs clear human separate | gap 0.24 x3       | gap 0.24 x3       | MISSED both |
| 3. All three labels reachable       | borderline 3/5 x3 | borderline 3/5 x3 | MISSED both |
| 4. Appeal always changes status     | 10/10 x3          | 10/10 x3          | MET both    |
| 5. Bad input rejected cleanly       | 9/9 x3            | 9/9 x3            | MET both    |

**Did it help, and how do I know:** yes, on exactly what it targeted. The malformed family went from
5 broke to 0, and the total from 19 to 13 broken, which is the number I predicted before making the
change. Every other result is identical to the before run, so the only things that moved are the 8 inputs
in the table above. My five criteria did not move at all (all of their inputs are over 20 words).

**What it cost:**

- **A real writer with a short submission is now refused.** FP08 ("Went for a run. Legs hurt. Worth it.", 8 words) used to get "unsure"; now it gets a 400. That is a genuine human piece rejected instead of judged, which is better than a wrong accusation but still a failure to serve them.
- **EV08 is a weak "held".** It was refused only because it is short, not because it was detected. A short AI text still can't be scored at all.
- **The flood test no longer tests scoring.** The 9-word flood text is now rejected on the first ten requests. The rate limiter still produced its 429s from request 11, but those first ten no longer went through the signals.
- It fixes only the "no real text" problem. 13 of 19 failures are untouched.

---

## What's Still Broken

13 of the 56 attacks still break and 2 of my 5 criteria are still missed. They come from three causes.
I fixed none of them. The one change I made targeted a fourth cause (text with no real words).

### Attacks still getting through

| Attacks                      | Cause                                                                                                                                                          | What I'd do                                                                                                                                                                                             | Why I stopped                                                                                                                                                                                                                                                                        |
| ---------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| EV02, EV03, EV06, EV07, EV09 | Signal two measures the shape of the whole text, and shape is cheap to change (an added one-word sentence, a pasted quotation, a human opening bolted on)      | Score style per sentence or per window, so one odd sentence can't drag the whole text. Also stop `sentence_length_spread == 0` (EV07, one giant sentence) from returning neutral 0.5 instead of AI-ish. | My arithmetic on the recorded scores showed reweighting doesn't remove the cause, so the real fix is a redesign of `stylometry.py`, not a tweak. It would also need new calibration against all my criteria, and I wasn't going to do that in this unit.                             |
| EV01, PI01, PI02             | Signal one rises in surprise for anything unusual, not just human writing (typos, a prefix)                                                                    | Detect and discount junk prefixes and typo-heavy spans before scoring.                                                                                                                                  | That is a new input-cleaning stage that guesses the writer's intent. I couldn't build it and show it doesn't hurt real human text in the time I had.                                                                                                                                 |
| EV05                         | Heavy human editing of AI text lowers both signals                                                                                                             | Nothing.                                                                                                                                                                                                | It is the attack working as intended. Two signals that measure predictability and shape can't see through real editing.                                                                                                                                                              |
| FP02, FP03, FP04, FP05       | Formal, plain, non-native or templated human writing is predictable and evenly shaped, so both signals agree it is AI and the "both must agree" cap can't help | Add a signal that doesn't reward plainness (for example, personal detail or revision traces), or ask for a longer sample. FP04 clears 0.65 by 0.004, so a threshold change would flip it.               | Moving the threshold to catch FP04 would be passing criterion 1 by editing the answer, which `criteria.md` rules out once testing starts. A third signal is more than the time left allows. These four are the ones I'd worry about most, since they are real writers being accused. |

Weak results I should not count as wins: EV08 is "held" only because 10 words is refused, not because the
AI text was detected. FP08 (a real 8-word human piece) is now refused instead of judged. If short texts
mattered, I'd want to score them with a looser rule and not refuse them.

### Criteria still missed

- **Criterion 2 (score spread): gap 0.24 against a target of 0.30, in all three trials.** AI text was fine
  (5/5 above 0.50) but only 3/5 of the human pieces were below 0.50. The cause is the same plain-human-writing
  problem as FP02–FP05, so the same fix applies (a signal that tells plain from generated). I didn't lower
  the target to 0.24, because that would be passing it by editing it.
- **Criterion 3 (label coverage): the labels part is met** (human 4, unsure 9, ai 2, each at least 2), **but
  only 3 of 5 borderline pieces landed in 0.40–0.60 against a target of 4.** "Unsure" is catching text it
  shouldn't, and the rest are scored with the same weak signals. I'd fix this with the better signals above,
  not by widening the band.

My improvement didn't move either criterion, because all their inputs are over 20 words and the check I
added never sees them. I stopped here because I had time for one fix, and I picked the one whose effect I
could predict and measure (19 broken to 13, as I predicted). The remaining fixes need redesign and
recalibration, not another small change, so I'd rather say that than ship a half-tested one.

**The trade I'd make if this ran for real:**

I would accept more AI text getting through before I would accuse more real writers, so I'd keep the AI
threshold high and put every borderline case in "unsure" with an appeal path. The people who pay are the
site and its honest readers, who see more undetected AI text, and I'd choose that over making formal,
plain or non-native writers (FP02–FP05) pay with a wrong accusation, since they are the ones this
detector gets wrong most.

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
