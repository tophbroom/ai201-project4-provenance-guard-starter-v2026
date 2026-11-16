"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

Two are filled in as examples. Replace them with what your criteria actually
need — these are a shape, not a set.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.
"""

# Criterion 1 data: ten pre-AI human-written Reddit comments, NOT the author's
# own writing (the author had no personal corpus). They are certainly human
# because they predate AI text generators. Pieces 1, 5, 7, 9 and 10 are the
# deliberately plain ones. Typos and awkward phrasing are left as written.
HUMAN_OWN = [
    """I usually use second person, like talking to myself but it's not really myself but an alter-ego, more careless version of myself and I keep patronizing that person through insults and advice which in turn helps me keep myself in control hahahahahah

It's like that friend you got that's always thinking dumb things and you gotta keep reminding him of what is correct and what's not, so I don't feel awkward as addressing that guy as myself and feel like my communication skills are enhanced by having "someone" by my side all day at all moments, summoned at will, who is always listening to my nonsense and is always paying attention.

I think it helps the most with improving your communication skills and decision-making processes.""",
    """At first I was shocked at how easy it was, and how far I didn't have to go in order to just... be somewhere and someone else, where no one knew me, and I was new again. I am from a small town of < 20k, so I was used to everybody knowing everyone and everyone knowing everybody's business-- including mine. Which made my crumbling marriage and soon-to-be divorce all the less palatable to my mid-twenties mindset. I knew she was leaving, so when she walked out the door for good, I decided rather than hear and be disposed to the gossip of town that I would Don Draper this life. Well... minus ID fraud.""",
    """Yep, this coupled with something someone said above you is exactly right. Do not EVER assume and think for other people. Don't make the assumption your friends don't care about you and let that prevent you from getting support you need. They most probably do care, at least some. And they either truly don't know because its not that easy to know for various reasons. One being they have shit of their own, another being that not everyone stick their heads into other people's lives without being premission to.""",
    """Holy shit, your writing is so clear. You know the perfect balance when setting a scene for your audience. You describe enough so that we have an idea but not too much that it breaks the flow. And the way you use literary devices and sentence fragments like \u201cbuzz\u201d or \u201cIn it goes\u201d creates such a vivid read. And, you know how to perfectly control a reader\u2019s stream of consciousness, how fast or how slow we\u2019re reading in the way to mimic your actual experience. Through mere words you can instill the emotions of your experiences into our hearts. That\u2019s not easy.""",
    """I've tried berries and stuff in oatmeal and I can never get into it. I think it's because this is how my mom made oatmeal for me, so all these years later it's what my brain recognizes as oatmeal? I don't know, but I've been eating it for almost every morning for like five years or so and I'm still not sick of it.""",
    """As a Salsa dancer, I have met many people who are single, dating and married. Some have partners who dance. Some don\u2019t. Some have partners who dance different styles (men and women). The general theme is that they are all secure in their relationships. Yes you will get flirters here and there as you will in almost any partner dancing. However, the partner dance community, especially in Salsa, as it is unfortunately more common to get hit on, self police\u2019s that real well.""",
    """I\u2019ve never even thought about saving leftover coffee for another day, but if you refrigerate it so it doesn\u2019t go bad, it should be ok to reheat and drink. A lot of places sell plain coffee or coffee drinks in the refrigerated section of their store. So, why not?""",
    """A simplified answer, but not necessarily a wrong one. I agree that people rarely want to say no, and some people don't even KNOW HOW to say no. I just feel like more directness in conversations can lead to less confusion and a more interesting conversation. Saying no can definitely appear to be rude to say in some circumstances, but I'd rather be honest than giving people a false sense of "hope". I just feel like saying maybe is a way to sugarcoat your answer.""",
    """I think there are a segment of maybe answer givers who just have trouble making a decision on the spot. They need time to think about their answer or they have circumstances where it is hard to make future plans. A maybe is sometimes not a no but a I can't answer this right now.""",
    """Let it go. Don't give other people power to control your emotions, don't be a victim. The people you're holding a grudge against probably don't care, while you're allowing something they did to continuously anger you. I know it's easier said then done, but there's no benefit to holding grudges, so try to work on forgiving each person, and moving on with your life. You don't need to become close or best friends with them. Also, the past are just memories. You don't live in the past, you live in the present, so stop letting the past affect your present, otherwise you'll always be angry about something.""",
]

