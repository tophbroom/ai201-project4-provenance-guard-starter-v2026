# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1. False positives: my own writing is rarely called AI

Of 10 pieces I wrote myself (at least 3 of them deliberately plain: short
sentences, simple words), at most 1 gets the high-confidence AI label
(combined score above `AI_THRESHOLD`). This must hold in each of the three
trials, not on average. No piece may score above 0.80.

**Why this target:**

On a writing site a wrong accusation costs the writer far more than a missed
detection costs the site, so I allow at most 1 in 10. The plain pieces are
there because my milestone 1 trace predicted that a plainly-written human
essay would score high on both signals. I haven't measured that yet, so these
pieces are how I find out. Testing only my ornate writing would make the
target too easy to hit. The 0.80 ceiling stops a single piece from being
confidently wrong by a wide margin. `AI_THRESHOLD` is fixed once I start
testing, because raising it afterward would pass this target without
improving anything.

---

## 2. Score spread: clear AI and clear human text separate

Take 5 pieces I'm confident are AI-generated and 5 I'm confident a human
wrote. The mean combined score of the AI set must be at least 0.30 higher than
the mean of the human set, and at least 4 of the 5 AI pieces must score above
0.50 while at least 4 of the 5 human pieces score below 0.50. This holds in
every trial.

**Why this target:**

A detector whose scores sit in a narrow cluster can't support three labels, so
I need the gap itself to be a number. 0.30 is about the width of my unsure
band (0.35 to 0.65), so a gap that size means clear cases land on opposite
sides of it. I'm not asking for 5 of 5, because GPT-2 is a weak detector of
newer models and I'd rather set a target I can defend than one I can't meet.

---

## 3. Label coverage: all three labels are reachable

Across a set of at least 12 inputs spanning clearly-AI, clearly-human and
borderline text, each of the three labels (high-confidence human, unsure,
high-confidence AI) is produced at least twice, in each of the three trials.
For 5 pieces I judged borderline, at least 4 score between 0.40 and 0.60.

**Why this target:**

`config.py` warns that with a stub style signal the human label may be
unreachable, and a label nobody can reach is a bug that looks like a design.
Requiring two hits per label, not one, keeps a single lucky score from
counting. The borderline check makes sure "unsure" means uncertain and isn't a
catch-all that other texts fall into by default.

---

## 4. The appeal path: every appeal changes status and is recorded

For 10 appeals on valid `content_id`s, all 10 return 200 with status
`under_review`, and each adds exactly one new entry to `logs/audit.jsonl`
containing the writer's `reasoning` and the `creator_id` copied from the
original decision. The original decision entry is byte-for-byte unchanged.
An appeal on an unknown `content_id` returns 404 and adds no appeal entry
(a `rejected` entry is fine and expected). 0 failures allowed.

**Why this target:**

The appeal is the only protection a wrongly flagged writer has (milestone 1),
so it can't be allowed to fail even once. Unlike the scores, this behavior is
deterministic and involves no model, so a target of 10 out of 10 is fair and
a single miss would mean a real bug. Checking that the original entry is
unchanged protects the audit trail.

---

## 5. Bad input: malformed requests are rejected cleanly

Send 9 bad requests: empty text, whitespace-only text, missing `text`, null
`text`, non-string `text`, missing `creator_id`, one text over the 20,000
character cap, a text too short to score (such as "Hi"), and a body that isn't
a JSON object. All 9 return a 4xx status (400, or 413 for the oversized one)
with a JSON `error` field. 0 return a 500
or crash the service, and each writes a `rejected` entry to the log and no
decision entry.

**Why this target:**

The service runs a 550 MB model inline, so an enormous or malformed input that
reaches it can hang the service or take it down for everyone. The contract I
wrote in milestone 1 already names each of these cases, so the target is
simply that the code does what I said it would. As with the appeal path, there
is no randomness here, so I allow 0 failures.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
