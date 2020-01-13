import sqlite3
from sqlite3 import Error
from flask import current_app, g

def connect(db_file=None):
    conn = None
    try:
        conn = sqlite3.connect(db_file or "minesweeper.db")
        print(sqlite3.version)
    except Error as e:
        print(e)
    return conn

def execute(conn, sql):
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)

def exit(conn):
    try:
        conn.close()
    except Error as e:
        print(e)

def get_db():
    if "db" not in g:
        g.db = connect()
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db():
    db = g.pop("db", None)

    if db is not None:
        exit(db)

def main():
    table_sql = open("static/schema.sql").read()
    execute(connect("minesweeper.db"), table_sql)


if __name__ == '__main__':
    main()
