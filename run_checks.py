#!/usr/bin/env python3
"""
Score the five criteria in criteria.md against the running service.

    python app.py                        # one terminal
    python run_checks.py --label before  # another

`run_eval.py` sends the /submit scenarios and records raw output. This script
does what it can't: it runs the appeal flow (criterion 4), reads the audit log
to check what each request left behind (criteria 4 and 5), and compares every
trial with the target written in criteria.md. Targets are copied from that file
and are never loosened here.
"""

import argparse
import datetime as dt
import json
import sys

import requests

import config
import scenarios

URL = f"http://{config.HOST}:{config.PORT}"


def post(path, body, timeout=90):
    r = requests.post(f"{URL}{path}", json=body, timeout=timeout)
    try:
        payload = r.json()
    except ValueError:
        payload = {"_non_json": r.text[:200]}
    return r.status_code, payload


def log():
    return requests.get(f"{URL}/log", timeout=30).json()["entries"]


def submit_all(texts, prefix):
    out = []
    for i, text in enumerate(texts, 1):
        status, p = post("/submit", {"text": text, "creator_id": f"{prefix}_{i}"})
        out.append({"status": status, "guess": p.get("guess"),
                    "confidence": p.get("confidence"),
                    "model_score": p.get("model_score"),
                    "style_score": p.get("style_score"),
                    "content_id": p.get("content_id"),
                    "sent": text[:60]})
    return out


# ── criterion 1 ───────────────────────────────────────────────────────────────
def c1(tag):
    res = submit_all(scenarios.HUMAN_OWN, f"chk_{tag}_c1")
    flagged = sum(r["guess"] == "ai" for r in res)
    top = max((r["confidence"] or 0) for r in res)
    ok = flagged <= 1 and top <= 0.80 and all(r["status"] == 200 for r in res)
    return ok, f"{flagged}/10 flagged AI, max {top:.2f}", res


# ── criterion 2 ───────────────────────────────────────────────────────────────
def c2(tag):
    ai = submit_all(scenarios.AI_TEXTS, f"chk_{tag}_c2ai")
    hu = submit_all(scenarios.HUMAN_CLEAR, f"chk_{tag}_c2hu")
    mean = lambda rs: sum(r["confidence"] for r in rs) / len(rs)
    gap = mean(ai) - mean(hu)
    ai_hi = sum(r["confidence"] > 0.5 for r in ai)
    hu_lo = sum(r["confidence"] < 0.5 for r in hu)
    ok = gap >= 0.30 and ai_hi >= 4 and hu_lo >= 4
    return ok, f"gap {gap:.2f}, AI>0.5 {ai_hi}/5, human<0.5 {hu_lo}/5", {"ai": ai, "human": hu}


# ── criterion 3 ───────────────────────────────────────────────────────────────
def c3(tag):
    ai = submit_all(scenarios.AI_TEXTS, f"chk_{tag}_c3ai")
    hu = submit_all(scenarios.HUMAN_CLEAR, f"chk_{tag}_c3hu")
    bo = submit_all(scenarios.BORDERLINE, f"chk_{tag}_c3bo")
    counts = {g: sum(r["guess"] == g for r in ai + hu + bo) for g in ("human", "unsure", "ai")}
    in_band = sum(0.40 <= r["confidence"] <= 0.60 for r in bo)
    ok = all(v >= 2 for v in counts.values()) and in_band >= 4
    return ok, (f"human {counts['human']}, unsure {counts['unsure']}, ai {counts['ai']}; "
                f"borderline in 0.40-0.60: {in_band}/5"), {"ai": ai, "human": hu, "borderline": bo}


# ── criterion 4 ───────────────────────────────────────────────────────────────
def c4(tag):
    texts = (scenarios.HUMAN_OWN)[:10]
    rows, passed = [], 0
    for i, text in enumerate(texts, 1):
        status, sub = post("/submit", {"text": text, "creator_id": f"chk_{tag}_c4_{i}"})
        cid = sub.get("content_id")
        before = [e for e in log() if e.get("content_id") == cid]
        original = before[0] if before else None
        a_status, a = post("/appeal", {"content_id": cid, "reasoning": f"I wrote this myself ({i})."})
        after = [e for e in log() if e.get("content_id") == cid]
        new = after[len(before):]
        good = (
            a_status == 200 and a.get("status") == "under_review"
            and len(new) == 1 and new[0].get("event") == "appeal"
            and new[0].get("reasoning") == f"I wrote this myself ({i})."
            and original is not None and new[0].get("creator_id") == original.get("creator_id")
            and after[0] == original
        )
        passed += good
        rows.append({"content_id": cid, "appeal_status": a_status, "appeal_response": a,
                     "new_log_entries": new, "ok": good})
    # unknown id: 404 and no appeal entry
    n_before = len(log())
    u_status, u = post("/appeal", {"content_id": "does-not-exist", "reasoning": "test"})
    new = log()[n_before:]
    unknown_ok = u_status == 404 and not any(e.get("event") == "appeal" for e in new)
    rows.append({"unknown_id_status": u_status, "response": u, "new_log_entries": new, "ok": unknown_ok})
    ok = passed == 10 and unknown_ok
    return ok, f"{passed}/10 appeals ok, unknown id {'404 ok' if unknown_ok else 'WRONG'}", rows


