import json
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai

env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(env_path)

api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None


def generate_story(outline, character_name):
    if not client:
        return (
            f"{character_name} begins an epic adventure guided by curiosity and courage. "
            "Each panel reveals a new clue, a new challenge, and a deeper sense of purpose. "
            "By the final scene, the hero has grown stronger and the story closes on a hopeful, triumphant note."
        )

    prompt = f"""
Create a complete comic story from this outline.

Main character: {character_name}

Outline:
{json.dumps(outline, indent=2)}

For each panel, include:
Panel number
Narration
Dialogue

Return readable text only.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        if not response.text:
            raise RuntimeError("Gemini returned an empty response.")

        return response.text.strip()
    except Exception:
        return (
            f"{character_name} begins an epic adventure guided by curiosity and courage. "
            "Each panel reveals a new clue, a new challenge, and a deeper sense of purpose. "
            "By the final scene, the hero has grown stronger and the story closes on a hopeful, triumphant note."
        )


if __name__ == "__main__":
    outline = [
        {
            "panel": 1,
            "title": "The Discovery",
            "scene_description": "Alex finds a mysterious map.",
            "image_prompt": "A young hero discovering an ancient glowing map",
        }
    ]

    print(generate_story(outline, "Alex"))
