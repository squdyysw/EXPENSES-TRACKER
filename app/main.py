"""
Main entry point for the Expense Tracker API.

Initializes the database, configures templates, mounts static files,
and registers application routes.
"""

import os
import logging
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from app.routes import expenses
from app.database import init_db


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


app = FastAPI(
    title="Expense Tracker API",
    description="Simple API to manage personal expenses.",
    version="1.0.0",
)

logger.info("Initializing database...")
init_db()
logger.info("Database initialized.")

templates = Jinja2Templates(directory="app/templates")

static_path = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")
logger.info(f"Static files mounted at {static_path}")


app.include_router(expenses.router)
logger.info("Expenses router loaded.")


@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    """
    Render the main application page.

    Args:
        request (Request): Current HTTP request.

    Returns:
        TemplateResponse: Rendered front-page template.
    """
    logger.debug("Rendering index page.")
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/favicon.ico")
async def favicon():
    """
    Serve the application favicon.

    Returns:
        FileResponse: Favicon file response.
    """
    path = "app/static/favicon.ico"
    logger.debug(f"Serving favicon from {path}")
    return FileResponse(path)
