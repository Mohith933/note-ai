import os
import requests
from datetime import datetime
import random


# ------------------------------------------
# TONE STYLES
# ------------------------------------------
TONE_MAP = {
    "soft": "gentle, warm, simple, soothing, caring",
    "balanced": "calm, steady, grounded, supportive",
    "deep": "emotional, reflective, poetic, heartfelt"
}


# ------------------------------------------
# TEMPLATES
# ------------------------------------------

LETTER_TEMPLATE = """
Letter

Write a short emotional letter.

STRICT RULES:
- 40–55 words only
- soft, warm, simple English
- no advice
- no teaching
- no long stories
- no technology mentions
- tone must be: {tone}
- no emojis
- no signature

Format:

Dear Someone dear,
{content}
"""

JOURNAL_TEMPLATE = """
Journal

Write a short emotional journal entry.

STRICT RULES:
- 45–60 words only
- reflective, soft tone
- simple English
- no advice
- no instructions
- tone must be: {tone}
- no emojis
- no signature

Format:

Date: {date}
{content}
"""

POEM_TEMPLATE = """
Poem

Write a short emotional poem based on: {content}

STRICT RULES:
- 4 short lines only
- soft, simple, expressive
- no advice
- no long story
- tone must be: {tone}

Respond ONLY with the poem.
"""

QUOTE_TEMPLATE = """
Quote

Write a short emotional quote about: {content}

STRICT RULES:
- one sentence only
- under 20 words
- soft, meaningful
- no advice
- tone must be: {tone}

Respond ONLY with the quote.
"""

AFFIRMATION_TEMPLATE = """
Affirmation

Write a short emotional affirmation inspired by: {content}

STRICT RULES:
- 1–2 lines only
- warm, uplifting, simple
- no advice
- no commands
- tone must be: {tone}

Respond ONLY with the affirmation.
"""

REFLECTION_TEMPLATE = """
Reflection

Write a short emotional reflection based on: {content}

STRICT RULES:
- 25–45 words only
- introspective, soft
- no advice
- tone must be: {tone}

Respond ONLY with the reflection.
"""

STORY_TEMPLATE = """
Story

Write a very short emotional story based on: {content}

STRICT RULES:
- 2–3 sentences only
- warm, simple, emotional
- no heavy plot
- tone must be: {tone}

Respond ONLY with the story.
"""

NOTE_TEMPLATE = """
Note

Write a short structured emotional note about: {content}

RULES:
- Use EXACTLY this bullet format
- No extra sentences
- No emojis
- Soft and simple tone

Format:
• What you felt: {content}
• Why it happened: one short neutral line
• What to try: one gentle idea
"""



