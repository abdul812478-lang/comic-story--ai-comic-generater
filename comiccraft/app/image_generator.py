import os
import random
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

BASE_DIR = Path(__file__).resolve().parent.parent


def _draw_background(draw, width, height, scene):
    if scene == "forest":
        sky = (126, 206, 244)
        ground = (81, 156, 90)
        accent = (250, 204, 21)
        draw.rectangle((0, 0, width, height), fill=(144, 217, 255))
        draw.ellipse((width - 260, 40, width - 30, 270), fill=(255, 240, 170))
        for i in range(0, width, 60):
            draw.polygon([(i, height), (i + 30, height - 140), (i + 60, height)], fill=(28, 90, 65))
        for i in range(0, width, 90):
            draw.ellipse((i, 110, i + 30, 170), fill=(255, 255, 255))
        draw.rectangle((0, height * 0.68, width, height), fill=ground)
        draw.rectangle((0, height * 0.68, width, height), fill=ground)
        draw.polygon([(0, height * 0.75), (width * 0.25, height * 0.55), (width * 0.5, height * 0.75)], fill=(55, 114, 76))
        draw.polygon([(width * 0.5, height * 0.75), (width * 0.75, height * 0.6), (width, height * 0.75)], fill=(38, 102, 66))
        return sky, ground, accent

    if scene == "space":
        draw.rectangle((0, 0, width, height), fill=(10, 15, 40))
        for _ in range(120):
            x = random.randint(10, width - 10)
            y = random.randint(10, height - 10)
            r = random.randint(1, 3)
            draw.ellipse((x, y, x + r, y + r), fill=(255, 255, 255))
        draw.ellipse((width * 0.72, height * 0.18, width * 0.92, height * 0.42), fill=(118, 129, 255))
        draw.ellipse((width * 0.15, height * 0.25, width * 0.4, height * 0.55), fill=(255, 230, 120))
        draw.rectangle((0, height * 0.75, width, height), fill=(20, 30, 60))
        return (10, 15, 40), (20, 30, 60), (255, 209, 102)

    if scene == "city":
        draw.rectangle((0, 0, width, height), fill=(129, 179, 255))
        draw.ellipse((width - 220, 40, width - 40, 220), fill=(255, 214, 102))
        for x in range(40, width - 40, 70):
            h = random.randint(120, 220)
            draw.rectangle((x, height - h, x + 42, height), fill=(46, 55, 74))
            for wx in range(x + 10, x + 32, 10):
                draw.rectangle((wx, height - h + 18, wx + 6, height - h + 44), fill=(240, 232, 163))
        draw.rectangle((0, height * 0.72, width, height), fill=(61, 85, 103))
        return (129, 179, 255), (61, 85, 103), (255, 214, 102)

    if scene == "school":
        draw.rectangle((0, 0, width, height), fill=(255, 214, 138))
        draw.rectangle((0, height * 0.7, width, height), fill=(118, 168, 143))
        for x in range(40, width - 40, 100):
            draw.rectangle((x, height * 0.48, x + 55, height * 0.72), fill=(255, 248, 220))
            draw.rectangle((x + 12, height * 0.42, x + 45, height * 0.48), fill=(255, 151, 81))
        draw.ellipse((width * 0.75, 45, width * 0.92, 160), fill=(255, 243, 167))
        return (255, 214, 138), (118, 168, 143), (255, 151, 81)

    draw.rectangle((0, 0, width, height), fill=(200, 230, 255))
    return (200, 230, 255), (100, 180, 120), (255, 225, 130)


