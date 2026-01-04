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
            "soft awareness growing, thoughts slowing down, comfort in stillness",
            "accepting the moment without resistance, feeling settled inside"
        ],
        "medium": [
            "understanding myself more clearly, balance forming, patience developing",
            "pausing without pressure, clarity replacing confusion, calm holding steady",
            "acceptance taking shape, emotions grounding themselves",
            "emotional steadiness forming, awareness becoming clearer"
        ],
        "deep": [
            "healing old layers silently, time softening memories, meaning forming slowly",
            "unresolved feelings resting deep, staying present with what remains",
            "inner depth unfolding quietly, emotions settling without answers",
            "silent emotions holding weight, depth staying unresolved"
        ]
    },

    "journal": {
        "light": [
            "small progress noticed today, hope staying nearby, growth happening quietly",
            "gentle emotions passing through, calm moments repeating",
            "simple awareness today, nothing heavy, nothing forced",
            "a light emotional tone carrying the day"
        ],
        "medium": [
            "mixed feelings today, still holding balance, still moving forward",
            "emotions steady but thoughtful, reflection guiding the day",
            "a calm rhythm forming, staying grounded throughout",
            "quiet emotional consistency shaping the day"
        ],
        "deep": [
            "thoughts felt layered today, meaning forming slowly, silence present",
            "emotional weight stayed close, still manageable, still steady",
            "depth without clarity, reflection staying unresolved",
            "inner heaviness noticed, calm still holding"
        ]
    },

    "notes": {
        "light": [
            "gentle care for myself, quiet reassurance, steady breathing",
            "soft reminders, progress without noise, patience intact",
            "kind awareness, slowing down, allowing space",
            "small emotional check-in, calm reassurance"
        ],
        "medium": [
            "confidence forming quietly, growth happening in silence",
            "steady emotional presence, calm recognition, inner balance",
            "soft strength appearing, staying centered",
            "emotional steadiness noticed, grounding maintained"
        ],
        "deep": [
            "unspoken emotions present, depth without urgency",
            "inner complexity noticed, allowing stillness",
            "weight beneath calm, remaining steady",
            "quiet emotional layers staying unresolved"
        ]
    },

    "affirmation": {
        "light": [
            "I am allowed to move slowly",
            "Gentleness is enough today",
            "I can stay present",
            "I do not need to rush"
        ],
        "medium": [
            "I remain grounded and steady",
            "I trust the pace of my growth",
            "I allow balance to form",
            "I stay calm within change"
        ],
        "deep": [
            "I honor emotions without resolving them",
            "Depth can exist without clarity",
            "Stillness is safe",
            "I allow complexity to remain"
        ]
    },

    "letters": {
        "light": [
            "warm memories lingering, softness remaining, peace slowly forming",
            "gentle connection felt, nothing rushed, nothing forced",
            "quiet appreciation staying, calm presence lasting",
            "soft emotions resting, warmth remaining"
        ],
        "medium": [
            "truth felt calmly, honesty without weight",
            "shared moments settling, clarity without intensity",
            "emotion staying balanced, grounded and sincere",
            "steady feelings holding space"
        ],
        "deep": [
            "unspoken feelings resting, depth remaining without answers",
            "memory holding space, silence speaking gently",
            "emotion lingering quietly, unresolved but present",
            "feelings staying deep, words unnecessary"
        ]
    },

    "poems": {
        "light": [
            "soft light returning, breath slowing, warmth staying",
            "gentle hope drifting, calm unfolding",
            "still moments glowing",
            "quiet warmth filling space"
        ],
        "medium": [
            "balance between thought and breath",
            "emotion standing quietly",
            "clarity forming slowly",
            "calm holding steady"
        ],
        "deep": [
            "silence holding meaning",
            "depth without sound",
            "emotion remaining",
            "stillness carrying weight"
        ]
    },

    "story": {
        "light": [
            "a calm turn of events, nothing dramatic, peace remaining",
            "quiet moments passing, feeling staying gently",
            "soft transition unfolding",
            "a gentle shift without tension"
        ],
        "medium": [
            "change arriving quietly, balance shaping the moment",
            "emotion grounding the scene",
            "nothing loud, yet meaningful",
            "steady emotion guiding the moment"
        ],
        "deep": [
            "unspoken shift occurring, silence carrying weight",
            "emotion outlasting the moment",
            "depth forming without resolution",
            "quiet intensity remaining after the moment"
        ]
    },

    "quotes": {
        "light": [
            "Soft moments matter",
            "Calm has its own strength",
            "Gentleness holds meaning",
            "Quiet feelings still count"
        ],
        "medium": [
            "Balance often speaks quietly",
            "Clarity doesn’t rush",
            "Presence is enough",
            "Stillness shapes understanding"
        ],
        "deep": [
            "Silence carries depth",
            "Not everything seeks answers",
            "Stillness holds truth",
            "Depth does not need noise"
        ]
    }
}


