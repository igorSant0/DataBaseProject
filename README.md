# DataBaseProject

This repository contains the **final project for a Database course**: database **schema**, **data population**, and a **Python CLI program** to create/populate/query/manage the database from the terminal.

---

## Main purpose

- Create and populate a PostgreSQL database using SQL scripts
- Interact with the database through a simple terminal menu:
  - initialize database (drop → create → populate)
  - show tables
  - run predefined queries (and display results)
  - update records
  - soft-delete records
- Use **AI** to turn a natural language request into SQL and interpret the results

---

## Tools used

- **Python**
- **PostgreSQL**
- **psycopg** (database driver)
- **python-dotenv** (environment variables)
- **pandas + tabulate** (format query results as tables)
- **matplotlib** (generate graphs for some queries)
- **OpenAI API** via the `openai` Python package (AI integration)

Dependencies are listed in `requirements.txt`.

---

## AI integration

The project has an **AI mode** that:
1. reads the database schema from `sql/create.sql`
2. asks the user for a question in natural language
3. uses an LLM (OpenAI) to generate a SQL query
4. runs the SQL in PostgreSQL
5. prints the results and an interpretation

You’ll need an OpenAI API key configured in your environment for this option.

---

## How to run

### 1) Install dependencies
```bash
pip install -r requirements.txt
```

### 2) Configure environment variables
This project uses `python-dotenv`, so you can create a `.env` file in the project root with:
- PostgreSQL connection settings (host, port, db name, user, password)
- OpenAI key (for AI mode)

(Variable names must match what `service/connector.py` expects.)

### 3) Run
```bash
python main.py
```

---

## What you will see when you run it

When you execute `python main.py`, you will see a **terminal menu** where you can choose options such as:

- **Init** (drop tables → create schema → populate data)
- **Create schema**
- **Populate database**
- **Show tables**
- **Run predefined queries** (prints tables and may generate graphs)
- **Update data**
- **Delete data** (soft delete)
- **AI mode** (natural language → SQL → results + interpretation)
- **Clear database** (drop)

The program will print confirmations (success/error messages) and query outputs directly in the console.

---
