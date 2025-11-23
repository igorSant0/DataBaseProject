from . import executor
from typing import Dict, List, Optional
import pandas as pd
import matplotlib.pyplot as plt
import json
from tabulate import tabulate
import time

BLOCKED_TABLES = ["envolvido_crime", "agente_crime", "tipo_prova", "Tipo_Crime"]
DEPENDENCIES = {
    "delegacia": [("crime", "fk_delegacia_id_delegacia"), 
                  ("departamento", "fk_delegacia_id_delegacia"), 
                  ("agente", "fk_delegacia_id_delegacia"), 
                  ("veiculo", "fk_delegacia_id_delegacia")],
    "crime": [("prova", "fk_crime_id_crime"), 
              ("agente_crime", "fk_crime_id_crime"), 
              ("envolvido_crime", "fk_crime_id_crime")],
    "prova": [("tipo_prova", "fk_prova_id_prova")],
    "envolvido": [("envolvido_crime", "fk_envolvido_id_envolvido"), 
                  ("vitima", "fk_envolvido_id_envolvido"), 
                  ("criminoso", "fk_envolvido_id_envolvido"), 
                  ("suspeito", "fk_envolvido_id_envolvido"), 
                  ("testemunha", "fk_envolvido_id_envolvido")],

}


def format_db_tables(tables: Optional[List[str]] = None) -> Dict[str, str]:
    results = []
    try:
        if tables is None:
            result_tuple = executor.execute_sql_by_file("tables.sql", fetch_results=True)
            if not result_tuple:
                return {"table": "No tables found", "name": ""}
            results, _ = result_tuple
            if not results:
                return {"table": "No tables found", "name": ""}

            print("\n--- AVAILABLE TABLES ---")
            for idx, row in enumerate(results, start=1):
                print(f"{idx}. {row[0]}")
        else:
            results = tables
            if not results:
                return {"table": "No tables found", "name": ""}

            print("\n--- AVAILABLE TABLES ---")
            for idx, table_name in enumerate(results, start=1):
                print(f"{idx}. {table_name}")

        table_name = input("\nType the table name to see the infos: ").strip().lower()
        print(f"\n--- TABLE DATA: {table_name.upper()} ---")

        colnames_result_tuple = executor.execute_sql_by_query(
            f"SELECT column_name FROM information_schema.columns WHERE table_name = %s ORDER BY ordinal_position",
            params=(table_name,),
            fetch_results=True,
        )
        if not colnames_result_tuple:
            return {"table": "Could not retrieve column names.", "name": table_name}
        colnames_result, _ = colnames_result_tuple
        colnames = [col[0] for col in colnames_result]

        columns_to_select = [col for col in colnames if col != "is_deleted"]
        columns_str = ", ".join(columns_to_select)

        if "is_deleted" in colnames:
            query = f"SELECT {columns_str} FROM {table_name} WHERE is_deleted = FALSE"
        else:
            query = f"SELECT {columns_str} FROM {table_name}"

        table_result_tuple = executor.execute_sql_by_query(query, fetch_results=True)
        if not table_result_tuple:
            return {"table": "No data found in the table.", "name": table_name}

        table_results, columns = table_result_tuple
        if not table_results:
            return {"table": "No data found in the table.", "name": table_name}

        # Cria tabela formatada usando tabulate para melhor visualização
        formatted_table = tabulate(table_results, headers=columns, tablefmt="grid")
        
        return {"table": formatted_table, "name": table_name}

    except Exception as e:
        return {"table": f"Error: {e}", "name": ""}


def return_pk_column_name(table_name: Optional[str]) -> Optional[List[str]]:
    query_pk = """
    SELECT kcu.column_name
    FROM information_schema.table_constraints tc
    JOIN information_schema.key_column_usage kcu
      ON tc.constraint_name = kcu.constraint_name
      AND tc.table_schema = kcu.table_schema
    WHERE tc.constraint_type = 'PRIMARY KEY'
      AND tc.table_name = %s;
    """
    try:
        pk_result_tuple = executor.execute_sql_by_query(
            query_pk, params=(table_name,), fetch_results=True
        )
        if not pk_result_tuple:
            return None
        pk_result, _ = pk_result_tuple
        primary_keys = [row[0] for row in pk_result] if pk_result else []
        return primary_keys
    except:
        return None


def generate_graph(data, columns, x_col, y_col, graph_type="bar", title="none"):
    if not isinstance(data, pd.DataFrame):
        df = pd.DataFrame(data, columns=columns)
    else:
        df = data

    df[y_col] = pd.to_numeric(df[y_col], errors="coerce")
    if graph_type == "bar":
        df.plot(x=x_col, y=y_col, kind="bar")
    elif graph_type == "pie":
        df.set_index(x_col)[y_col].plot.pie(autopct="%1.1f%%")
    elif graph_type == "line":
        df.plot(x=x_col, y=y_col, kind="line")
    else:
        print("Unsupported graph type.")
        return

    plt.title(title)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.tight_layout()
    plt.show()


def format_query_table(data, columns):
    if not data or not columns:
        return "No data to display."

    return tabulate(data, headers=columns, tablefmt="grid")


def tuples_to_json(results, columns):
    dict_list = [dict(zip(columns, row)) for row in results]
    return json.dumps(dict_list, ensure_ascii=False, indent=2)


def menu(num):
    time.sleep(0.5)
    if num == 1:
        return """
===========================
          MENU
===========================

1. Init: Execute clear, create and populate at same time
2. Create: Start all the database schema
3. Insert: Populate the database
4. Show: Display all tables and their data
5. Query: Execute predefined queries
6. Update: Update values in a table
7. Delete: Delete specific values
8. IA: Perform AI-related tasks
9. Clear: Drop all database schema
0. Disconnect: Exit the program
===========================
"""
        print()
    elif num == 2:
        return """
===========================
       QUERY MENU
===========================

1. Crime statistics: Shows, for each crime, the total of agents, total of evidences and the average of evidences per agent.
2. Crimes by agent role: Shows, for each agent role, the total number of crimes they investigated.
3. Crime type average age: Shows, for each crime type, the average age of the involved people.
0. Return to main menu
===========================
"""
        print()
    else:
        return "Menu error"