FALLBACK_CONTENT = {

    # --------------------------------
    # REFLECTION (25–45 words)
    # --------------------------------
    "reflection": {
        "light": [
            "Some feelings rise quietly around {desc}, settling without resistance and creating a soft awareness that feels natural, calm, and unforced.",
            "A gentle emotional state shaped by {desc} appeared without effort, allowing calm understanding to remain present in the moment.",
            "Nothing demanded attention within {desc}, yet a peaceful emotional layer stayed quietly, steady and supportive.",
            "The experience of {desc} carried light emotional weight, existing calmly without explanation or urgency."
        ],
        "medium": [
            "A balanced emotional tone formed through {desc}, steady and grounded, allowing reflection without pressure or confusion.",
            "The feeling connected to {desc} unfolded slowly, offering stability, patience, and emotional clarity over time.",
            "Within {desc}, emotions stayed centered, calm yet thoughtful, shaping the moment with quiet understanding.",
            "A composed emotional presence surrounded {desc}, neither intense nor distant, simply steady."
        ],
        "deep": [
            "The emotion within {desc} remained layered and quiet, resting beneath the surface and holding depth without resolution.",
            "Some feelings shaped by {desc} stayed present in silence, deep but gentle, resisting clear definition.",
            "An unresolved emotional weight tied to {desc} lingered calmly, existing without the need for answers.",
            "The inner response to {desc} carried depth, remaining steady and reflective long after the moment passed."
        ]
    },

    # --------------------------------
    # JOURNAL (25–45 words)
    # --------------------------------
    "journal": {
        "light": [
          "Date: {date}\n\nToday moved gently, with {desc} staying in the background, creating a calm emotional rhythm from morning to evening.",
"Date: {date}\n\nThe day felt light as {desc} allowed moments to pass softly, without needing attention or effort."  
        ],
        "medium": [
            "Date: {date}\n\nEmotions felt balanced today, as {desc} quietly supported reflection and steady awareness throughout the day.",
"Date: {date}\n\nThe presence of {desc} kept the day grounded, holding emotional balance during moments of pause."
        ],
        "deep": [
            "Date: {date}\n\nThe emotion surrounding {desc} felt layered today, quiet and meaningful, staying close without explanation.",
"Date: {date}\n\nSome unresolved feelings remained through {desc}, calm but deep, shaping inner awareness as the day passed."
        ]
    },

    # --------------------------------
    # POEMS (3–4 lines)
    # --------------------------------
    "poems": {
        "light": [
           "A soft feeling formed\naround {desc}\nresting without needing words.",
"Light emotion appears\nthrough {desc}\nthen settles calmly."
        ],
        "medium": [
            "Emotion shaped by {desc}\nstays between thought and breath\nquiet, but aware.",
"{desc} carries a feeling\nbalanced and present\nneither heavy nor distant."
        ],
        "deep": [
            "Something unresolved\nwithin {desc}\nremains, quietly breathing.",
"{desc} holds weight\nwithout explanation\nand stays."
        ]
    },

    # --------------------------------
    # LETTERS (25–45 words)
    # --------------------------------
    "letters": {
        "light": [
            "Dear {name},\n\nWarm moments shaped by {desc} rested gently, calm and unhurried, allowing space without expectation.\n\nWarmth By,\n💗 HeartNote AI",
"Dear {name},\n\nThrough {desc}, a light emotional calm settled naturally, steady and sincere.\n\nWarmth By,\n💗 HeartNote AI"
        ],
        "medium": [
            "Dear {name},\n\nEmotions surrounding {desc} unfolded with balance, thoughtful and grounded.\n\nWarmth By,\n💗 HeartNote AI",
"Dear {name},\n\n{desc} carried a composed emotional presence, reflective and clear.\n\nWarmth By,\n💗 HeartNote AI"
        ],
        "deep": [
            "Dear {name},\n\n{desc} remained quietly layered, holding depth without urgency or explanation.\n\nWarmth By,\n💗 HeartNote AI",
"Dear {name},\n\nAn unspoken depth connected to {desc} stayed present, calm and unresolved.\n\nWarmth By,\n💗 HeartNote AI"
        ]
    },

    # --------------------------------
    # STORY (25–45 words, max 2 sentences)
    # --------------------------------
    "story": {
        "light": [
            "The moment shaped by {desc} unfolded quietly, without urgency or expectation. Calm settled naturally, leaving a soft emotional stillness behind.",
            "Nothing rushed within {desc}, and the moment passed gently. A simple sense of peace remained, unnoticed but steady."
        ],
        "medium": [
            "The experience shaped by {desc} moved slowly, allowing emotions to settle with balance. Reflection stayed present without becoming heavy.",
           "Through {desc}, the moment held emotional steadiness. Meaning existed quietly, grounded and thoughtful."
        ],
        "deep": [
            "The moment connected to {desc} ended, but the feeling did not. It remained quietly, unresolved, carrying depth without needing explanation.",
            "Though the experience shaped by {desc} passed, its emotional weight stayed. Silence held what words could not."
        ]
    },

    # --------------------------------
    # QUOTES
    # --------------------------------
    "quotes": {
        "light": [
            "Some feelings shaped by {desc} need no explanation.",
            "Calm often lives quietly within {desc}.",
            "Gentle moments within {desc} still matter.",
            "Peace can exist naturally through {desc}."
        ],
        "medium": [
            "Balance within {desc} often speaks softly.",
            "Clarity connected to {desc} does not rush.",
            "Presence shaped by {desc} is enough.",
            "Emotion within {desc} can remain steady."
        ],
        "deep": [
            "Depth within {desc} often stays silent.",
            "Not every feeling in {desc} seeks answers.",
            "Stillness shaped by {desc} holds meaning.",
            "Some emotions tied to {desc} remain unresolved."
        ]
    },

    # --------------------------------
    # AFFIRMATION
    # --------------------------------
    "affirmation": {
        "light": [
            "This feeling shaped by {desc} is allowed.",
            "Calm within {desc} can remain.",
            "Gentleness through {desc} is enough.",
            "Peace shaped by {desc} is valid."
        ],
        "medium": [
            "Balance within {desc} is steady.",
            "The emotional pace of {desc} can be trusted.",
            "Clarity through {desc} can form slowly.",
            "Presence shaped by {desc} is grounding."
        ],
        "deep": [
            "Unresolved emotions within {desc} are allowed.",
            "Depth shaped by {desc} needs no answers.",
            "Stillness within {desc} can remain.",
            "Silence through {desc} holds meaning."
        ]
    },

    # --------------------------------
# NOTES (STRICT BULLETS) — H1 FINAL
# --------------------------------
"notes": {
    "light": [
        "• What you felt: gentle emotional calm around {desc}\n• Why it happened: quiet awareness\n• What remained: space",
        "• What you felt: light emotional ease within {desc}\n• Why it happened: natural pacing\n• What remained: stillness",
        "• What you felt: calm presence shaped by {desc}\n• Why it happened: emotional softness\n• What remained: quiet",
        "• What you felt: steady calm tied to {desc}\n• Why it happened: acceptance\n• What remained: openness"
    ],
    "medium": [
        "• What you felt: balanced emotional awareness in {desc}\n• Why it happened: grounding\n• What remained: steadiness",
        "• What you felt: steady emotions shaped by {desc}\n• Why it happened: inner balance\n• What remained: clarity",
        "• What you felt: calm emotional rhythm in {desc}\n• Why it happened: awareness\n• What remained: focus-free stillness",
        "• What you felt: emotional steadiness within {desc}\n• Why it happened: stability\n• What remained: consistency"
    ],
    "deep": [
        "• What you felt: unresolved depth tied to {desc}\n• Why it happened: inner complexity\n• What remained: stillness",
        "• What you felt: silent emotional weight within {desc}\n• Why it happened: reflection\n• What remained: time passing",
        "• What you felt: deep emotional presence in {desc}\n• Why it happened: memory\n• What remained: quiet depth",
        "• What you felt: layered emotion shaped by {desc}\n• Why it happened: awareness\n• What remained: space"
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
            safe_desc = get_suggested_desc(mode, depth, desc)
            fallback_mode = FALLBACK_CONTENT.get(mode, {})
            fallback_list = fallback_mode.get(depth, [])
            if fallback_list:
                text = random.choice(fallback_list).format(date=date,name=name,desc=safe_desc)
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
