"""
Signal two: the style signal. ← YOU BUILD THIS IN MILESTONE 4

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

Three measures are stubbed below because the brief names those three. They are
stubs, not implementations: what they compute is yours, and so is how you
combine them.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Build each function on its own and call it from a terminal before you wire
anything together:

    python stylometry.py "some text to look at"
"""

import re
import statistics

TTR_WINDOW = 100

# Below this many words there isn't enough text to read a shape from.
MIN_WORDS_FOR_STYLE = 20

# How each raw measure maps to 0–1 AI-ness: the raw value that counts as fully
# AI-ish, and the raw value that counts as fully human-ish.
SPREAD_AI, SPREAD_HUMAN = 0.20, 0.60   # sentence-length coefficient of variation
TTR_AI, TTR_HUMAN = 0.55, 0.85         # unique words / words, first 100 words
PUNCT_AI, PUNCT_HUMAN = 0.02, 0.12     # non-full-stop marks per word

WEIGHT_SPREAD = 0.60
WEIGHT_TTR = 0.25
WEIGHT_PUNCT = 0.15


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


# ── The three measures — YOU BUILD THESE ─────────────────────────────────────

def sentence_length_spread(text: str) -> float:
    """
    How much sentence length varies.

    Returns:
        A float. Decide yourself what scale it's on and which direction means
        "more human" — then write that down, because your combining rule
        depends on knowing it.

    A hint on what you're reaching for: the standard deviation of sentence
    lengths, probably divided by the mean so a long text and a short one are
    comparable. `statistics.stdev` is imported for you.

    Watch the edge case: a one-sentence submission has no spread at all, and
    `stdev` raises on fewer than two values. Decide what that should return
    before the attack set decides for you.
    """
    sentence_lengths = [len(words(s)) for s in sentences(text)]
    sentence_lengths = [n for n in sentence_lengths if n > 0]
    if len(sentence_lengths) < 2:
        return 0.0  # no spread to measure; style_signal treats this as neutral
    mean = statistics.mean(sentence_lengths)
    return statistics.stdev(sentence_lengths) / mean


def type_token_ratio(text: str) -> float:
    """
    Unique words over total words.

    Returns:
        A float between 0 and 1. Higher means more varied vocabulary.

    Worth knowing before you rely on it: this measure falls as text gets
    longer, because common words repeat. Two texts of different lengths aren't
    directly comparable on it, and if your test inputs vary a lot in length,
    that alone can look like a signal.
    """
    # Only the first TTR_WINDOW words count, so a long text and a short one
    # are compared over the same length.
    tokens = words(text)[:TTR_WINDOW]
    if not tokens:
        return 0.0
    return len(set(tokens)) / len(tokens)


def punctuation_density(text: str) -> float:
    """
    How much punctuation, relative to length.

    Returns:
        A float. Whether you count all punctuation or only some kinds — commas,
        semicolons, dashes — is a real choice. Semicolons and em dashes are
        more interesting than full stops, because they vary more between
        writers.
    """
    tokens = words(text)
    if not tokens:
        return 0.0
    # Everything except the full stop: commas, semicolons, colons, dashes,
    # brackets, quotes, question and exclamation marks.
    marks = re.findall(r"[,;:—–()!?\"“”-]", text)
    return len(marks) / len(tokens)


# ── Combining them ───────────────────────────────────────────────────────────

def style_signal(text: str) -> float:
    """
    The style signal as a 0–1 score. **Higher means more likely AI.**

    Combine your three measures into one number. Same direction as
    `detector.model_signal`, so that `scoring.combine_signals` can treat them
    the same way — if one of your signals runs backwards, everything above it
    is wrong in a way that's hard to see.

    Two things to decide and write down:

      1. Which direction each measure points. Low spread means more AI-ish, so
         it needs flipping. Work out which of your three need that.
      2. How to get each onto a comparable scale. A raw type-token ratio sits
         between 0 and 1; a raw punctuation count doesn't. Adding them
         unscaled means whichever has the bigger numbers wins by default.

    Test it on the four calibration inputs from Milestone 4 — clearly AI,
    clearly human, plain conventional human writing, lightly-edited AI — before
    you trust it. Plain and ordinary, not formal: formal prose reads as *human*
    to signal one, and it is plain writing that gets accused.
    """
    tokens = words(text)
    if len(tokens) < MIN_WORDS_FOR_STYLE:
        return 0.5  # too little text to read a shape from; say "no idea"

    # Each measure becomes a 0–1 "AI-ness" score. Direction in each case:
    #   low sentence spread   -> AI-ish (even, same-length sentences)
    #   low vocabulary variety -> AI-ish (narrower word choice)
    #   low punctuation        -> AI-ish (less varied marks)
    if len(sentences(text)) < 3:
        spread_ai = 0.5  # too few sentences to measure spread: neutral
    else:
        spread_ai = _scale(sentence_length_spread(text), SPREAD_AI, SPREAD_HUMAN)
    ttr_ai = _scale(type_token_ratio(text), TTR_AI, TTR_HUMAN)
    punct_ai = _scale(punctuation_density(text), PUNCT_AI, PUNCT_HUMAN)

    score = (
        WEIGHT_SPREAD * spread_ai
        + WEIGHT_TTR * ttr_ai
        + WEIGHT_PUNCT * punct_ai
    )
    return round(min(max(score, 0.0), 1.0), 4)


def _scale(value: float, ai_end: float, human_end: float) -> float:
    """
    Map a raw measure onto 0–1 where 1 = AI-ish, linearly between two ends.

    `ai_end` is the raw value that counts as fully AI-ish and `human_end` the
    value that counts as fully human-ish. Anything beyond either end is clipped.
    """
    fraction = (value - ai_end) / (human_end - ai_end)
    return 1.0 - min(max(fraction, 0.0), 1.0)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")