# ── criterion 5 ───────────────────────────────────────────────────────────────
def c5(tag):
    c = f"chk_{tag}_c5"
    bad = [
        ("empty text", {"text": "", "creator_id": f"{c}_a"}),
        ("whitespace text", {"text": "   \n\t ", "creator_id": f"{c}_b"}),
        ("missing text", {"creator_id": f"{c}_c"}),
        ("null text", {"text": None, "creator_id": f"{c}_d"}),
        ("non-string text", {"text": 12345, "creator_id": f"{c}_e"}),
        ("missing creator_id", {"text": "Real writing here but no creator at all."}),
        ("over 20,000 chars", {"text": "word " * 5000, "creator_id": f"{c}_g"}),
        ("too short", {"text": "Hi", "creator_id": f"{c}_h"}),
        ("not a JSON object", ["text", "creator_id"]),
    ]
    rows, passed = [], 0
    for name, body in bad:
        before = len(log())
        status, p = post("/submit", body)
        new = log()[before:]
        rejected = [e for e in new if e.get("event") == "rejected"]
        decisions = [e for e in new if "event" not in e]
        good = 400 <= status < 500 and "error" in p and rejected and not decisions
        passed += bool(good)
        rows.append({"case": name, "status": status, "response": p,
                     "new_log_entries": new, "ok": bool(good)})
    return passed == 9, f"{passed}/9 rejected cleanly", rows


CRITERIA = [
    (1, "Human writing flagged as AI", "≤ 1 of 10, none > 0.80", c1),
    (2, "Clear AI vs clear human separate", "gap ≥ 0.30, ≥4/5 each side", c2),
    (3, "All three labels reachable", "each label ≥ 2; ≥4/5 borderline in 0.40–0.60", c3),
    (4, "Appeal always changes status and is logged", "10/10 + 404 on unknown", c4),
    (5, "Bad input rejected cleanly", "9/9, no 500s", c5),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trials", type=int, default=3)
    ap.add_argument("--label", default="")
    args = ap.parse_args()

    try:
        requests.get(f"{URL}/health", timeout=5)
    except Exception:  # noqa: BLE001
        sys.exit(f"Nothing answering at {URL}. Start it:  python app.py")

    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    run_id = stamp.replace("-", "").replace("_", "")
    results = {n: [] for n, *_ in CRITERIA}
    for t in range(1, args.trials + 1):
        print(f"\n== trial {t} ==")
        for n, name, _, fn in CRITERIA:
            try:
                ok, summary, raw = fn(f"{run_id}t{t}")
            except Exception as exc:  # noqa: BLE001
                ok, summary, raw = False, f"ERROR {type(exc).__name__}: {exc}", None
            results[n].append({"ok": ok, "summary": summary, "raw": raw})
            print(f"  {n}. {name}: {'MET' if ok else 'MISSED'} — {summary}")

    label = f"_{args.label}" if args.label else ""
    path = config.RESULTS_DIR / f"checks_{stamp}{label}.md"
    lines = [f"# Criteria check{f' — {args.label}' if args.label else ''}", "",
             "- Produced by: `run_checks.py` (calls `app.py::submit` and `app.py::appeal`)",
             f"- {args.trials} trials · {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}", "",
             "| Criterion | Target | " + " | ".join(f"Run {i}" for i in range(1, args.trials + 1)) + " | Verdict |",
             "|---|---|" + "---|" * args.trials + "---|"]
    for n, name, target, _ in CRITERIA:
        rs = results[n]
        verdict = "MET" if all(r["ok"] for r in rs) else "MISSED"
        lines.append(f"| {n}. {name} | {target} | " + " | ".join(r["summary"] for r in rs) + f" | {verdict} |")
    lines += ["", "---", "", "## Raw output", ""]
    for n, name, _, _ in CRITERIA:
        for t, r in enumerate(results[n], 1):
            lines += [f"### Criterion {n} — trial {t}", "", "```json",
                      json.dumps(r["raw"], indent=2, ensure_ascii=False), "```", ""]
    config.RESULTS_DIR.mkdir(exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {path.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