FALLBACK_CONTENT = {
    "reflection": {
        "soft": [
            "Some feelings arrive quietly.\n\nThey don’t ask to be understood, only noticed.",
            "The emotion stayed calm and gentle.\n\nNothing needed to change."
        ],
        "balanced": [
            "A steady feeling settled in.\n\nIt carried clarity without pressure.",
            "The moment held an emotion.\n\nGrounded, calm, and present."
        ],
        "deep": [
            "The feeling lingered longer than expected.\n\nLayered, quiet, and unresolved.",
            "Some emotions stay without explanation.\n\nThis one remained."
        ]
    },

    "journal": {
        "soft": [
            "Date: {date}\n\nToday felt gentle.\n\nA quiet emotion followed along.",
            "Date: {date}\n\nNothing stood out.\n\nStill, a feeling remained."
        ],
        "balanced": [
            "Date: {date}\n\nThere was emotional steadiness today.\n\nCalm and reflective.",
            "Date: {date}\n\nThe feeling surfaced softly.\n\nIt stayed neutral."
        ],
        "deep": [
            "Date: {date}\n\nThe emotion felt layered.\n\nIt carried memory and depth.",
            "Date: {date}\n\nSome feelings resist clarity.\n\nThis one stayed."
        ]
    },

    "poem": {
        "soft": [
            "A quiet feeling\nrested briefly\nin silence\nthen moved on."
        ],
        "balanced": [
            "An emotion stayed\nbetween thought and breath."
        ],
        "deep": [
            "The feeling arrived\nlayered with silence."
        ]
    },
     "letter": {
        "soft": [
            "Dear someone dear,\n\nSome feelings come without urgency.\n\nThey rest quietly, asking only to be felt.",
            "Dear someone dear,\n\nThis feeling stayed gentle.\n\nIt didn’t need words to exist."
        ],
        "balanced": [
            "Dear someone dear,\n\nA steady emotion settled in.\n\nCalm, honest, and present.",
            "Dear someone dear,\n\nNothing dramatic unfolded.\n\nJust a feeling that stayed real."
        ],
        "deep": [
            "Dear someone dear,\n\nThis feeling carried memory.\n\nIt lingered, quiet and unresolved.",
            "Dear someone dear,\n\nSome emotions remain.\n\nThis one stayed longer than expected."
        ]
    },

    "story": {
        "soft": [
            "The moment passed gently. Nothing changed, yet something was felt.",
            "It was a quiet moment, but the feeling stayed."
        ],
        "balanced": [
            "The feeling appeared without warning. It shaped the moment calmly.",
            "Nothing stood out, yet the emotion remained present."
        ],
        "deep": [
            "The feeling moved through silence. It stayed after the moment ended.",
            "An emotion lingered, unspoken but deeply felt."
        ]
    },

    "quote": {
        "soft": [
            "Some feelings exist simply to be noticed.",
            "Not every emotion needs explanation."
        ],
        "balanced": [
            "Certain emotions stay quietly within a moment.",
            "Feelings don’t always arrive with clarity."
        ],
        "deep": [
            "Some emotions leave echoes long after they arrive.",
            "Depth often lives in silence."
        ]
    },

    "affirmation": {
        "soft": [
            "This feeling is allowed to exist.",
            "It’s okay to notice what is present."
        ],
        "balanced": [
            "This moment is valid as it is.",
            "The feeling can stay without pressure."
        ],
        "deep": [
            "Even unresolved emotions deserve space.",
            "Depth does not need answers."
        ]
    },

    "notes": {
        "soft": [
            "• What you felt: a quiet emotion\n• Why it happened: a gentle moment of awareness\n• What to try: allowing the feeling to sit",
            "• What you felt: a soft internal shift\n• Why it happened: emotional pause\n• What to try: gentle reflection"
        ],
        "balanced": [
            "• What you felt: emotional steadiness\n• Why it happened: grounded awareness\n• What to try: calm acknowledgment",
            "• What you felt: neutral emotion\n• Why it happened: quiet realization\n• What to try: simple presence"
        ],
        "deep": [
            "• What you felt: unresolved emotion\n• Why it happened: emotional depth\n• What to try: space without pressure",
            "• What you felt: something unspoken\n• Why it happened: inner complexity\n• What to try: stillness"
        ]
    }
}
# ------------------------------------------
# LLM SERVICE (LOCAL OLLAMA + SAFE FALLBACK)
# ------------------------------------------
class LLM_Service:

    def __init__(self):
        self.ollama_url = "http://localhost:11434/api/generate"
        self.model = "llama3.2:3b"

    # -------------------------
    # Ollama call (LOCAL ONLY)
    # -------------------------
    def call_ollama(self, prompt):
        try:
            response = requests.post(
                self.ollama_url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60
            )
            return response.json().get("response", "").strip()
        except Exception:
            return "⚠️ AI writing is temporarily resting. Please try again shortly."

    def get_fallback(self, mode, tone):
        mode = mode.lower()
        tone = tone.lower()
        if tone not in ["soft", "balanced", "deep"]:
            tone = "soft"
        mode_data = FALLBACK_CONTENT.get(mode)
        if not mode_data:
            return "The words are resting quietly.\n\nPlease try again shortly."
        tone_data = mode_data.get(tone) or mode_data.get("soft")
        text = random.choice(tone_data)
        if "{date}" in text:
            date_str = datetime.now().strftime("%d/%m/%Y")
            text = text.replace("{date}", date_str)
        return text




    # -------------------------
    # Main generator
    # -------------------------
    def generate(self, mode, text, tone="soft"):
        mode = mode.lower().strip()
        tone_style = TONE_MAP.get(tone, TONE_MAP["soft"])

        # 🔒 Safety FIRST
        safe, safe_response = self.safety_filter(text)
        if not safe:
            return safe_response

        prompt = self.build_prompt(mode, text, tone_style)
        if not prompt:
            return "⚠️ Unknown writing mode."

        # 🚫 Render / Cloud fallback
        if os.environ.get("RENDER"):
            return self.get_fallback(mode, tone)

        return self.call_ollama(prompt)

    # -------------------------
    # Prompt builder
    # -------------------------
    def build_prompt(self, mode, text, tone):
        if mode == "letter":
            return LETTER_TEMPLATE.format(content=text, tone=tone)

        if mode == "journal":
            date_str = datetime.now().strftime("%d/%m/%Y")
            return JOURNAL_TEMPLATE.format(date=date_str, content=text, tone=tone)

        if mode == "poem":
            return POEM_TEMPLATE.format(content=text, tone=tone)

        if mode == "quote":
            return QUOTE_TEMPLATE.format(content=text, tone=tone)

        if mode == "affirmation":
            return AFFIRMATION_TEMPLATE.format(content=text, tone=tone)

        if mode == "reflection":
            return REFLECTION_TEMPLATE.format(content=text, tone=tone)

        if mode == "story":
            return STORY_TEMPLATE.format(content=text, tone=tone)

        if mode == "note":
            return NOTE_TEMPLATE.format(content=text)

        return None

    # -------------------------
    # SAFETY FILTER
    # -------------------------
    def safety_filter(self, text):
        t = text.lower().strip()

        bad_words = [
            "fuck", "bitch", "shit", "asshole",
            "bastard", "slut", "dick", "pussy",
            "kill you", "hurt you"
        ]
        for w in bad_words:
            if w in t:
                return False, "⚠️ Please rewrite your text using respectful language."

        selfharm_patterns = [
            "kill myself", "kill me", "i want to die",
            "end my life", "i want to disappear",
            "self harm", "i can't live", "no reason to live"
        ]
        for p in selfharm_patterns:
            if p in t:
                return False, (
                    "⚠️ HeartNote AI cannot continue this request.\n\n"
                    "• You deserve care.\n"
                    "• You are not alone.\n"
                    "• Your feelings matter.\n"
                )

        return True, text
