import sqlite3
from flask import g



def connect_to_database():
    sql=sqlite3.connect("members.db")
    sql.row_factory=sqlite3.Row
    return sql

def get_database():
    if not hasattr(g,"members_db"):
        g.members_db= connect_to_database()
    return g.members_db
