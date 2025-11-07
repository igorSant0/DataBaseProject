from service import executor


def create():
    executor.execute_sql("create.sql")


def drop():
    executor.execute_sql("drop.sql")


def populate():
    executor.execute_sql("populate.sql")


drop()
