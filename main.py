from service import executor
from service import utils

BLOCKED_TABLES = ["envolvido_crime", "agente_crime", "tipo_prova", "Tipo_Crime"]


def menu(num):
    if num == 1:
        return """
===========================
          MENU
===========================

1. Create: Start all the database schema
2. Insert: Populate the database
3. Show: Display all tables and their data
4. Query: Execute predefined queries
5. Update: Update values in a table
6. Delete: Delete specific values
7. IA: Perform AI-related tasks
8. Clear: Drop all database schema
0. Disconnect: Exit the program
===========================
"""
    elif num == 2:
        return """
===========================
       QUERY MENU
===========================

1. Query 1: Description of query 1
2. Query 2: Description of query 2
3. Query 3: Description of query 3
===========================
"""
    else:
        return "Menu error"


def create():
    executor.execute_sql_by_file("create.sql")


def insert():
    executor.execute_sql_by_file("populate.sql")


def clear():
    executor.execute_sql_by_file("drop.sql")


def show():
    result = utils.format_tables()
    print(result["table"])


def update():
    results = executor.execute_sql_by_file("tables.sql", fetch_results=True)
    filtered_results = []
    if results:
        for r in results:
            if r[0] not in BLOCKED_TABLES:
                filtered_results.append(r[0])

    table = utils.format_tables(filtered_results)
    print()
    print(table["table"])
    print()

    table_name = table["name"]

    if not table_name:
        print("No table selected.\n")
        return

    res = utils.return_pk_column_name(table_name)
    if not res:
        print("Table not found or without a pk\n")
        return
    pk_column_name = res[0]

    col = input("Type the column to receive an update: ").strip()
    if col == pk_column_name:
        print("Impossible to change a pk column!")
        return
    query_col = executor.execute_sql_by_query(
        f"SELECT column_name FROM information_schema.columns WHERE table_name = %s AND column_name = %s",
        params=(table_name, col),
        fetch_results=True,
    )
    if not query_col:
        print(f"Column '{col}' not found at table {table_name}\n")
        return

    id = input("Type the information id to locate: ").strip()
    query_id = executor.execute_sql_by_query(
        f"SELECT * FROM {table_name} WHERE {pk_column_name} = %s",
        params=(id,),
        fetch_results=True,
    )
    if not query_id:
        print(f"Id '{id}' not found at table {table_name}\n")
        return

    new_info = input(f"Type the new info to update into {col} with id {id}: ").strip()

    executor.execute_sql_by_query(
        f"UPDATE {table_name} SET {col} = %s WHERE {pk_column_name} = %s",
        params=(new_info, id),
    )

    print("\nUpdated successfully\n")
    print(utils.format_tables(filtered_results)["table"])
    print()


update()
