# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-16 04:30
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
| EV01 | evasion | signal two: typos raise word variety | 200 | `0b6be86f-69d1-4cd8-b9d4-f0ce58ce28cc` | unsure | 0.491 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `d1c49afa-e369-45e3-a5e5-86051dee06c3` | human | 0.319 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `ac898fe8-5dc5-4354-af25-08efdae8f52f` | unsure | 0.448 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `58890389-71e2-4da8-a2f0-dbc0227861a8` | ai | 0.660 | HELD |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `58d472bd-da0b-4516-9122-c382f5b6d72a` | human | 0.201 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `35e703cc-616e-4140-9c96-a4f2a82623b8` | unsure | 0.358 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | `70988820-d094-4f8b-b2ff-65d829185283` | unsure | 0.453 | BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | `eed4eb8e-a919-4575-8cf2-463a56a1eb43` | unsure | 0.398 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `3722c838-060a-4baf-8aef-49b4fdb0e21a` | unsure | 0.460 | BROKE |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `e60bcf76-870f-4aa4-a737-aa48b579e40a` | ai | 0.817 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `6b78f29c-c3eb-4759-a02f-8ee515fd1194` | unsure | 0.540 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `96a45635-1b18-4429-a420-c0e96cceb59c` | ai | 0.779 | BROKE |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `d8a2b6d0-7abd-4541-8288-bf33049c459e` | ai | 0.720 | BROKE |
| FP04 | false_positive | a student essay written to a rubric | 200 | `eec3c845-737e-4602-bb8a-105039aec40a` | ai | 0.654 | BROKE |
| FP05 | false_positive | technical documentation written by a person | 200 | `bbb6ed8b-a309-457e-8777-4ee992ee2099` | ai | 0.825 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | `be92929c-31a5-46bd-93f0-9b59e86d36d9` | unsure | 0.573 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `34e5ffbf-77a9-4ac0-8b8c-42234585ea72` | unsure | 0.580 | HELD |
| FP08 | false_positive | very short genuine human submission | 200 | `1b9496bf-c24c-4ce3-a78f-9b72db3acdf0` | unsure | 0.429 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `a1c7e51f-8a07-4f86-b2db-be8e42ce4cf4` | human | 0.275 | BROKE |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `b197f420-623a-436c-b5ef-a64b41149e07` | human | 0.150 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `f2368bb0-73b6-405a-8dab-2eb59a1c8239` | unsure | 0.528 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `b8129e0b-50fc-49bb-a07e-d9e8415d783d` | unsure | 0.420 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `389bcd85-098e-498a-8ea1-f9570a5707d1` | unsure | 0.436 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `a7ed2bab-dac2-42af-816e-1543f0271388` | unsure | 0.512 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | `—` | — | — | HELD |
| MF03 | malformed | text is control characters | 200 | `faeddd5d-949d-4f8c-af5f-80eebfb0c32f` | human | 0.300 | BROKE |
| MF04 | malformed | text is only punctuation | 200 | `62320ff4-c798-4be6-bd12-34d819634509` | human | 0.304 | BROKE |
| MF05 | malformed | text is a very long single word | 200 | `c7f1b930-fdba-4e70-8a9f-1f6153e4d241` | ai | 0.699 | BROKE |
| MF06 | malformed | text is emoji only | 200 | `9d806179-7b69-4f43-ba90-bc5028a938a8` | ai | 0.699 | BROKE |
| MF07 | malformed | text is right-to-left script | 200 | `fb067888-9083-443d-8b9e-e9af8e79c49c` | ai | 0.663 | BROKE |
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
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `931486fb-3a7b-40ae-9f72-80b36345fa8e` | human | 0.311 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `f90b2a87-8349-4122-a49d-7cfb6f06f21c` | human | 0.311 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `2b50fe30-c493-4400-9196-f2b9068b4d61` | human | 0.311 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `cd743fba-0f0b-4f86-be52-f872f8ad29ff` | human | 0.311 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `3e9f6a88-0b13-4ddd-9fbb-fc96e12323a7` | human | 0.311 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `699109be-d196-41d1-97a1-019bcd1cad6a` | human | 0.311 | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `584a7699-9b0b-4ea3-b77f-57028d7f4979` | human | 0.311 | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `f7a61af0-d5d2-42c4-ac1a-5ddf7600dfee` | human | 0.311 | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `93da5c02-4694-43c1-866b-73e890df9f62` | human | 0.311 | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `8fc1f34a-3744-42c6-b61f-50a44d9ffa5e` | human | 0.311 | HELD |
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
  "content_id": "0b6be86f-69d1-4cd8-b9d4-f0ce58ce28cc",
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
  "content_id": "d1c49afa-e369-45e3-a5e5-86051dee06c3",
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
  "content_id": "ac898fe8-5dc5-4354-af25-08efdae8f52f",
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
  "content_id": "58890389-71e2-4da8-a2f0-dbc0227861a8",
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
  "content_id": "58d472bd-da0b-4516-9122-c382f5b6d72a",
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
  "content_id": "35e703cc-616e-4140-9c96-a4f2a82623b8",
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
  "content_id": "70988820-d094-4f8b-b2ff-65d829185283",
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
  "status": 200,
  "content_id": "eed4eb8e-a919-4575-8cf2-463a56a1eb43",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.3981,
  "model_score": 0.2452,
  "style_score": 0.5,
  "label": "We can't tell whether this was written by a person or with the help of AI. That isn't a judgment against you. If you wrote it yourself, there's nothing you need to do, and you can ask us to take another look at any time.",
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
  "content_id": "3722c838-060a-4baf-8aef-49b4fdb0e21a",
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
  "content_id": "e60bcf76-870f-4aa4-a737-aa48b579e40a",
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
  "content_id": "6b78f29c-c3eb-4759-a02f-8ee515fd1194",
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
  "content_id": "96a45635-1b18-4429-a420-c0e96cceb59c",
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
  "content_id": "d8a2b6d0-7abd-4541-8288-bf33049c459e",
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
  "content_id": "eec3c845-737e-4602-bb8a-105039aec40a",
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
  "content_id": "bbb6ed8b-a309-457e-8777-4ee992ee2099",
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
  "content_id": "be92929c-31a5-46bd-93f0-9b59e86d36d9",
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
  "content_id": "34e5ffbf-77a9-4ac0-8b8c-42234585ea72",
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
  "status": 200,
  "content_id": "1b9496bf-c24c-4ce3-a78f-9b72db3acdf0",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.4289,
  "model_score": 0.3223,
  "style_score": 0.5,
  "label": "We can't tell whether this was written by a person or with the help of AI. That isn't a judgment against you. If you wrote it yourself, there's nothing you need to do, and you can ask us to take another look at any time.",
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
  "content_id": "a1c7e51f-8a07-4f86-b2db-be8e42ce4cf4",
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
  "content_id": "b197f420-623a-436c-b5ef-a64b41149e07",
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
  "content_id": "f2368bb0-73b6-405a-8dab-2eb59a1c8239",
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
  "content_id": "b8129e0b-50fc-49bb-a07e-d9e8415d783d",
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
  "content_id": "389bcd85-098e-498a-8ea1-f9570a5707d1",
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
  "content_id": "a7ed2bab-dac2-42af-816e-1543f0271388",
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
  "status": 200,
  "content_id": "faeddd5d-949d-4f8c-af5f-80eebfb0c32f",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.3,
  "model_score": 0.0,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "62320ff4-c798-4be6-bd12-34d819634509",
  "creator_id": "attacker_MF04",
  "guess": "human",
  "confidence": 0.3045,
  "model_score": 0.0112,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "c7f1b930-fdba-4e70-8a9f-1f6153e4d241",
  "creator_id": "attacker_MF05",
  "guess": "ai",
  "confidence": 0.699,
  "model_score": 0.9976,
  "style_score": 0.5,
  "label": "Our check thinks this may have been written with the help of AI. Checks like ours can be wrong, especially with plain, simple writing. If you wrote this yourself, please tell us and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "9d806179-7b69-4f43-ba90-bc5028a938a8",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.6988,
  "model_score": 0.9969,
  "style_score": 0.5,
  "label": "Our check thinks this may have been written with the help of AI. Checks like ours can be wrong, especially with plain, simple writing. If you wrote this yourself, please tell us and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "fb067888-9083-443d-8b9e-e9af8e79c49c",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.6626,
  "model_score": 0.9064,
  "style_score": 0.5,
  "label": "Our check thinks this may have been written with the help of AI. Checks like ours can be wrong, especially with plain, simple writing. If you wrote this yourself, please tell us and a person will take a look.",
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
  "status": 200,
  "content_id": "931486fb-3a7b-40ae-9f72-80b36345fa8e",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3115,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "f90b2a87-8349-4122-a49d-7cfb6f06f21c",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3115,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "2b50fe30-c493-4400-9196-f2b9068b4d61",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3115,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "cd743fba-0f0b-4f86-be52-f872f8ad29ff",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3115,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "3e9f6a88-0b13-4ddd-9fbb-fc96e12323a7",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3115,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 200,
  "content_id": "699109be-d196-41d1-97a1-019bcd1cad6a",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3115,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 200,
  "content_id": "584a7699-9b0b-4ea3-b77f-57028d7f4979",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3115,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 200,
  "content_id": "f7a61af0-d5d2-42c4-ac1a-5ddf7600dfee",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3115,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 200,
  "content_id": "93da5c02-4694-43c1-866b-73e890df9f62",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3115,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 200,
  "content_id": "8fc1f34a-3744-42c6-b61f-50a44d9ffa5e",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3115,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
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
