import sqlite3
from flask import g
from os import path

ROOT = path.dirname(path.realpath(__file__))

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(path.join(ROOT, "minesweeper.db"))
        g.db.row_factory = sqlite3.Row
        if not g.db.execute("SELECT sql FROM sqlite_master WHERE type = \'table\' AND name = \'users\'").fetchone():
            table_sql = open("static/schema.sql").read()
            g.db.execute(table_sql)
    return g.db

def close_db():
    db = g.pop("db", None)
    if db is not None:
       db.close()
