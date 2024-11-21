# database.py
import sqlite3

def connect():
    return sqlite3.connect("escalas.db")

def create_tables():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS alunos (id INTEGER PRIMARY KEY, nome TEXT, turma_id INTEGER)")
    cursor.execute("CREATE TABLE IF NOT EXISTS turmas (id INTEGER PRIMARY KEY, nome TEXT)")
    conn.commit()
    conn.close()

# Crie as tabelas ao importar o módulo
create_tables()
