def build_comic_layout(outline, story, image_paths):

    panels = []

    story_text = story

    for index, panel in enumerate(outline):

        panel_number = panel["panel"]

        panels.append({
            "panel": panel_number,
            "title": panel["title"],
            "scene_description": panel["scene_description"],
            "image_prompt": panel["image_prompt"],
            "image": image_paths[index],
            "story": story_text
        })

    return panels