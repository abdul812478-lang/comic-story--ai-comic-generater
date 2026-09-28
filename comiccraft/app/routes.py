from fastapi import APIRouter, Request, Form
from fastapi.responses import JSONResponse

from .gemini_flash import generate_outline
from .gemini_pro import generate_story
from .image_generator import generate_image
from .layout_builder import build_comic_layout
from .exporters import save_pdf

router = APIRouter()


@router.post("/generate")
async def generate_comic(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...)
):

    outline = generate_outline(
        story_prompt,
        character_name,
        setting,
        tone,
        art_style
    )

    story = generate_story(
        outline,
        character_name
    )

    image_paths = []

    for panel in outline:

        image_path = generate_image(
            panel["image_prompt"],
            panel["panel"]
        )

        image_paths.append(image_path)

    layout = build_comic_layout(
        outline,
        story,
        image_paths
    )

    pdf_path = save_pdf(layout)

    return request.app.state.templates.TemplateResponse(
        request=request,
        name="comic_preview.html",
        context={
            "layout": layout,
            "pdf_path": pdf_path
        }
    )


@router.get("/export-success")
async def export_success(request: Request):

    return request.app.state.templates.TemplateResponse(
        request=request,
        name="export_success.html",
        context={}
    )


@router.get("/test-image")
async def test_image():

    image_path = generate_image(
        "A brave fox exploring an enchanted forest, colorful comic book style",
        1
    )

    return {
        "image": image_path
    }