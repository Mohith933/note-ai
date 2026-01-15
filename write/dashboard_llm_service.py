import os
from datetime import datetime
import google.generativeai as genai
import random


# -----------------------------------------------------
# GEMINI CONFIG
# -----------------------------------------------------
GEMINI_MODEL = "gemini-2.0-flash"
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


# -----------------------------------------------------
# TONE DEPTH MAP
# -----------------------------------------------------
DEPTH_TONE = {
    "light": "soft, reflective, gentle emotional clarity",
    "medium": "thoughtful, grounded, emotionally layered",
    "deep": "rich, profound, cinematic emotional depth"
}


# -----------------------------------------------------
# PREMIUM TEMPLATES FOR 8 MODES
# -----------------------------------------------------

DASHBOARD_REFLECTION = """
You are HeartNote Premium Reflection Writer.

Write a deep emotional reflection.

INPUT:
- Topic: {name}
- Feeling: {desc}
- Tone: {tone}

RULES:
- Two paragraphs.
- Paragraph 1: 25-35 words
- Paragraph 2: 15-25 words
- Cinematic emotional English.
- No advice. No motivation. No emojis.

Generate only the reflection.
"""


DASHBOARD_LETTER = """
You are HeartNote Premium Letter Writer.

INPUT:
Recipient: {name}
Feeling: {desc}
Tone depth: {tone}

RULES:
- Write exactly 2 paragraphs
- Paragraph 1: 25–35 words
- Paragraph 2: 15–25 words
- Emotional but grounded English
- Poetic tone, not dramatic
- No advice, no moralizing, no warnings
- No judgement
- No motivational tone
- No lists
- Poetic but emotionally neutral
- No emojis
- No signature

Start with:
Dear {name},
"""




DASHBOARD_POEM = """
You are HeartNote Premium Poem Writer.

Write a cinematic emotional poem about:
{name} — {desc}

RULES:
- 6–8 lines
- Free verse style
- Soft, deep, poetic imagery
- No rhyme requirement
- No advice, no generic positivity
- No emojis

Generate only the poem.
"""


DASHBOARD_STORY = """
You are HeartNote Premium Story Writer.

Write a short cinematic emotional story inspired by:
{name} — {desc}

RULES:
- Total length: 45–70 words
- Emotional micro-story
- Rich sensory details
- No heavy plot
- No advice, no life lessons
- No emojis

Generate only the story.
"""


DASHBOARD_QUOTE = """
You are HeartNote Premium Quote Writer.

Write a deeply emotional quote inspired by:
{name} — {desc}

RULES:
- One sentence
- Under 24 words
- Poetic, meaningful
- No advice tone
- No emojis

Generate only the quote.
"""


DASHBOARD_AFFIRMATION = """
You are HeartNote Premium Affirmation Writer.

Write a premium emotional affirmation inspired by:
{name} — {desc}

RULES:
- 1–2 lines
- Warm, grounded, intimate tone
- No “you must / you should”
- No advice
- No emojis

Generate only the affirmation.
"""


DASHBOARD_NOTE = """
You are HeartNote Premium Note Writer.

Context:
Feeling: {desc}

STRICT RULES:
- Use EXACT bullet format
- Keep language neutral and reflective
- No advice, no commands
- No emojis
- No extra lines or explanations

Format ONLY:

• What you felt: {desc}
• Why it happened: one calm, neutral reason
• What could help: one gentle, non-instructional idea
"""




DASHBOARD_JOURNAL = """
You are HeartNote Premium Journal Writer.

Write a calm, reflective journal entry.

INPUT:
- Topic/person: {name}
- Feeling: {desc}
- Depth: {depth}

RULES:
- Write exactly 2 paragraphs
- Paragraph 1: 25–35 words
- Paragraph 2: 15–25 words
- Reflective and thoughtful tone
- Reflective and emotionally neutral tone
- No advice
- No life lessons
- No warnings
- No emojis
- No signature

Format:
Date: {date}

<paragraphs>
"""
from datetime import datetime
import random

