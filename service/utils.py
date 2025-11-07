from . import executor
from typing import Dict, List, Optional


def format_tables(tables: Optional[List[str]] = None) -> Dict[str, str]:
    results = []

    if tables is None:
        results = executor.execute_sql_by_file("tables.sql", fetch_results=True)
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

    table_results = executor.execute_sql_by_query(
        f"SELECT * FROM {table_name}", fetch_results=True
    )

    if not table_results:
        return {"table": "No data found in the table.", "name": table_name}

    colnames_result = executor.execute_sql_by_query(
        f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}' ORDER BY ordinal_position",
        fetch_results=True,
    )

    if not colnames_result:
        return {"table": "Could not retrieve column names.", "name": table_name}

    colnames = [col[0] for col in colnames_result]

    header = " | ".join(str(col).ljust(15) for col in colnames)
    separator = "-" * len(header)

    formatted_rows = []
    for row in table_results:
        formatted_rows.append(" | ".join(str(value).ljust(15) for value in row))

    table = f"{header}\n{separator}\n" + "\n".join(formatted_rows)
    return {"table": table, "name": table_name}
