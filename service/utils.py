from . import executor
from typing import Dict, List, Optional
import pandas as pd
import matplotlib.pyplot as plt
import json


def format_db_tables(tables: Optional[List[str]] = None) -> Dict[str, str]:
    results = []
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

    table_name = input("\nType the table name to consult: ").strip().lower()

    print(f"\n--- TABLE DATA: {table_name.upper()} ---")

    table_result_tuple = executor.execute_sql_by_query(
        f"SELECT * FROM {table_name}", fetch_results=True
    )

    if not table_result_tuple:
        return {"table": "No data found in the table.", "name": table_name}

    table_results, _ = table_result_tuple

    if not table_results:
        return {"table": "No data found in the table.", "name": table_name}

    colnames_result_tuple = executor.execute_sql_by_query(
        f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}' ORDER BY ordinal_position",
        fetch_results=True,
    )

    if not colnames_result_tuple:
        return {"table": "Could not retrieve column names.", "name": table_name}

    colnames_result, _ = colnames_result_tuple

    colnames = [col[0] for col in colnames_result]

    header = " | ".join(str(col).ljust(15) for col in colnames)
    separator = "-" * len(header)

    formatted_rows = []
    for row in table_results:
        formatted_rows.append(" | ".join(str(value).ljust(15) for value in row))

    table = f"{header}\n{separator}\n" + "\n".join(formatted_rows)
    return {"table": table, "name": table_name}


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


def generate_graph(data, columns, x_col, y_col, graph_type="bar"):
    if not isinstance(data, pd.DataFrame):
        df = pd.DataFrame(data, columns=columns)
    else:
        df = data

    if graph_type == "bar":
        df.plot(x=x_col, y=y_col, kind="bar")
    elif graph_type == "pie":
        df.set_index(x_col)[y_col].plot.pie(autopct="%1.1f%%")
    elif graph_type == "line":
        df.plot(x=x_col, y=y_col, kind="line")
    else:
        print("Unsupported graph type.")
        return

    plt.title(f"{y_col} by {x_col}")
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.tight_layout()
    plt.show()


def format_query_table(data, columns):
    if not data or not columns:
        return "No data to display."

    header = " | ".join(str(col).ljust(20) for col in columns)
    separator = "-" * len(header)
    formatted_rows = [" | ".join(str(value).ljust(20) for value in row) for row in data]
    table = f"{header}\n{separator}\n" + "\n".join(formatted_rows)
    return table


def tuples_to_json(results, columns):
    dict_list = [dict(zip(columns, row)) for row in results]
    return json.dumps(dict_list, ensure_ascii=False, indent=2)
