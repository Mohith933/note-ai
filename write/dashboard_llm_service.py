import requests
import json
import os
from datetime import datetime

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:3b"


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





# -----------------------------------------------------
# LLM SERVICE
# -----------------------------------------------------
class Dashboard_LLM_Service:

    def __init__(self, model=MODEL_NAME):
        self.model = model

    def generate(self, mode, name, desc, depth, language):
        depth = depth.lower().strip()
        tone = DEPTH_TONE.get(depth, DEPTH_TONE["light"])
        mode = mode.lower().strip()
        language = language.lower().strip()

        

        safe, result = self.safety_filter(desc)
        if not safe:
            return {
        "response": result,
        "blocked": True
        }

        if os.environ.get("RENDER"):
            return {
        "response": "⚠️ AI generation is available only in local mode.",
        "blocked": False
        }





        # Pick correct template
        if mode == "reflection":
            template = DASHBOARD_REFLECTION
        elif mode == "letters":
            template = DASHBOARD_LETTER
        elif mode == "poems":
            template = DASHBOARD_POEM
        elif mode == "story":
            template = DASHBOARD_STORY
        elif mode == "quotes":
            template = DASHBOARD_QUOTE
        elif mode == "affirmation":
            template = DASHBOARD_AFFIRMATION
        elif mode == "notes":
            template = DASHBOARD_NOTE
        elif mode == "journal":
            date = datetime.now().strftime("%d/%m/%Y")
            template = DASHBOARD_JOURNAL
            prompt = template.format(date=date, name=name, desc=desc, depth=depth,tone=tone)

            return requests.post(OLLAMA_URL,
    json={"model":MODEL_NAME, "prompt": prompt, "stream": False}
).json().get("response", "").strip()
        else:
            return "⚠ Unknown dashboard mode"
        
        # Build final prompt
        prompt = template.format(name=name, desc=desc, tone=tone)
        prompt = f"[LANG={language}]\n" + prompt    # ← ADD THIS

# Call Ollama
        payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
        }
        res = requests.post(OLLAMA_URL, json=payload)
        return {
    "response": res.json().get("response", "").strip(),
    "blocked": False
    }


    
    
    def safety_filter(self, text):
        t = text.lower().strip()
        bad_words = [
        "fuck", "bitch", "shit", "asshole",
        "bastard", "slut", "dick", "pussy",
        "kill you", "hurt you"
        ]
        for w in bad_words:
            if w in t:
                return False, "⚠️ Unsafe or harmful language detected. Please rewrite your text more respectfully."
            
        selfharm_patterns = [
        "kill myself",
        "kill me",
        "i want to die",
        "end my life",
        "i want to disappear",
        "i hurt myself",
        "self harm",
        "i can't live",
        "no reason to live"
        ]
        for s in selfharm_patterns:
            if s in t:
                return False, (
                "⚠️ HeartNote AI cannot generate this.\n"
                "Here is a gentle, safe message instead:\n\n"
                "• You deserve care.\n"
                "• You are not alone.\n"
                "• Your feelings matter.\n"
            )
        return True, text



