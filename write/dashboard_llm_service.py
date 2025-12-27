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

SUGGESTION_CONTENT = {

    "reflection": {
        "light": [
            "a calm sense slowly returning, learning gently, allowing things to stay as they are",
            "quiet peace settling in, breathing easier, letting moments pass naturally",
            "soft awareness growing, thoughts slowing down, comfort in stillness"
        ],
        "medium": [
            "understanding myself more clearly, balance forming, patience developing",
            "pausing without pressure, clarity replacing confusion, calm holding steady",
            "acceptance taking shape, emotions grounding themselves"
        ],
        "deep": [
            "healing old layers silently, time softening memories, meaning forming slowly",
            "unresolved feelings resting deep, staying present with what remains",
            "inner depth unfolding quietly, emotions settling without answers"
        ]
    },

    "journal": {
        "light": [
            "small progress noticed today, hope staying nearby, growth happening quietly",
            "gentle emotions passing through, calm moments repeating",
            "simple awareness today, nothing heavy, nothing forced"
        ],
        "medium": [
            "mixed feelings today, still holding balance, still moving forward",
            "emotions steady but thoughtful, reflection guiding the day",
            "a calm rhythm forming, staying grounded throughout"
        ],
        "deep": [
            "thoughts felt layered today, meaning forming slowly, silence present",
            "emotional weight stayed close, still manageable, still steady",
            "depth without clarity, reflection staying unresolved"
        ]
    },

    "notes": {
        "light": [
            "gentle care for myself, quiet reassurance, steady breathing",
            "soft reminders, progress without noise, patience intact",
            "kind awareness, slowing down, allowing space"
        ],
        "medium": [
            "confidence forming quietly, growth happening in silence",
            "steady emotional presence, calm recognition, inner balance",
            "soft strength appearing, staying centered"
        ],
        "deep": [
            "unspoken emotions present, depth without urgency",
            "inner complexity noticed, allowing stillness",
            "weight beneath calm, remaining steady"
        ]
    },

    "affirmation": {
        "light": [
            "I am allowed to move slowly",
            "Gentleness is enough today",
            "I can stay present"
        ],
        "medium": [
            "I remain grounded and steady",
            "I trust the pace of my growth",
            "I allow balance to form"
        ],
        "deep": [
            "I honor emotions without resolving them",
            "Depth can exist without clarity",
            "Stillness is safe"
        ]
    },

    "letters": {
        "light": [
            "warm memories lingering, softness remaining, peace slowly forming",
            "gentle connection felt, nothing rushed, nothing forced",
            "quiet appreciation staying, calm presence lasting"
        ],
        "medium": [
            "truth felt calmly, honesty without weight",
            "shared moments settling, clarity without intensity",
            "emotion staying balanced, grounded and sincere"
        ],
        "deep": [
            "unspoken feelings resting, depth remaining without answers",
            "memory holding space, silence speaking gently",
            "emotion lingering quietly, unresolved but present"
        ]
    },

    "poems": {
        "light": [
            "soft light returning, breath slowing, warmth staying",
            "gentle hope drifting, calm unfolding",
            "still moments glowing"
        ],
        "medium": [
            "balance between thought and breath",
            "emotion standing quietly",
            "clarity forming slowly"
        ],
        "deep": [
            "silence holding meaning",
            "depth without sound",
            "emotion remaining"
        ]
    },

    "story": {
        "light": [
            "a calm turn of events, nothing dramatic, peace remaining",
            "quiet moments passing, feeling staying gently",
            "soft transition unfolding"
        ],
        "medium": [
            "change arriving quietly, balance shaping the moment",
            "emotion grounding the scene",
            "nothing loud, yet meaningful"
        ],
        "deep": [
            "unspoken shift occurring, silence carrying weight",
            "emotion outlasting the moment",
            "depth forming without resolution"
        ]
    },

    "quotes": {
        "light": [
            "Soft moments matter",
            "Calm has its own strength",
            "Gentleness holds meaning"
        ],
        "medium": [
            "Balance often speaks quietly",
            "Clarity doesn’t rush",
            "Presence is enough"
        ],
        "deep": [
            "Silence carries depth",
            "Not everything seeks answers",
            "Stillness holds truth"
        ]
    }
}


