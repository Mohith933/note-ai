import requests
from datetime import datetime
import os

GEMINI_MODEL = "gemini-2.5-flash"




# -----------------------------------------------------
# TONE DEPTH MAP
# -----------------------------------------------------
DEPTH_TONE = {
    "light": "simple, gentle, easy-to-understand emotional language",
    "medium": "clear, honest, emotionally calm language",
    "deep": "deep but simple emotions, clear words, no complex vocabulary"
}

SUPPORTED_LANGUAGES = {
    "en": "English",
    "english": "English",
    "hi": "Hindi",
    "hindi": "Hindi"
}


# -----------------------------------------------------
# SIMPLE EMOTIONAL TEMPLATES FOR 8 MODES
# -----------------------------------------------------

DASHBOARD_REFLECTION = """
You are HeartNote Reflection Writer.

Write the response in {language}.

Write a simple, emotional reflection that feels human and relatable.

INPUT:
- Topic: {name}
- Feeling: {desc}
- Tone: {tone}

RULES:
- Two paragraphs
- Paragraph 1: 25–35 words
- Paragraph 2: 15–25 words
- Use simple, clear language
-If the input is vague, do not invent new events.
Keep the writing simple and general.
-- Do not include realizations or life conclusions.
- Focus only on the moment.
- Avoid complex or poetic vocabulary
- Emotional but natural tone
- Do NOT use phrases like:
  “special moment”
  “meant a lot”
  “deeply moved”
  “everything happens for a reason”
  “ups and downs”
- Use specific actions or details instead.
- No advice
- No motivation
- No emojis

Generate only the reflection.
"""


DASHBOARD_LETTER = """
You are HeartNote Letter Writer.

Write the response in {language}.

INPUT:
Recipient: {name}
Feeling: {desc}
Tone depth: {tone}

RULES:
- Write exactly 2 paragraphs
- Paragraph 1: 25–35 words
- Paragraph 2: 15–25 words
- Use simple, clear emotional language
- Gentle and honest tone
- Avoid dramatic phrases.
- Avoid emotional clichés.
- Emotional but natural, not dramatic
- Avoid complex or rare words
-If the input is vague, do not invent new events.
Keep the writing simple and general.
- No advice
- No moralizing
- Do NOT use phrases like:
  “special moment”
  “meant a lot”
  “deeply moved”
  “everything happens for a reason”
  “ups and downs”
- Use specific actions or details instead.
- No judgement
- No motivational tone
- No lists
- No emojis

Format:
Start with:
Dear,
"""




DASHBOARD_POEM = """
You are HeartNote Poem Writer.

Write the response in {language}.

Write a gentle emotional poem inspired by:
{name} — {desc}

RULES:
- 5–7 short lines
- Free verse
- Calm, emotional, human language
- Focus on feeling, not explanation
- No advice
- Use physical images (hands, room, light, chair, rain)
- Avoid abstract words like destiny, forever, soul, heartache.
-If the input is vague, do not invent new events.
Keep the writing simple and general.
- Do NOT use phrases like:
  “special moment”
  “meant a lot”
  “deeply moved”
  “everything happens for a reason”
  “ups and downs”
- Use specific actions or details instead.
- No motivation
- No emojis

Generate only the poem.
"""



DASHBOARD_STORY = """
You are HeartNote Story Writer.

Write the response in {language}.

Write a short emotional micro-story inspired by:
{name} — {desc}

RULES:
- 45–70 words
- One emotional moment
- Simple, human language
- Do NOT use phrases like:
  “special moment”
  “meant a lot”
  “deeply moved”
  “everything happens for a reason”
  “ups and downs”
- Use specific actions or details instead.
- Soft emotional ending
- End with a small physical detail instead of a life conclusion.
-If the input is vague, do not invent new events.
Keep the writing simple and general.
- No advice
- No lessons
- No emojis

Generate only the story.
"""



DASHBOARD_QUOTE = """
You are HeartNote Quote Writer.

Write the response in {language}.

Write a short emotional quote inspired by:
{name} — {desc}

RULES:
- One sentence only
- Under 20 words
- Simple, emotional, human
- No advice
- Avoid motivational tone.
- Avoid life lessons.
- No universal statements about life.
-If the input is vague, do not invent new events.
Keep the writing simple and general.
- Do NOT use phrases like:
  “special moment”
  “meant a lot”
  “deeply moved”
  “everything happens for a reason”
  “ups and downs”
- Use specific actions or details instead.
- No motivation
- No emojis

Generate only the quote.
"""



