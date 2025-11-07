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

    utils.format_tables()
    print(utils.format_tables())


def update():
    results = executor.execute_sql_by_file("tables.sql", fetch_results=True)
    filtered_results = []
    if results:
        for r in results:
            if r[0] not in BLOCKED_TABLES:
                filtered_results.append(r[0])
    table = utils.format_tables(filtered_results)
    print(table["table"])

    # Obter nomes das colunas
    colnames_result = executor.execute_sql_by_query(
        f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table["name"]}' ORDER BY ordinal_position",
        fetch_results=True,
    )
    if not colnames_result:
        print("Could not retrieve column names.")
        return
    colnames = [col[0] for col in colnames_result]

    pk_column = colnames[0]
    pk_value = input(
        f"\nType the {pk_column} of the record you want to update: "
    ).strip()

    # Verificar se o registro existe
    check_record = executor.execute_sql_by_query(
        f"SELECT * FROM {table_name} WHERE {pk_column} = %s",
        params=(pk_value,),
        fetch_results=True,
    )
    if not check_record:
        print(f"❌ No record found with {pk_column} = {pk_value}")
        return

    # Mostrar campos disponíveis para UPDATE (exceto a chave primária)
    updatable_fields = [col for col in colnames if col != pk_column]
    print(f"\n--- AVAILABLE FIELDS TO UPDATE ---")
    for idx, field in enumerate(updatable_fields, start=1):
        print(f"{idx}. {field}")

    # Solicitar campo a atualizar
    field_to_update = (
        input("\nType the field name you want to update: ").strip().lower()
    )
    if field_to_update not in updatable_fields:
        print("❌ Field not available for UPDATE.")
        return

    # Solicitar novo valor
    new_value = input(f"Type the new value for {field_to_update}: ").strip()

    # Executar UPDATE
    query = f"UPDATE {table_name} SET {field_to_update} = %s WHERE {pk_column} = %s"
    executor.execute_sql_by_query(query, params=(new_value, pk_value))

    print("✅ Record updated successfully!")

    # Mostrar o registro atualizado
    print("\n--- UPDATED RECORD ---")
    print(utils.format_tables(table_name))


update()


"""

4. Query  - Test; -> mostra um submenu das consultas (min 3) existentes

5. Update - Test; ->  update na tabela, primeiro mostrando seus atributos e valores, depois permitindo
que seja selecionado um atributo e um valor dele para modificar

6. Delete - Test; -> realizar deletes de valores especificos

7. IA     - Test;

0. Disconnect.
"""
