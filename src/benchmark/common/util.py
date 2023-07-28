def escape_postgres_sql_str(input:str):
    return input.replace("'", "''")