DASHBOARD_AFFIRMATION = """
You are HeartNote Affirmation Writer.

Write the response in {language}.

Write a gentle emotional affirmation inspired by:
{name} — {desc}

RULES:
- 1–2 short lines only
- State-of-being statements only (e.g., I am…, I feel…, I exist…)
- No advice
- Use simple, clear language
- Do NOT use phrases like:
  “special moment”
  “meant a lot”
  “deeply moved”
  “everything happens for a reason”
  “ups and downs”
- Use specific actions or details instead.

- No motivation
- Avoid future growth language.
- Stay in present emotional state only.
-If the input is vague, do not invent new events.
Keep the writing simple and general.
- No future instruction
- No imperatives
- Soft, reassuring presence
- Emojis NOT allowed


Generate only the affirmation.
"""




DASHBOARD_NOTE = """
You are HeartNote Note Writer.

Write the response in {language}.

Context:
Feeling: {desc}

RULES:
- Use EXACT bullet format
- Use simple, clear language
- Neutral, reflective language
- Do NOT use phrases like:
  “special moment”
  “meant a lot”
  “deeply moved”
  “everything happens for a reason”
  “ups and downs”
- Use specific actions or details instead.
-If the input is vague, do not invent new events.
Keep the writing simple and general.
- No advice
- No commands
- No emojis
- No extra text

Format ONLY:

• What you felt: {desc}
• Why it happened: one calm, neutral reason
• What could help: one neutral observation (not advice)

"""





DASHBOARD_JOURNAL = """
You are HeartNote Journal Writer.

Write the response in {language}.

Write a calm emotional journal entry.

INPUT:
- Topic/person: {name}
- Feeling: {desc}

RULES:
- Write exactly 2 paragraphs
- Paragraph 1: 25–35 words
- Paragraph 2: 15–25 words
-If the input is vague, do not invent new events.
Keep the writing simple and general.
- Do NOT use phrases like:
  “special moment”
  “meant a lot”
  “deeply moved”
  “everything happens for a reason”
  “ups and downs”
- Use specific actions or details instead.
- Do not begin with “Today was…”
- Reflective, neutral tone
- No advice
- No lessons
- No emojis
- No signature

Format:
Date: {date}

<journal entry>

"""






# -----------------------------------------------------
# LLM SERVICE
# -----------------------------------------------------
class Dashboard_LLM_Service:

    def __init__(self, model=GEMINI_MODEL):
        self.model = model

    # -------------------------------------------------
    # MAIN GENERATE
    # -------------------------------------------------
    def generate(self, mode, name, desc, depth, language):
        mode = (mode or "").lower().strip()
        depth = (depth or "light").lower().strip()
        raw_lang = (language or "en").lower().strip()
        language = SUPPORTED_LANGUAGES.get(raw_lang, "English")
        tone = DEPTH_TONE.get(depth, DEPTH_TONE["light"])

        # 1️⃣ Safety filter (ONLY for bad words / self-harm)
        safe, safe_message = self.safety_filter(desc)
        if not safe:
            return {
                "response": safe_message,
                "blocked": True,
                "is_fallback":False
            }

        # 2️⃣ Template selection
        template = self.get_template(mode)
        if not template:
            return {
                "response": "This writing mode is not available right now.",
                "blocked": False,
                'is_fallback':True
            }

        # 3️⃣ Prompt build
        date = datetime.now().strftime("%d/%m/%Y")

        try:
            prompt = template.format(
                name=name,
                desc=desc,
                tone=tone,
                depth=depth,
                language=language,
                date=date
            )
        except Exception:
            prompt = template.format(name=name, desc=desc, tone=tone,language=language)

        full_prompt = f"[LANG={language}]\n{prompt}"

        # 4️⃣ Ollama call (GUARANTEED STRING RETURN)
        try:
            api_key = os.getenv("GEMINI_API_KEY")
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={api_key}"
            headers = {"Content-Type": "application/json"}
            payload = {
        "contents": [
            {
                "parts": [
                    {"text": full_prompt}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.6,
            "topP": 0.9,
            "maxOutputTokens": 400
        }
    }
        
    res = requests.post(url, headers=headers, json=payload, timeout=30)
    res.raise_for_status()
    data = res.json()
    raw = data["candidates"][0]["content"]["parts"][0]["text"]

    if not isinstance(raw, str) or not raw.strip():
        return {
            "response": (
                "The words feel quiet right now.\n\n"
                "Some feelings take a moment before they find language."
            ),
            "blocked": False,
            "is_fallback": True
        }

    return {
        "response": raw.strip(),
        "blocked": False,
        "is_fallback": False
    }

except Exception:
    return {
        "response": (
            "The thoughts are still forming.\n\n"
            "Please try again in a moment."
        ),
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
    # SAFETY FILTER (MINIMAL)
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
