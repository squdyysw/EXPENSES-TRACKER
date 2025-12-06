"""
Main entry point for the Expense Tracker API.
"""

import os
import logging
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from app.routes import expenses
from app.database import init_db


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger("expense_tracker")

app = FastAPI(
    title="Expense Tracker API",
    description="Simple API to manage personal expenses.",
    version="1.0.0",
)

if os.environ.get("TESTING") != "1":
    logger.info("Initializing database...")
    init_db()
    logger.info("Database initialized.")


templates = Jinja2Templates(directory="app/templates")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
logger.info(f"Static files mounted at {STATIC_DIR}")

app.include_router(expenses.router)
logger.info("Expenses router loaded.")


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.info(f"{request.method} {request.url}")
        response = await call_next(request)
        logger.info(f"Response status: {response.status_code}")
        return response

app.add_middleware(LoggingMiddleware)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc}")
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )


@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    logger.debug("Rendering index page.")
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/favicon.ico")
async def favicon():
    path = "app/static/favicon.ico"
    logger.debug(f"Serving favicon from {path}")
    return FileResponse(path)