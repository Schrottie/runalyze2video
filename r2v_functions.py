import sqlite3
import random
import string
from datetime import datetime, timedelta

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

def clean_protocol(db_filename, weeks_to_keep):
    # Berechne die Grenze des Zeitstempels für Einträge, die behalten werden sollen
    current_time = datetime.now()
    threshold_time = current_time - timedelta(weeks=weeks_to_keep)
    threshold_timestamp = threshold_time.strftime("%Y-%m-%d %H:%M:%S")

    # Lösche Einträge, die älter als die Grenze sind
    with sqlite3.connect(db_filename) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM protocol WHERE timestamp < ?", (threshold_timestamp,))
        conn.commit()