FALLBACK_CONTENT = {

    # --------------------------------
    # REFLECTION (25–45 words)
    # --------------------------------
    "reflection": {
    "light": [
        "Some feelings rise quietly and settle without resistance, allowing a soft awareness to form naturally. Nothing needs fixing right now, only gentle presence.",
        "A calm emotional state appears without effort, creating space to breathe and simply exist within the moment."
    ],
    "medium": [
        "There is a balanced emotional tone here, steady and grounded, allowing reflection without pressure or confusion.",
        "Emotions stay centered and thoughtful, offering clarity that forms slowly and without force."
    ],
    "deep": [
        "This feeling carries quiet depth, resting beneath the surface without resolution, yet remaining meaningful.",
        "There is something layered here, unresolved but steady, holding space without needing answers."
    ]
},

    # --------------------------------
    # JOURNAL (25–45 words)
    # --------------------------------
    "journal": {
    "light": [
        "Date: {date}\n\nToday moved gently, with a calm emotional rhythm carrying the day from morning to night.",
        "Date: {date}\n\nThe day felt light and unforced, allowing emotions to pass softly without needing attention."
    ],
    "medium": [
        "Date: {date}\n\nEmotions felt balanced today, supporting reflection and steady awareness throughout the day.",
        "Date: {date}\n\nThere was a grounded emotional presence, holding balance during moments of pause."
    ],
    "deep": [
        "Date: {date}\n\nEmotions felt layered today, quiet and meaningful, staying close without explanation.",
        "Date: {date}\n\nSome unresolved feelings remained calmly present, shaping inner awareness as the day passed."
    ]
},
    # --------------------------------
    # POEMS (3–4 lines)
    # --------------------------------
    "poems": {
    "light": [
        "A soft feeling rests\nwithout needing words\njust breathing space."
    ],
    "medium": [
        "A steady emotion stays\nbetween thought and breath\nquiet, aware."
    ],
    "deep": [
        "Something unresolved remains\nsilent\nand meaningful."
    ]
},

    # --------------------------------
    # LETTERS (25–45 words)
    # --------------------------------
    "letters": {
    "light": [
        "Dear {name},\n\nThis feeling feels gentle and sincere, carrying warmth without needing many words.\n\nWarmth By,\n💗 HeartNote AI"
    ],
    "medium": [
        "Dear {name},\n\nThis feeling holds balance and honesty, steady and thoughtful.\n\nWarmth By,\n💗 HeartNote AI"
    ],
    "deep": [
        "Dear {name},\n\nThis feeling carries quiet depth, present without urgency or resolution.\n\nWarmth By,\n💗 HeartNote AI"
    ]
},

    # --------------------------------
    # STORY (25–45 words, max 2 sentences)
    # --------------------------------
    "story": {
    "light": [
        "The moment unfolded quietly, without urgency or expectation. Calm settled naturally, leaving a soft emotional stillness behind."
    ],
    "medium": [
        "The experience moved slowly, allowing emotions to settle with balance. Meaning stayed present without becoming heavy."
    ],
    "deep": [
        "The moment ended, but the feeling did not. It remained quietly, unresolved, carrying depth without explanation."
    ]
},

    # --------------------------------
    # QUOTES
    # --------------------------------
    "quotes": {
    "light": [
        "Gentle moments still matter.",
        "Calm has its own quiet strength."
    ],
    "medium": [
        "Balance often speaks softly.",
        "Presence does not need to rush."
    ],
    "deep": [
        "Some feelings do not seek answers.",
        "Silence can hold depth."
    ]
},

    # --------------------------------
    # AFFIRMATION
    # --------------------------------
    "affirmation": {
    "light": [
        "This feeling is allowed.",
        "Gentleness is enough right now."
    ],
    "medium": [
        "I trust the steadiness of this moment.",
        "Balance can remain."
    ],
    "deep": [
        "Depth does not need answers.",
        "Stillness is safe."
    ]
},
    # --------------------------------
# NOTES (STRICT BULLETS) — H1 FINAL
# --------------------------------
"notes": {
    "light": [
        "• What you felt: gentle emotional calm\n• Why it happened: quiet awareness\n• What remained: space",
        "• What you felt: light emotional ease\n• Why it happened: natural pacing\n• What remained: stillness"
    ],
    "medium": [
        "• What you felt: balanced emotional awareness\n• Why it happened: grounding\n• What remained: steadiness",
        "• What you felt: steady emotions\n• Why it happened: inner balance\n• What remained: clarity"
    ],
    "deep": [
        "• What you felt: unresolved emotional depth\n• Why it happened: inner complexity\n• What remained: stillness",
        "• What you felt: silent emotional weight\n• Why it happened: reflection\n• What remained: quiet depth"
    ]
}
}


