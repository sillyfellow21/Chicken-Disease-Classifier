from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.endpoints import router as api_router
from src.endpoints import init_model
import threading

app = FastAPI(title="Chicken Disease Classifier")

# Mount static for any future CSS/JS files
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Include the API router
app.include_router(api_router, prefix="/api")

@app.on_event("startup")
async def startup_event():
    # Initialize the model in the background so app starts fast
    t = threading.Thread(target=init_model)
    t.start()

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")
