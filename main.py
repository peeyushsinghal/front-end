from fastapi import FastAPI, File, UploadFile, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Create a directory for animal images if it doesn't exist
Path("static/images").mkdir(parents=True, exist_ok=True)

# Sample animal images (you should replace these with actual image files)
animal_images = {
    "cat": "/static/images/cat.jpg",
    "dog": "/static/images/dog.jpg",
    "elephant": "/static/images/elephant.jpg"
}

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    logger.debug("Received request for root path")
    try:
        response = templates.TemplateResponse("index.html", {"request": request})
        logger.debug(f"Rendering template with context: {response.context}")
        return response
    except Exception as e:
        logger.error(f"Error rendering template: {str(e)}")
        raise

@app.get("/get_animal_image/{animal}")
async def get_animal_image(animal: str):
    if animal in animal_images:
        return {"image_url": animal_images[animal]}
    return {"error": "Animal not found"}

@app.post("/upload_file")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    return {
        "filename": file.filename,
        "size": len(contents),
        "content_type": file.content_type
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
