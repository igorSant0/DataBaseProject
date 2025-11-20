from . import connector
import os
import psycopg2
from typing import Optional, Tuple, List, Any

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SQL_DIR = os.path.join(BASE_DIR, "sql")


def execute_sql_by_file(
    file_name: str, params=None, fetch_results: bool = False
) -> Optional[Tuple[List[Tuple[Any, ...]], List[str]]]:
    conn = None
    cursor = None
    file_path = os.path.join(SQL_DIR, file_name)

    try:
        conn = connector.connect()
        if conn is None:
            raise Exception("Failed to get database connection.")

        cursor = conn.cursor()

        with open(file_path, "r", encoding="utf-8") as f:
            sql_commands = f.read().split(";")

        for sql_command in sql_commands:
            sql_command = sql_command.strip()
            if sql_command:
                cursor.execute(sql_command, params)

        if fetch_results:
            results = cursor.fetchall()
            columns = (
                [desc[0] for desc in cursor.description] if cursor.description else []
            )
            return results, columns
        else:
            conn.commit()
            return True

    except (Exception, psycopg2.Error) as error:
        print(f"Error executing '{file_name}': {error}")
        if conn:
            conn.rollback()
        return False

    finally:
        connector.disconnect(conn, cursor)


def execute_sql_by_query(
    query: str, params=None, fetch_results: bool = False
) -> Optional[Tuple[List[Tuple[Any, ...]], List[str]]]:
    conn = None
    cursor = None

    try:
        conn = connector.connect()
        if conn is None:
            raise Exception("Failed to get database connection.")

        cursor = conn.cursor()
        cursor.execute(query, params)

        if fetch_results:
            results = cursor.fetchall()
            columns = (
                [desc[0] for desc in cursor.description] if cursor.description else []
            )
            return results, columns
        else:
            conn.commit()
            return True

    except (Exception, psycopg2.Error) as error:
        print(f"Error executing query: {error}")
        if conn:
            conn.rollback()
        return False

    finally:
        connector.disconnect(conn, cursor)
