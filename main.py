# from fastapi import FastAPI
# from app.api import health

# app = FastAPI(title="IoT Laptop Server")
# app.include_router(health.router)

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api import health

app = FastAPI(title="IoT Laptop Server")

app.include_router(health.router)

app.mount("/static", StaticFiles(directory="app/ui/static"), name="static")
templates = Jinja2Templates(directory="app/ui/templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request}
    )