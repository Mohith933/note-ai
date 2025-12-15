import os
import google.generativeai as genai
from datetime import datetime

# -----------------------------------------------------
# GEMINI CONFIG
# -----------------------------------------------------
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
MODEL_NAME = "gemini-2.0-flash"


def call_gemini(prompt: str) -> str:
    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(prompt)
    return response.text.strip()


# -----------------------------------------------------
# TONE DEPTH MAP
# -----------------------------------------------------
DEPTH_TONE = {
    "light": "soft, reflective, gentle emotional clarity",
    "medium": "thoughtful, grounded, emotionally layered",
    "deep": "rich, profound, cinematic emotional depth"
}


# -----------------------------------------------------
# DASHBOARD TEMPLATES
# -----------------------------------------------------

DASHBOARD_REFLECTION = """
You are HeartNote Premium Reflection Writer.

Topic: {name}
Feeling: {desc}
Tone: {tone}

Rules:
- Two paragraphs
- Paragraph 1: 25–35 words
- Paragraph 2: 15–25 words
- Emotional, cinematic English
- No advice, no motivation, no emojis
"""

DASHBOARD_LETTER = """
You are HeartNote Premium Letter Writer.

Recipient: {name}
Feeling: {desc}
Tone: {tone}

Rules:
- Exactly 2 paragraphs
- Paragraph 1: 25–35 words
- Paragraph 2: 15–25 words
- Poetic, grounded
- No advice, no judgement, no emojis

Format: 
Dear Someone dear,  
With warmth, 
💗 HeartNote AI
"""

DASHBOARD_JOURNAL = """
You are HeartNote Premium Journal Writer.

Topic: {name}
Feeling: {desc}
Tone: {tone}

Rules:
- 2 paragraphs
- Paragraph 1: 25–35 words
- Paragraph 2: 15–25 words
- Reflective, cinematic
- No advice, no emojis

Date: {date}
💗 HeartNote AI
"""

DASHBOARD_POEM = """
You are HeartNote Premium Poem Writer.

Theme: {name} — {desc}

Rules:
- 6–8 free-verse lines
- Soft emotional imagery
- No advice, no emojis
"""

DASHBOARD_STORY = """
You are HeartNote Premium Story Writer.

Theme: {name} — {desc}

Rules:
- 45–70 words
- Emotional micro-story
- No advice, no emojis
"""

DASHBOARD_QUOTE = """
You are HeartNote Premium Quote Writer.

Theme: {name} — {desc}

Rules:
- One sentence
- Under 24 words
- Poetic, reflective
- No emojis
"""

DASHBOARD_AFFIRMATION = """
You are HeartNote Premium Affirmation Writer.

Theme: {name} — {desc}

Rules:
- 1–2 lines
- Gentle, grounded
- No advice, no emojis
"""

DASHBOARD_NOTE = """
You are HeartNote Premium Note Writer.

Rules:
- Use EXACT bullet format
- Neutral, reflective language
- No advice, no emojis

Format ONLY:

• What you felt: {desc}
• Why it happened: one calm reason
• What could help: one gentle idea
"""


# -----------------------------------------------------
# LLM SERVICE
# -----------------------------------------------------
class Dashboard_LLM_Service:

    def generate(self, mode, name, desc, depth, language):
        depth = depth.lower().strip()
        tone = DEPTH_TONE.get(depth, DEPTH_TONE["light"])
        mode = mode.lower().strip()
        language = language.lower().strip()

        # 🔐 Safety first
        safe, result = self.safety_filter(desc)
        if not safe:
            return {"response": result, "blocked": True}

        # Template selection
        date = datetime.now().strftime("%d/%m/%Y")

        templates = {
            "reflection": DASHBOARD_REFLECTION,
            "letters": DASHBOARD_LETTER,
            "journal": DASHBOARD_JOURNAL,
            "poems": DASHBOARD_POEM,
            "story": DASHBOARD_STORY,
            "quotes": DASHBOARD_QUOTE,
            "affirmation": DASHBOARD_AFFIRMATION,
            "notes": DASHBOARD_NOTE
        }

        template = templates.get(mode)
        if not template:
            return {"response": "⚠ Unknown mode", "blocked": False}

        prompt = template.format(
            name=name,
            desc=desc,
            tone=tone,
            date=date
        )

        prompt = f"[LANG={language}]\n{prompt}"

        text = call_gemini(prompt)

        return {
            "response": text,
            "blocked": False
        }

    # -------------------------------------------------
    # SAFETY FILTER
    # -------------------------------------------------
    def safety_filter(self, text):
        t = text.lower()

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
