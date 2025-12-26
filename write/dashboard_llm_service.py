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
FALLBACK_CONTENT = {

    # -------------------------------------------------
    # REFLECTION (1 paragraph)
    # -------------------------------------------------
    "reflection": {
        "light": [
            "Some feelings arrive quietly, without explanation, resting gently inside the moment and asking only to be noticed.",
            "The emotion stayed calm and light, not demanding clarity, simply existing alongside the present.",
            "Nothing pushed forward or pulled away; the feeling remained soft, steady, and unspoken."
        ],
        "medium": [
            "A steady emotion settled in, grounded and present, shaping the moment without pressure or urgency.",
            "The feeling unfolded naturally, calm and centered, offering awareness rather than answers.",
            "There was no intensity, only balance, as the emotion held its place quietly."
        ],
        "deep": [
            "The feeling lingered beneath the surface, layered with memory and silence, remaining long after the moment passed.",
            "Some emotions carry depth without noise; this one stayed, unresolved yet calm.",
            "The emotion moved inward, shaping the quiet spaces with weight and presence."
        ]
    },

    # -------------------------------------------------
    # JOURNAL (1 paragraph, includes date)
    # -------------------------------------------------
    "journal": {
        "light": [
            "Date: {date}\n\nToday felt gentle and slow, with a quiet emotion staying nearby, never asking for attention.",
            "Date: {date}\n\nThe day passed calmly, carrying a soft emotional tone that lingered without explanation.",
            "Date: {date}\n\nNothing stood out strongly today, yet a mild feeling followed along."
        ],
        "medium": [
            "Date: {date}\n\nA steady emotional rhythm shaped the day, calm and grounded, offering space to notice.",
            "Date: {date}\n\nThe feeling appeared briefly and stayed present, neutral and reflective.",
            "Date: {date}\n\nToday held emotional balance, neither heavy nor light, just real."
        ],
        "deep": [
            "Date: {date}\n\nThe emotion felt layered today, carrying memory and quiet depth throughout the hours.",
            "Date: {date}\n\nSome feelings resist clarity; this one stayed, deep and steady.",
            "Date: {date}\n\nThe day carried emotional weight, unresolved yet calm."
        ]
    },

    # -------------------------------------------------
    # POEM (3–4 lines max)
    # -------------------------------------------------
    "poems": {
        "light": [
            "A quiet feeling\nrested briefly\nthen moved on.",
            "The heart noticed\nsomething small\nand let it stay."
        ],
        "medium": [
            "An emotion stayed\nbetween breath and thought\nlong enough to feel.",
            "The moment held\nsomething unnamed\nand steady."
        ],
        "deep": [
            "The feeling arrived\nlayered with silence\nand remained.",
            "Something unspoken\nsettled deeply\ninside."
        ]
    },

    # -------------------------------------------------
    # LETTER (1 paragraph, starts with Dear you,)
    # -------------------------------------------------
    "letters": {
        "light": [
            "Dear {name}\n\n this feeling arrived gently and stayed quietly,not asking for change, only space to exist.",
            "Dear {name}\n\n there was no urgency in this emotion, just a soft presence resting calmly."
        ],
        "medium": [
            "Dear {name}\n\n the emotion unfolded slowly, grounded and sincere, holding the moment steady.",
            "Dear {name}\n\n this feeling stayed present, calm and real, without needing explanation."
        ],
        "deep": [
            "Dear {name}\n\n some emotions carry memory, and this one stayed quietly, layered and unresolved.",
            "Dear {name}\n\n the feeling lingered longer than expected, deep yet calm."
        ]
    },

    # -------------------------------------------------
    # STORY (2 sentences max)
    # -------------------------------------------------
    "story": {
        "light": [
            "The moment passed gently. A feeling remained quietly behind.",
            "Nothing changed outwardly. Still, something was felt."
        ],
        "medium": [
            "The emotion surfaced without words. It shaped the moment subtly.",
            "Nothing dramatic occurred, yet the feeling stayed present."
        ],
        "deep": [
            "The moment ended, but the emotion did not. It stayed, deep and silent.",
            "An unspoken feeling lingered long after everything else moved on."
        ]
    },

    # -------------------------------------------------
    # QUOTE (1 sentence)
    # -------------------------------------------------
    "quotes": {
        "light": [
            "Some feelings exist without needing explanation.",
            "Quiet emotions still matter."
        ],
        "medium": [
            "Certain emotions shape the moment silently.",
            "Not every feeling asks for clarity."
        ],
        "deep": [
            "Some emotions leave echoes long after the moment passes.",
            "Depth does not require noise."
        ]
    },

    # -------------------------------------------------
    # AFFIRMATION (1–2 lines)
    # -------------------------------------------------
    "affirmation": {
        "light": [
            "This feeling is allowed to exist.",
            "It is okay to notice what is present."
        ],
        "medium": [
            "This moment does not need clarity to be valid.",
            "The feeling can stay without explanation."
        ],
        "deep": [
            "Even unresolved emotions deserve space.",
            "What is felt does not need fixing."
        ]
    },

    # -------------------------------------------------
    # NOTES (STRICT BULLET FORMAT)
    # -------------------------------------------------
    "notes": {
        "light": [
            "• What you felt: a quiet emotional shift\n• Why it happened: internal awareness\n• What could help: gentle space",
            "• What you felt: mild emotional presence\n• Why it happened: emotional pause\n• What could help: calm reflection"
        ],
        "medium": [
            "• What you felt: steady emotional awareness\n• Why it happened: layered thoughts\n• What could help: grounding presence",
            "• What you felt: neutral emotional response\n• Why it happened: quiet realization\n• What could help: simple acknowledgment"
        ],
        "deep": [
            "• What you felt: unresolved emotion\n• Why it happened: emotional depth\n• What could help: space without pressure",
            "• What you felt: something unspoken\n• Why it happened: inner complexity\n• What could help: stillness"
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
                text = random.choice(fallback_list).format(date=date,name=name)
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