FALLBACK_CONTENT = {

    # -------------------------------
    # REFLECTION (1 paragraph | 25–45 words)
    # -------------------------------
    "reflection": {
        "light": [
            "Some feelings arrive quietly around {desc}, staying without questions, resting gently inside the moment and allowing calm awareness to remain.",
            "The emotion shaped by {desc} felt soft and light, present without needing explanation, existing naturally within the experience.",
            "Nothing demanded attention in {desc}, yet a calm emotional presence remained, steady and unspoken."
        ],
        "medium": [
            "A steady emotional tone formed around {desc}, grounded and calm, shaping the moment naturally without urgency or resistance.",
            "The feeling connected to {desc} unfolded slowly, balanced and sincere, holding quiet emotional clarity.",
            "There was emotional clarity in {desc} without intensity, just quiet awareness settling in."
        ],
        "deep": [
            "The feeling beneath {desc} lingered below the surface, layered and silent, staying longer than expected.",
            "Some emotions within {desc} carry depth without noise, and this one remained quietly present.",
            "The emotion shaped by {desc} filled the quiet inner space, unresolved yet calm."
        ]
    },

    # -------------------------------
    # JOURNAL (1 paragraph with date | 25–45 words)
    # -------------------------------
    "journal": {
        "light": [
            "Date: {date}\n\nToday felt gentle and slow as {desc} stayed in the background, creating a calm emotional presence throughout the day.",
            "Date: {date}\n\nThe day moved quietly with {desc}, carrying a soft emotional tone without pressure.",
            "Date: {date}\n\nNothing stood out strongly in {desc}, yet the feeling stayed."
        ],
        "medium": [
            "Date: {date}\n\nA steady emotional rhythm formed around {desc}, grounded and calm throughout the day.",
            "Date: {date}\n\nThe feeling linked to {desc} remained present, neutral and reflective.",
            "Date: {date}\n\nEmotional balance shaped the day as {desc} stayed quietly present."
        ],
        "deep": [
            "Date: {date}\n\nThe emotion connected to {desc} felt layered today, carrying depth and silence.",
            "Date: {date}\n\nSome feelings within {desc} resist clarity, and this one stayed.",
            "Date: {date}\n\nThe day carried emotional weight through {desc}, unresolved yet steady."
        ]
    },

    # -------------------------------
    # POEM (3–4 lines)
    # -------------------------------
    "poems": {
        "light": [
            "A quiet feeling\nformed around {desc}\nthen moved on."
        ],
        "medium": [
            "An emotion shaped by {desc}\nstayed between breath and thought."
        ],
        "deep": [
            "Something unspoken\nwithin {desc}\nsettled deeply and remained."
        ]
    },

    # -------------------------------
    # LETTER (USES {name} + SIGNATURE | 25–45 words)
    # -------------------------------
    "letters": {
        "light": [
            "Dear {name},\n\nA gentle feeling shaped by {desc} stayed quietly, without urgency or demand, simply resting in the moment.\n\nWarmth By,\n💗 HeartNote AI"
        ],
        "medium": [
            "Dear {name},\n\nThe emotion surrounding {desc} unfolded slowly, grounded and sincere, holding its place calmly.\n\nWarmth By,\n💗 HeartNote AI"
        ],
        "deep": [
            "Dear {name},\n\nSome emotions tied to {desc} linger without explanation, layered and quiet, staying longer than expected.\n\nWarmth By,\n💗 HeartNote AI"
        ]
    },

    # -------------------------------
    # STORY (25–45 words | 2 sentences max)
    # -------------------------------
    "story": {
        "light": [
            "The moment shaped by {desc} passed gently. A quiet feeling remained, steady and unnoticed."
        ],
        "medium": [
            "Nothing dramatic occurred around {desc}. Still, the emotion stayed present and grounded."
        ],
        "deep": [
            "The moment connected to {desc} ended, but the feeling did not. It stayed in silence, carrying depth."
        ]
    },

    # -------------------------------
    # QUOTE (1 sentence)
    # -------------------------------
    "quotes": {
        "light": [
            "Some feelings formed around {desc} exist without needing explanation."
        ],
        "medium": [
            "Not every emotion within {desc} arrives with clarity."
        ],
        "deep": [
            "Depth within {desc} often lives in silence."
        ]
    },

    # -------------------------------
    # AFFIRMATION (1–2 lines)
    # -------------------------------
    "affirmation": {
        "light": [
            "This feeling shaped by {desc} is allowed to exist."
        ],
        "medium": [
            "This moment within {desc} does not need explanation."
        ],
        "deep": [
            "Even unresolved emotions within {desc} deserve space."
        ]
    },

    # -------------------------------
    # NOTES (STRICT BULLET FORMAT)
    # -------------------------------
    "notes": {
        "light": [
            "• What you felt: a quiet emotional presence around {desc}\n• Why it happened: inner awareness\n• What could help: gentle space"
        ],
        "medium": [
            "• What you felt: steady emotional awareness within {desc}\n• Why it happened: emotional balance\n• What could help: grounding presence"
        ],
        "deep": [
            "• What you felt: deep unresolved emotion tied to {desc}\n• Why it happened: inner complexity\n• What could help: stillness"
        ]
    }
}

def get_suggested_desc(mode, depth, original_desc):
        suggestions = SUGGESTION_CONTENT.get(mode, {}).get(depth, [])
        if suggestions:
            return random.choice(suggestions)
    return original_desc

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
            suggested_desc = get_suggested_desc(mode, depth, safe_desc)
            if fallback_list:
                text = random.choice(fallback_list).format(date=date,name=name,desc=sugesstion_desc)
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
