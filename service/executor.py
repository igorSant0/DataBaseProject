from . import connector
import os
import psycopg2

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SQL_DIR = os.path.join(BASE_DIR, "sql")


def execute_sql_by_file(file_name, params=None, fetch_results=False):
    conn = None
    cursor = None
    file_path = os.path.join(SQL_DIR, file_name)
    print("-----", file_path)

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

        results = None

        if fetch_results:
            results = cursor.fetchall()
        else:
            conn.commit()
            print(f"Success: Commands from file '{file_name}' were executed.")

        return results

    except (Exception, psycopg2.Error) as error:
        print(f"Error executing '{file_name}': {error}")
        if conn:
            conn.rollback()
        return None

    finally:
        connector.disconnect(conn, cursor)


def execute_sql_by_query(query, params=None, fetch_results=False):
    conn = None
    cursor = None

    try:
        conn = connector.connect()
        if conn is None:
            raise Exception("Failed to get database connection.")

        cursor = conn.cursor()
        cursor.execute(query, params)

        results = None

        if fetch_results:
            results = cursor.fetchall()
        else:
            conn.commit()

        return results

    except (Exception, psycopg2.Error) as error:
        print(f"Error executing query: {error}")
        if conn:
            conn.rollback()
        return None

    finally:
        connector.disconnect(conn, cursor)