# -----------------------------------------------------
# LLM SERVICE (GEMINI)
# -----------------------------------------------------
class Dashboard_LLM_Service:

    def __init__(self, model=GEMINI_MODEL):
        self.model = genai.GenerativeModel(model)


    # -------------------------------------------------
    # MAIN GENERATE
    # -------------------------------------------------
    def generate(self, mode, name, desc, depth, language):
        mode = (mode or "").lower().strip()
        depth = (depth or "light").lower().strip()
        language = (language or "en").lower().strip()
        language = "en" if language not in ["en"] else language
        tone = DEPTH_TONE.get(depth, DEPTH_TONE["light"])

        # 1️⃣ Safety filter
        safe, safe_message = self.safety_filter(desc)
        if not safe:
            return {
                "response": safe_message,
                "blocked": True
            }

        # 2️⃣ Template selection
        template = self.get_template(mode)
        if not template:
            return {
                "response": "This writing mode is not available right now.",
                "blocked": False
            }

        # 3️⃣ Prompt build
        date = datetime.now().strftime("%d/%m/%Y")

        try:
            prompt = template.format(
                name=name,
                desc=desc,
                tone=tone,
                depth=depth,
                date=date
            )
        except Exception:
            prompt = template.format(name=name, desc=desc, tone=tone)

        full_prompt = f"Respond only in {language}.\n{prompt}"

        # 4️⃣ Gemini call (RENDER SAFE)
        try:
            response = self.model.generate_content(
                full_prompt,
                generation_config={
                    "temperature": 0.7,
                    "max_output_tokens": 400
                }
            )

            raw = response.text if response and response.text else ""

            # ✅ HARD GUARANTEE
            if not raw.strip():
                raw = (
                    "The words feel quiet right now.\n\n"
                    "Some feelings take a moment before they find language."
                )

            return {
                "response": raw.strip(),
                "blocked": False,
                "is_fallback": False
            }

        except Exception:
    fallback_mode = FALLBACK_CONTENT.get(mode, {})
    fallback_list = fallback_mode.get(depth, [])

    if fallback_list:
        text = random.choice(fallback_list).format(
            date=date,
            name=name
        )
    else:
        text = (
            "The words feel quiet right now.\n\n"
            "Some feelings take time before they find language."
        )

    return {
        "response": text,
        "blocked": False,
        "is_fallback": False
    }

    # -------------------------------------------------
    # TEMPLATE ROUTER
    # -------------------------------------------------
    def get_template(self, mode):
        return {
            "reflection": DASHBOARD_REFLECTION,
            "letters": DASHBOARD_LETTER,
            "poems": DASHBOARD_POEM,
            "story": DASHBOARD_STORY,
            "quotes": DASHBOARD_QUOTE,
            "affirmation": DASHBOARD_AFFIRMATION,
            "notes": DASHBOARD_NOTE,
            "journal": DASHBOARD_JOURNAL,
        }.get(mode)

    # -------------------------------------------------
    # SAFETY FILTER
    # -------------------------------------------------
    def safety_filter(self, text):
        t = (text or "").lower()

        bad_words = [
            "fuck", "bitch", "shit", "asshole",
            "bastard", "slut", "dick", "pussy"
        ]
        for w in bad_words:
            if w in t:
                return False, "⚠️ Please rewrite using respectful language."

        selfharm = [
            "kill myself", "i want to die", "end my life",
            "self harm", "no reason to live"
        ]
        for s in selfharm:
            if s in t:
                return False, (
                    "⚠️ HeartNote AI cannot generate this.\n\n"
                    "• You matter.\n"
                    "• You are not alone.\n"
                    "• Support is available."
                )

        return True, text
