# SQL Agent

An AI-powered SQL assistant that converts plain English questions into SQL queries and executes them against a SQLite database.

## What it does

This project allows users to ask questions in natural language, such as:

- Top 5 customers by total spend
- Number of tracks per genre
- Total sales by country

The application uses an OpenAI model to generate SQL, validates it, executes it on the Chinook sample database, and returns the results.

## Tech Stack

- Python
- FastAPI
- OpenAI API
- SQLite
- SQLGlot
- python-dotenv
- Uvicorn

## Project Structure

sql-agent/
│
├── app/
│   ├── db.py
│   ├── llm.py
│   ├── schema.py
│   └── __init__.py
│
├── dsa/
├── notes/
├── tests/
│
├── chinook.db
├── .env
├── pyproject.toml
└── README.md
```

## How to Run

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd sql-agent
```

### 2. Install dependencies

```bash
uv sync
```

Or if starting from scratch:

```bash
uv add openai fastapi uvicorn sqlglot python-dotenv
```

### 3. Add your API key

Create a `.env` file:

### 4. Start the application

```bash
uv run uvicorn app.main:app --reload
```

### 5. Open the API


Use the interactive Swagger UI to ask questions in natural language.

