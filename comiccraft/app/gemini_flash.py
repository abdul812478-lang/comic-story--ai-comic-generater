import json
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai

env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(env_path)

API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=API_KEY) if API_KEY else None


def _fallback_outline(prompt, character_name, setting, tone, art_style):
    return [
        {
            "panel": 1,
            "title": "The First Spark",
            "scene_description": f"{character_name} begins a journey inspired by {prompt} in a {setting} setting with a {tone} mood.",
            "image_prompt": f"{character_name} in a {setting}, {art_style} style, cinematic lighting, high detail, vibrant colors"
        },
        {
            "panel": 2,
            "title": "A Hidden Clue",
            "scene_description": f"A mysterious clue reveals the next step in the adventure as {character_name} faces a challenge.",
            "image_prompt": f"{character_name} discovering a glowing clue in a {setting}, {art_style} comic book style, dynamic composition"
        },
        {
            "panel": 3,
            "title": "The Turning Point",
            "scene_description": f"The story shifts dramatically as the stakes rise and the hero must decide what matters most.",
            "image_prompt": f"{character_name} at a dramatic turning point in a {setting}, {art_style} style, strong emotion and contrast"
        },
        {
            "panel": 4,
            "title": "The Big Challenge",
            "scene_description": f"An obstacle blocks the path, testing courage, wit, and the strength of the team.",
            "image_prompt": f"{character_name} facing a major obstacle in a {setting}, {art_style} style, energetic action scene"
        },
        {
            "panel": 5,
            "title": "A New Dawn",
            "scene_description": f"The adventure ends with hope, growth, and a bright new chapter for {character_name}.",
            "image_prompt": f"{character_name} victorious at sunrise in a {setting}, {art_style} style, uplifting final scene"
        }
    ]


def generate_outline(prompt, character_name, setting, tone, art_style):
    if not client:
        return _fallback_outline(prompt, character_name, setting, tone, art_style)

    instruction = f"""
Create a 5-panel comic outline.

Story idea: {prompt}
Main character: {character_name}
Setting: {setting}
Tone: {tone}
Art style: {art_style}

Return ONLY valid JSON.
Do not use markdown.
Do not use ```json.
Do not add explanations.

The JSON must contain exactly 5 panels.

Each panel must have exactly these fields:
- panel
- title
- scene_description
- image_prompt

Return this structure:

[
  {{
    "panel": 1,
    "title": "Panel title",
    "scene_description": "Scene description",
    "image_prompt": "Detailed image generation prompt"
  }},
  {{
    "panel": 2,
    "title": "Panel title",
    "scene_description": "Scene description",
    "image_prompt": "Detailed image generation prompt"
  }},
  {{
    "panel": 3,
    "title": "Panel title",
    "scene_description": "Scene description",
    "image_prompt": "Detailed image generation prompt"
  }},
  {{
    "panel": 4,
    "title": "Panel title",
    "scene_description": "Scene description",
    "image_prompt": "Detailed image generation prompt"
  }},
  {{
    "panel": 5,
    "title": "Panel title",
    "scene_description": "Scene description",
    "image_prompt": "Detailed image generation prompt"
  }}
]
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=instruction
        )

        text = response.text.strip()

        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]

        if text.endswith("```"):
            text = text[:-3]

        text = text.strip()

        outline = json.loads(text)

        if not isinstance(outline, list):
            raise ValueError("Gemini response is not a list.")

        if len(outline) != 5:
            raise ValueError(f"Expected 5 panels, but received {len(outline)} panels.")

        return outline

    except Exception:
        return _fallback_outline(prompt, character_name, setting, tone, art_style)