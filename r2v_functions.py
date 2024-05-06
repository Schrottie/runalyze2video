import sqlite3
import random
import string
from datetime import datetime

internal_id = None
last_used_id = None

def create_database(db_filename):
    # Erstellt die SQLite-Datenbank und die Tabellen für Protokoll und Warnungen, falls sie nicht existieren.
    with sqlite3.connect(db_filename) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS protocol (
                            timestamp TEXT,
                            internal_id INTEGER,
                            process TEXT
                          )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS warnings (
                            timestamp TEXT,
                            message TEXT,
                            category TEXT,
                            filename TEXT,
                            lineno INTEGER
                          )''')

def log_step(process, internal_id, db_filename):
    # Schreibt die einzelnen Logeinträge in die Protokolltabelle der Datenbank
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with sqlite3.connect(db_filename) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO protocol (timestamp, internal_id, process) VALUES (?, ?, ?)", (timestamp, internal_id, process))