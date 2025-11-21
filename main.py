from service import executor
from service import utils
from ai import ai_manager
import time

def create():
    if executor.execute_sql_by_file("create.sql"):
        print("Schame created successfully")


def populate():
    if executor.execute_sql_by_file("populate.sql"):
        print("Database populated successfully")


def clear():
    if executor.execute_sql_by_file("drop.sql"):
        print("All data cleaned successfully")


def show():
    result = utils.format_db_tables()
    print(result["table"])


def update():
    result_tuple = executor.execute_sql_by_file("tables.sql", fetch_results=True)
    if not result_tuple:
        print("Error fetching tables.")
        return
    results, _ = result_tuple
    filtered_results = []
    if results:
        for r in results:
            if r[0] not in utils.BLOCKED_TABLES:
                filtered_results.append(r[0])

    table = utils.format_db_tables(filtered_results)
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
    if query_col:
        query_col, _ = query_col
    if not query_col:
        print(f"Column '{col}' not found at table {table_name}\n")
        return

    id = input("Type the information id to locate: ").strip()
    query_id = executor.execute_sql_by_query(
        f"SELECT * FROM {table_name} WHERE {pk_column_name} = %s",
        params=(id,),
        fetch_results=True,
    )
    if query_id:
        query_id, _ = query_id
    if not query_id:
        print(f"Id '{id}' not found at table {table_name}\n")
        return

    new_info = input(f"Type the new info to update into {col} with id {id}: ").strip()

    executor.execute_sql_by_query(
        f"UPDATE {table_name} SET {col} = %s WHERE {pk_column_name} = %s",
        params=(new_info, id),
    )

    print("\nUpdated successfully\n")
    print()

def query():

    while True: 
        print(utils.menu(2))
        opt = input("Type a query option: ")

        if opt == "1":
            result_tuple = executor.execute_sql_by_file(
                "querys/crime_statistics.sql", fetch_results=True
            )
            if result_tuple:
                results, columns = result_tuple
                print(utils.format_query_table(results, columns))
                utils.generate_graph(
                    results,
                    columns,
                    x_col="id_crime",
                    y_col="total_agentes",
                    graph_type="bar",
                    title="Agents by crime"
                )
        elif opt == "2":
            result_tuple = executor.execute_sql_by_file(
                "querys/agents_by_proofs.sql", fetch_results=True
            )
            if result_tuple:
                results, columns = result_tuple
                print(utils.format_query_table(results, columns))
                utils.generate_graph(
                    results,
                    columns,
                    x_col="cargo_agente",
                    y_col="total_provas",
                    graph_type="bar",
                    title="Agents by proofs"
                )
        elif opt == "3":
            result_tuple = executor.execute_sql_by_file(
                "querys/crime_by_avg_age.sql", fetch_results=True
            )
            if result_tuple:
                results, columns = result_tuple
                print(utils.format_query_table(results, columns))
                utils.generate_graph(
                    results,
                    columns,
                    x_col="tipo_crime",
                    y_col="media_idade_envolvidos",
                    graph_type="bar",
                    title="Age average by crime"
                )

        elif opt == "0":
            for i in range(3, 0, -1):
                print(f"Retornando em {i}..")
                time.sleep(0.5)
            break

        else: print("option not found, try again!");print()

def ai():
    with open("sql/create.sql", "r", encoding="utf-8") as file:
        schema = file.read()

    order = input("Type something to consult in our database: ").strip()

    try:
        sql_query = ai_manager.sql_from_LLM(nl=order, schema=schema)

        result_tuple = executor.execute_sql_by_query(sql_query, fetch_results=True)

        if result_tuple:
            results, columns = result_tuple
            print()
            print(utils.format_query_table(results, columns))
            print()

        if result_tuple:
            result, columns = result_tuple
            interpretation = ai_manager.interpretation_from_LLM(
                query_result=result,
                columns=columns,
                schema=schema,
                original_query=sql_query,
            )

            print(interpretation)

    except Exception as e:
        print(f"Error: {e}")


def delete():
    result_tuple = executor.execute_sql_by_file("tables.sql", fetch_results=True)
    if not result_tuple:
        print("Error fetching tables.")
        return
    results, _ = result_tuple
    filtered_results = []
    if results:
        for r in results:
            if r[0] not in utils.BLOCKED_TABLES:
                filtered_results.append(r[0])

    table_info = utils.format_db_tables(filtered_results)
    print()
    print(table_info["table"])
    print()

    table_name = table_info.get("name")
    if not table_name:
        table_name = input("Type the table name to delete from: ").strip().lower()

    if table_name not in filtered_results:
        print("Table not found")
        return

    pk_column = utils.return_pk_column_name(table_name)
    if not pk_column or not pk_column[0]:
        print("Table not found or without a pk\n")
        return
    pk_column = pk_column[0]

    id_to_delete = input(f"Type the {pk_column} value to delete: ").strip()

    id_check = executor.execute_sql_by_query(
        f"SELECT * FROM {table_name} WHERE {pk_column} = %s AND is_deleted = FALSE",
        params=(id_to_delete,),
        fetch_results=True,
    )
    if not id_check or not id_check[0]:
        print(f"Id '{id_to_delete}' not found at table {table_name}\n")
        return

    if table_name in utils.DEPENDENCIES:
        for dep_table, fk_column in utils.DEPENDENCIES[table_name]:
            dep_col_check = executor.execute_sql_by_query(
                "SELECT column_name FROM information_schema.columns WHERE table_name = %s AND column_name = 'is_deleted'",
                params=(dep_table,),
                fetch_results=True,
            )
            if dep_col_check and dep_col_check[0]:
                executor.execute_sql_by_query(
                    f"UPDATE {dep_table} SET is_deleted = TRUE WHERE {fk_column} = %s AND is_deleted = FALSE",
                    params=(id_to_delete,)
                )

    query = f"UPDATE {table_name} SET is_deleted = TRUE WHERE {pk_column} = %s"
    executor.execute_sql_by_query(query, params=(id_to_delete,))
    print("\nDeleted successfully (soft)")

def init():
    try:
        clear()
        create()
        populate()
        print("System init sucessfully")
        print()
        return
    except:
        print("Error to init system :(")
        print()
        return

if __name__ == "__main__":

    while True:

        print(utils.menu(1))
        opt = input("Type a number: ")

        if opt == "1": time.sleep(0.5) ; init()

        if opt == "2": time.sleep(0.5) ; create()

        if opt == "3": time.sleep(0.5) ; populate()

        if opt == "4": time.sleep(0.5) ; show()

        if opt == "5": time.sleep(0.5) ; query()

        if opt == "6": time.sleep(0.5) ; update()

        if opt == "7": time.sleep(0.5) ; delete()

        if opt == "8": time.sleep(0.5) ; ai()

        if opt == "9": time.sleep(0.5) ; clear()

        if opt == "0":
            for i in range(3, 0, -1):
                print(f"Encerrando em {i}..")
                time.sleep(0.5) 
            break

    print("\nThanks to use our system ;)")