def _draw_character(draw, center_x, center_y, scene, prompt):
    # Comic silhouette with exaggerated proportions.
    if "fox" in prompt.lower() or "animal" in prompt.lower():
        draw.ellipse((center_x - 70, center_y - 100, center_x + 70, center_y + 30), fill=(255, 140, 60))
        draw.polygon([(center_x - 30, center_y - 115), (center_x - 15, center_y - 165), (center_x + 10, center_y - 115)], fill=(255, 170, 90))
        draw.polygon([(center_x + 30, center_y - 115), (center_x + 45, center_y - 165), (center_x + 65, center_y - 115)], fill=(255, 170, 90))
        draw.ellipse((center_x - 35, center_y + 20, center_x + 110, center_y + 120), fill=(255, 160, 100))
        draw.polygon([(center_x + 85, center_y + 30), (center_x + 150, center_y + 80), (center_x + 110, center_y + 120)], fill=(255, 170, 90))
        draw.ellipse((center_x - 12, center_y - 5, center_x + 18, center_y + 25), fill=(0, 0, 0))
        draw.ellipse((center_x + 38, center_y - 5, center_x + 68, center_y + 25), fill=(0, 0, 0))
        draw.arc((center_x - 20, center_y + 5, center_x + 40, center_y + 45), start=200, end=340, fill=(32, 32, 32), width=4)
        return

    # Generic hero figure
    draw.ellipse((center_x - 52, center_y - 90, center_x + 52, center_y + 10), fill=(52, 107, 235))
    draw.rectangle((center_x - 35, center_y + 10, center_x + 35, center_y + 140), fill=(84, 132, 245))
    draw.line((center_x, center_y + 140, center_x - 30, center_y + 230), fill=(33, 38, 41), width=10)
    draw.line((center_x, center_y + 140, center_x + 35, center_y + 230), fill=(33, 38, 41), width=10)
    draw.line((center_x - 35, center_y + 80, center_x - 90, center_y + 150), fill=(33, 38, 41), width=10)
    draw.line((center_x + 35, center_y + 80, center_x + 90, center_y + 150), fill=(33, 38, 41), width=10)
    draw.ellipse((center_x - 12, center_y - 20, center_x + 12, center_y + 10), fill=(0, 0, 0))
    draw.ellipse((center_x - 32, center_y - 10, center_x - 15, center_y + 12), fill=(0, 0, 0))
    draw.ellipse((center_x + 15, center_y - 10, center_x + 32, center_y + 12), fill=(0, 0, 0))


def _add_speech_bubble(draw, prompt):
    bubble = (50, 60, 250, 130)
    draw.rounded_rectangle(bubble, radius=20, fill=(255, 255, 255), outline=(25, 25, 25), width=4)
    text = re.sub(r"\s+", " ", prompt[:40]).strip()
    draw.text((70, 86), text, fill=(25, 25, 25))


def _make_comic_panel_png(output_path: Path, prompt: str, panel_number: int) -> str:
    width, height = 900, 600
    image = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    prompt_lower = prompt.lower()
    if "space" in prompt_lower:
        scene = "space"
    elif "city" in prompt_lower:
        scene = "city"
    elif "school" in prompt_lower:
        scene = "school"
    else:
        scene = "forest"

    _draw_background(draw, width, height, scene)
    _add_speech_bubble(draw, prompt)
    _draw_character(draw, width // 2, height * 0.7, scene, prompt)

    draw.rounded_rectangle((20, 20, width - 20, height - 20), radius=24, outline=(20, 20, 20), width=6, fill=None)
    draw.text((width // 2, 560), f"Panel {panel_number}", anchor="mm", fill=(20, 20, 20), font=None)
    image = image.filter(ImageFilter.SMOOTH_MORE)
    image.save(output_path, format="PNG")
    return "/" + str(output_path.relative_to(BASE_DIR)).replace("\\", "/")


def generate_image(prompt, panel_number):
    output_dir = BASE_DIR / "static" / "panels"

    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except FileExistsError:
        if output_dir.exists() and not output_dir.is_dir():
            output_dir.unlink()
            output_dir.mkdir(parents=True, exist_ok=True)

    safe_name = re.sub(r"[^a-zA-Z0-9_-]", "_", prompt[:50])
    filename = f"panel_{panel_number}_{safe_name}.png"
    output_path = output_dir / filename

    return _make_comic_panel_png(output_path, prompt, panel_number)