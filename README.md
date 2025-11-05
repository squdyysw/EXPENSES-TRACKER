# Expense Tracker

Expense Tracker is a simple web application for managing personal expenses. It provides a complete CRUD (Create, Read, Update, Delete) interface with a REST API built using FastAPI, SQLite, and a clean HTML + JavaScript frontend.

## 🎯 Features
- Add, view, edit, and delete expenses (CRUD)
- Filter by category and date range
- Simple and intuitive UI (HTML + vanilla JS)
- FastAPI backend with Jinja2 templates and SQLite database

## 🛠️ Tech Stack
- Backend: FastAPI (Python)
- Database: SQLite
- Frontend: HTML, CSS, JavaScript (Fetch API)
- Templating: Jinja2

## 📂 Project Structure
app/ # Main application package
main.py # Entry point
routes/ # Routers and endpoints
models.py # Pydantic and DB models
database.py # DB setup and connection
crud.py # CRUD operations
templates/ # index.html and other templates
static/ # main.js, styles, etc.
requirements.txt
README.md

## 🚀 Quick Start
1. Clone the repository
   ```bash
   git clone https://github.com/andreydev/expense-tracker-fastapi.git
   cd expense-tracker-fastapi
2. Create a virtual environment and install dependencies
python -m venv venv
source venv/bin/activate   # macOS / Linux
venv\Scripts\activate      # Windows
pip install -r requirements.txt
3. Run the application
uvicorn app.main:app --reload
4. Open in browser
http://127.0.0.1:8000/

🧩 API Endpoints
Method Endpoint Description
GET /expenses/ Get list of expenses (supports filters)
POST /expenses/ Add a new expense
GET /expenses/{id} Get a single expense
PUT /expenses/{id} Update an expense
DELETE /expenses/{id} Delete an expense

📘 Example API Usage
Add a new expense:
curl -X POST "http://127.0.0.1:8000/expenses/" \
-H "Content-Type: application/json" \
-d '{"title": "Coffee", "amount": 3.5, "category": "Food"}'

💡 Notes
This project was created to practice backend development with FastAPI and implement full CRUD functionality. It includes structured code separation (models, CRUD, routes) and can be extended with user authentication or analytics dashboards.

📜 License
Licensed under the MIT License.
👤 Author
Developed by squdyysw
GitHub: https://github.com/squdyysw