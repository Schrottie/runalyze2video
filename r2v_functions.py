import sqlite3
import random
import string
import subprocess
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
        cursor.execute('''CREATE TABLE IF NOT EXISTS requirements (
                            module TEXT,
                            version TEXT
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

def save_reqs(db_filename):
    # Stelle eine Verbindung zur Datenbank her
    with sqlite3.connect(db_filename) as conn:
        cursor = conn.cursor()

        # Leere die Tabelle "requirements" vor dem Speichern
        cursor.execute("DELETE FROM requirements")

        # Hole die Ausgabe von `pip freeze`
        pip_freeze_output = subprocess.check_output(["pip", "freeze"]).decode("utf-8")

        # Speichere jedes Paket in der Datenbank
        for line in pip_freeze_output.splitlines():
            if line:
                module, version = line.split("==")
                cursor.execute("INSERT INTO requirements (module, version) VALUES (?, ?)", (module, version))

        # Speichere die Änderungen
        conn.commit()

def install_reqs(db_filename):
    # Stelle eine Verbindung zur Datenbank her
    with sqlite3.connect(db_filename) as conn:
        cursor = conn.cursor()

        # Prüfe, ob die Tabelle "requirements" existiert
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='requirements'")
        table_exists = cursor.fetchone() is not None

        if table_exists:
            # Prüfe, ob die Tabelle "requirements" Einträge enthält
            cursor.execute("SELECT COUNT(*) FROM requirements")
            requirements_count = cursor.fetchone()[0]

            if requirements_count > 0:
                # Hole alle Module aus der Tabelle "requirements"
                cursor.execute("SELECT module, version FROM requirements")
                requirements = cursor.fetchall()

                # Installiere jedes Modul mit pip
                for module, version in requirements:
                    subprocess.call(["pip", "install", f"{module}=={version}"])
            else:
                print("Tabelle 'requirements' enthält keine Einträge.")
        else:
            print("Tabelle 'requirements' existiert nicht.")


