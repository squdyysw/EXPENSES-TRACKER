from fastapi import FastAPI, Request
from app.routes import expenses
from app.database import init_db
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import os

app = FastAPI(
    title="Expense Tracker API",
    description="Simple API to manage personal expenses",
    version="1.0.0"
)

init_db()  # создаём таблицу при старте

templates = Jinja2Templates(directory='app/templates')

app.mount("/static",
    StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")),
    name="static",)

app.include_router(expenses.router)

@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/favicon.ico")
async def favicon():
    return FileResponse("app/static/favicon.ico")
