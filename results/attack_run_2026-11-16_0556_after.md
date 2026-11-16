# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-16 05:56
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `4b1be7ef-a983-4837-b505-83c0d0b00d3d` | unsure | 0.491 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `ef2bf9ee-ee04-4a67-9b95-532d9c1912bc` | human | 0.319 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `9977ac3a-156e-4aed-9d0b-ebfe455cdd94` | unsure | 0.448 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `edf94fb7-d780-480d-b52e-c5ce05bf0cc9` | ai | 0.660 | HELD |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `ea888673-ebcf-4961-b3a5-45f415d451a9` | human | 0.201 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `9938df39-7b2c-4fb5-b113-be74dfd45d6b` | unsure | 0.358 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | `4db9676d-9d49-40c1-b607-551fc5c99a19` | unsure | 0.453 | BROKE |
| EV08 | evasion | signal one: text below the token window | 400 | `—` | — | — | HELD |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `ded165e6-396b-4d4c-a730-8ece6c85503d` | unsure | 0.460 | BROKE |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `0e0f0395-8e78-4a73-b905-e9b26671b71b` | ai | 0.817 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `a3e46075-5b45-4159-a362-b8d331a08793` | unsure | 0.540 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `c9435665-701c-4b31-a867-56c2b95a364d` | ai | 0.779 | BROKE |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `1eb2a9bd-995a-417f-bff5-f424aa875518` | ai | 0.720 | BROKE |
| FP04 | false_positive | a student essay written to a rubric | 200 | `e31f0e25-b009-4d7e-b174-26511a8d7d26` | ai | 0.654 | BROKE |
| FP05 | false_positive | technical documentation written by a person | 200 | `b3b32c06-d5ab-47e3-a390-ec43727e4de1` | ai | 0.825 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | `727382ad-85cf-4fa7-835c-7099ee34cd04` | unsure | 0.573 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `924b427f-78e2-4a6a-8900-867cceaa2148` | unsure | 0.580 | HELD |
| FP08 | false_positive | very short genuine human submission | 400 | `—` | — | — | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `222b363a-c2c8-4edc-8394-62674cdcea7a` | human | 0.275 | BROKE |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `0b19d0ea-dc70-46f4-bddb-8d0d6c75553b` | human | 0.150 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `dd77c52b-af6f-421f-9891-0a992d273e8b` | unsure | 0.528 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `f053aace-3a7d-4092-b224-40f1f476a50f` | unsure | 0.420 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `893dc67c-5572-4019-a7a9-304b66ae9441` | unsure | 0.436 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `ee0cd066-da55-495a-9fb8-fc2df88769aa` | unsure | 0.512 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | `—` | — | — | HELD |
| MF03 | malformed | text is control characters | 400 | `—` | — | — | HELD |
| MF04 | malformed | text is only punctuation | 400 | `—` | — | — | HELD |
| MF05 | malformed | text is a very long single word | 400 | `—` | — | — | HELD |
| MF06 | malformed | text is emoji only | 400 | `—` | — | — | HELD |
| MF07 | malformed | text is right-to-left script | 400 | `—` | — | — | HELD |
| MF08 | malformed | text is 60,000 characters | 413 | `—` | — | — | HELD |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — | HELD |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — | HELD |
| RQ03 | malformed | text is a number | 400 | `—` | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | `—` | — | — | HELD |
| RQ05 | malformed | text is null | 400 | `—` | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | `—` | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 400 | `—` | — | — | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 400 | `—` | — | — | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 400 | `—` | — | — | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 400 | `—` | — | — | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 400 | `—` | — | — | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 400 | `—` | — | — | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 400 | `—` | — | — | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 400 | `—` | — | — | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 400 | `—` | — | — | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 400 | `—` | — | — | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "4b1be7ef-a983-4837-b505-83c0d0b00d3d",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.491,
  "model_score": 0.1635,
  "style_score": 0.7094,
  "label": "We can't tell whether this was written by a person or with the help of AI. That isn't a judgment against you. If you wrote it yourself, there's nothing you need to do, and you can ask us to take another look at any time.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "ef2bf9ee-ee04-4a67-9b95-532d9c1912bc",
  "creator_id": "attacker_EV02",
  "guess": "human",
  "confidence": 0.3191,
  "model_score": 0.5943,
  "style_score": 0.1356,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "9977ac3a-156e-4aed-9d0b-ebfe455cdd94",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.4475,
  "model_score": 0.6662,
  "style_score": 0.3017,
  "label": "We can't tell whether this was written by a person or with the help of AI. That isn't a judgment against you. If you wrote it yourself, there's nothing you need to do, and you can ask us to take another look at any time.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "edf94fb7-d780-480d-b52e-c5ce05bf0cc9",
  "creator_id": "attacker_EV04",
  "guess": "ai",
  "confidence": 0.6602,
  "model_score": 0.6114,
  "style_score": 0.6928,
  "label": "Our check thinks this may have been written with the help of AI. Checks like ours can be wrong, especially with plain, simple writing. If you wrote this yourself, please tell us and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "ea888673-ebcf-4961-b3a5-45f415d451a9",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.2005,
  "model_score": 0.3212,
  "style_score": 0.12,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "9938df39-7b2c-4fb5-b113-be74dfd45d6b",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.3577,
  "model_score": 0.5727,
  "style_score": 0.2144,
  "label": "We can't tell whether this was written by a person or with the help of AI. That isn't a judgment against you. If you wrote it yourself, there's nothing you need to do, and you can ask us to take another look at any time.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "4db9676d-9d49-40c1-b607-551fc5c99a19",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.4529,
  "model_score": 0.5862,
  "style_score": 0.364,
  "label": "We can't tell whether this was written by a person or with the help of AI. That isn't a judgment against you. If you wrote it yourself, there's nothing you need to do, and you can ask us to take another look at any time.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_EV08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "ded165e6-396b-4d4c-a730-8ece6c85503d",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.4602,
  "model_score": 0.7042,
  "style_score": 0.2976,
  "label": "We can't tell whether this was written by a person or with the help of AI. That isn't a judgment against you. If you wrote it yourself, there's nothing you need to do, and you can ask us to take another look at any time.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "0e0f0395-8e78-4a73-b905-e9b26671b71b",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.8171,
  "model_score": 0.9792,
  "style_score": 0.7091,
  "label": "Our check thinks this may have been written with the help of AI. Checks like ours can be wrong, especially with plain, simple writing. If you wrote this yourself, please tell us and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "a3e46075-5b45-4159-a362-b8d331a08793",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.5402,
  "model_score": 0.6175,
  "style_score": 0.4887,
  "label": "We can't tell whether this was written by a person or with the help of AI. That isn't a judgment against you. If you wrote it yourself, there's nothing you need to do, and you can ask us to take another look at any time.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "c9435665-701c-4b31-a867-56c2b95a364d",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.7789,
  "model_score": 0.7387,
  "style_score": 0.8057,
  "label": "Our check thinks this may have been written with the help of AI. Checks like ours can be wrong, especially with plain, simple writing. If you wrote this yourself, please tell us and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "1eb2a9bd-995a-417f-bff5-f424aa875518",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.7202,
  "model_score": 0.8051,
  "style_score": 0.6636,
  "label": "Our check thinks this may have been written with the help of AI. Checks like ours can be wrong, especially with plain, simple writing. If you wrote this yourself, please tell us and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "e31f0e25-b009-4d7e-b174-26511a8d7d26",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.6537,
  "model_score": 0.8329,
  "style_score": 0.5343,
  "label": "Our check thinks this may have been written with the help of AI. Checks like ours can be wrong, especially with plain, simple writing. If you wrote this yourself, please tell us and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "b3b32c06-d5ab-47e3-a390-ec43727e4de1",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.8254,
  "model_score": 0.8005,
  "style_score": 0.842,
  "label": "Our check thinks this may have been written with the help of AI. Checks like ours can be wrong, especially with plain, simple writing. If you wrote this yourself, please tell us and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "727382ad-85cf-4fa7-835c-7099ee34cd04",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.5731,
  "model_score": 0.8814,
  "style_score": 0.3676,
  "label": "We can't tell whether this was written by a person or with the help of AI. That isn't a judgment against you. If you wrote it yourself, there's nothing you need to do, and you can ask us to take another look at any time.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "924b427f-78e2-4a6a-8900-867cceaa2148",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.5802,
  "model_score": 0.8816,
  "style_score": 0.3792,
  "label": "We can't tell whether this was written by a person or with the help of AI. That isn't a judgment against you. If you wrote it yourself, there's nothing you need to do, and you can ask us to take another look at any time.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_FP08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "222b363a-c2c8-4edc-8394-62674cdcea7a",
  "creator_id": "attacker_PI01",
  "guess": "human",
  "confidence": 0.275,
  "model_score": 0.4625,
  "style_score": 0.15,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "0b19d0ea-dc70-46f4-bddb-8d0d6c75553b",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.1497,
  "model_score": 0.2044,
  "style_score": 0.1133,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "dd77c52b-af6f-421f-9891-0a992d273e8b",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.5279,
  "model_score": 0.5943,
  "style_score": 0.4836,
  "label": "We can't tell whether this was written by a person or with the help of AI. That isn't a judgment against you. If you wrote it yourself, there's nothing you need to do, and you can ask us to take another look at any time.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "f053aace-3a7d-4092-b224-40f1f476a50f",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.4203,
  "model_score": 0.4998,
  "style_score": 0.3673,
  "label": "We can't tell whether this was written by a person or with the help of AI. That isn't a judgment against you. If you wrote it yourself, there's nothing you need to do, and you can ask us to take another look at any time.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "893dc67c-5572-4019-a7a9-304b66ae9441",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.436,
  "model_score": 0.6401,
  "style_score": 0.3,
  "label": "We can't tell whether this was written by a person or with the help of AI. That isn't a judgment against you. If you wrote it yourself, there's nothing you need to do, and you can ask us to take another look at any time.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "ee0cd066-da55-495a-9fb8-fc2df88769aa",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.5125,
  "model_score": 0.5583,
  "style_score": 0.4819,
  "label": "We can't tell whether this was written by a person or with the help of AI. That isn't a judgment against you. If you wrote it yourself, there's nothing you need to do, and you can ask us to take another look at any time.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF06",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF07",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 413,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
