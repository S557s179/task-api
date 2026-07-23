# Task API

A simple CRUD Task API built with FastAPI and SQLite.

## Features

- Create tasks
- Read all tasks
- Read a single task
- Update tasks
- Delete tasks
- Data persists after restarting the server

## Why SQLite?

SQLite is a lightweight relational database that stores all data in a single file (`tasks.db`). It requires no separate database server and is ideal for small projects and learning SQL.

## Installation

1. Clone the repository

```bash
git clone <your-github-repository>
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the application

```bash
uvicorn main:app --reload
```

or

```bash
python -m uvicorn main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

## Database

The SQLite database is automatically created as:

```
tasks.db
```

The application also automatically:

- Creates the `tasks` table if it does not exist.
- Inserts three sample tasks only on the first run.

## Example SQL Query

```sql
SELECT * FROM tasks;
```

## Screenshot

Add a screenshot of your SQLite database here (for example, from DB Browser for SQLite).

```
screenshots/database.png
```
