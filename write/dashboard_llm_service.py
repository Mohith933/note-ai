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

    "reflection": {
        "light": [
            "Some feelings don’t arrive loudly.\n\nThey sit beside the moment, soft and unfinished, asking only to be felt.",
            "There was no clear beginning to this emotion.\n\nIt appeared gently, leaving a quiet warmth behind."
        ],
        "medium": [
            "This feeling carried weight without explanation.\n\nIt stayed steady, neither heavy nor light, simply present.",
            "The emotion unfolded slowly.\n\nNothing dramatic—just a calm awareness settling in."
        ],
        "deep": [
            "The feeling moved through memory and silence.\n\nIt lingered, layered and unresolved, shaping the space around it.",
            "Some emotions leave echoes.\n\nThey remain long after the moment passes, quietly reshaping the inside."
        ]
    },

    "journal": {
        "light": [
            "Date: {date}\n\nToday felt gentle but uncertain.\n\nNothing demanded answers, yet the feeling stayed, soft and observant.",
            "Date: {date}\n\nThe day moved calmly.\n\nA quiet emotion followed along, never asking to be named."
        ],
        "medium": [
            "Date: {date}\n\nThere was a steady emotional undercurrent today.\n\nNot overwhelming, but noticeable enough to pause and reflect.",
            "Date: {date}\n\nThe feeling surfaced without warning.\n\nIt stayed neutral, grounding the rhythm of the day."
        ],
        "deep": [
            "Date: {date}\n\nThe emotion felt layered and familiar.\n\nIt carried memory, silence, and a quiet sense of depth.",
            "Date: {date}\n\nSome feelings resist clarity.\n\nThis one stayed, heavy with presence, yet calm."
        ]
    },

    "poems": {
        "light": [
            "A feeling passed softly\nlike evening light\nnever asking to stay\nnever rushing away.",
            "The heart noticed\nsomething small\nand let it remain\nwithout questions."
        ],
        "medium": [
            "A quiet emotion\nstood still\nbetween thought and breath\nwaiting to be felt.",
            "Some feelings\nwalk slowly\nleaving space\nbehind them."
        ],
        "deep": [
            "The feeling arrived\nlayered with memory\nmoving through silence\nwithout leaving a name.",
            "An emotion stayed\nlonger than expected\nshaping the quiet\ninside."
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
                text = random.choice(fallback_list).format(date=date)
            else:
                text = (
            "The words feel quiet right now.\n\n"
            "Some feelings take time before they find language."
                )
            return {
        "response": text,
        "blocked": False,
        "is_fallback": True
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