AI_TEXTS = [
    open("samples/ai.txt", encoding="utf-8").read(),
    "The importance of effective communication in the workplace cannot be overstated. Teams that communicate clearly are better positioned to achieve their objectives and avoid costly misunderstandings. Furthermore, organizations that foster open dialogue tend to experience higher levels of employee engagement and satisfaction.",
    "Artificial intelligence has the potential to transform numerous industries by automating routine tasks and enabling data-driven decision making. However, it is essential to consider the ethical implications of these technologies. By implementing robust governance frameworks, organizations can ensure responsible and equitable outcomes.",
    "Sustainable development requires a holistic approach that balances economic growth, environmental protection, and social equity. Stakeholders across sectors must collaborate to implement effective strategies. In conclusion, a commitment to long-term thinking is essential for building a resilient future.",
    "Time management is a critical skill that can significantly enhance both personal and professional productivity. By prioritizing tasks, setting clear goals, and minimizing distractions, individuals can achieve greater efficiency. Ultimately, mastering this skill leads to improved well-being and success.",
]

HUMAN_CLEAR = [
    open("samples/human.txt", encoding="utf-8").read(),
    open("samples/human2.txt", encoding="utf-8").read(),
    HUMAN_OWN[1], HUMAN_OWN[5], HUMAN_OWN[9],
]

BORDERLINE = [
    open("samples/mixed.txt", encoding="utf-8").read(),
    "Remote work offers flexibility, but it also blurs the line between home and job. I found that setting a clear end to the day helped me a lot, even though I still check email at night more than I'd like to admit.",
    "Many students struggle with procrastination. In my experience it comes from anxiety more than laziness, because the task feels too big to start. Breaking it into small steps tends to help, though not always.",
    "Public libraries remain valuable community spaces. They offer free access to books, computers, and quiet rooms, and I have personally relied on all three. It would be a loss if funding kept shrinking.",
    "Social media can connect people across distances, yet it can also leave them feeling more alone. I deleted the apps for a month and felt calmer, but I also missed hearing from a few friends.",
]

SCENARIOS = [
    {"name": "human comments flagged as AI", "criterion": 1, "texts": HUMAN_OWN},
    {"name": "score spread: AI pieces", "criterion": 2, "texts": AI_TEXTS},
    {"name": "score spread: human pieces", "criterion": 2, "texts": HUMAN_CLEAR},
    {"name": "label coverage: clear AI", "criterion": 3, "texts": AI_TEXTS},
    {"name": "label coverage: clear human", "criterion": 3, "texts": HUMAN_CLEAR},
    {"name": "label coverage: borderline", "criterion": 3, "texts": BORDERLINE},
    # Criterion 4 (appeal path) needs a submit then an appeal: see run_checks.py
    {
        "name": "bad input",
        "criterion": 5,
        "bodies": [
            {"text": "", "creator_id": "eval_bad_empty"},
            {"text": "   \n\t ", "creator_id": "eval_bad_ws"},
            {"creator_id": "eval_bad_missing"},
            {"text": None, "creator_id": "eval_bad_null"},
            {"text": 12345, "creator_id": "eval_bad_nonstring"},
            {"text": "Real writing here but no creator at all."},
            {"text": "word " * 50000, "creator_id": "eval_bad_huge"},
            {"text": "Hi", "creator_id": "eval_bad_short"},
            # a non-object body (a JSON list) is sent by run_checks.py; bodies here must be dicts
        ],
    },
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
