import sqlite3
import random
import string
import subprocess
import pandas as pd
from datetime import datetime, timedelta
from dateutil import relativedelta
import pytz

# Globale Variablen (ersetze diese mit deinen Werten)
db_filename = "your_database.db"  # Ersetze dies mit deinem Datenbank-Dateinamen
start_date_string = "2023-01-01"  # Nur relevant für run_mode = 3
end_date_string = "2023-12-31"  # Nur relevant für run_mode = 3
internal_id = 123  # Ersetze mit einer passenden ID

def create_database(db_filename):
    # Erstellt die SQLite-Datenbank und die Tabellen, falls sie nicht existieren.
    conn = None  # Initialisiere conn
    try:
        conn = sqlite3.connect(db_filename)
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
    except sqlite3.Error as e:
        print(f"Fehler beim Erstellen der Datenbank: {e}")
    finally:
        if conn:
            conn.close()

def log_step(process, internal_id, db_filename):
    # Schreibt die einzelnen Logeinträge in die Protokolltabelle der Datenbank
    conn = None  # Initialisiere conn
    try:
        conn = sqlite3.connect(db_filename)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO protocol (timestamp, internal_id, process) VALUES (?, ?, ?)", (timestamp, internal_id, process))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Fehler beim Loggen: {e}")
    finally:
        if conn:
            conn.close()

def clean_protocol(db_filename, weeks_to_keep):
    # Lösche Einträge, die älter als weeks_to_keep sind
    conn = None  # Initialisiere conn
    try:
        conn = sqlite3.connect(db_filename)
        current_time = datetime.now()
        threshold_time = current_time - timedelta(weeks=weeks_to_keep)
        threshold_timestamp = threshold_time.strftime("%Y-%m-%d %H:%M:%S")

        cursor = conn.cursor()
        cursor.execute("DELETE FROM protocol WHERE timestamp < ?", (threshold_timestamp,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Fehler beim Bereinigen des Protokolls: {e}")
    finally:
        if conn:
            conn.close()

def save_reqs(db_filename):
    conn = None  # Initialisiere conn
    try:
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM requirements")
        pip_freeze_output = subprocess.check_output(["pip", "freeze"]).decode("utf-8")
        for line in pip_freeze_output.splitlines():
            if line and "==" in line:
                module, version = line.split("==")
                cursor.execute("INSERT INTO requirements (module, version) VALUES (?, ?)", (module, version))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Fehler beim Speichern der Requirements: {e}")
    except subprocess.CalledProcessError as e:
        print(f"Fehler beim Ausführen von pip freeze: {e}")
    finally:
        if conn:
            conn.close()
            
def install_reqs(db_filename):
    conn = None  # Initialisiere conn
    try:
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='requirements'")
        table_exists = cursor.fetchone() is not None
        if table_exists:
            cursor.execute("SELECT COUNT(*) FROM requirements")
            requirements_count = cursor.fetchone()[0]
            if requirements_count > 0:
                cursor.execute("SELECT module, version FROM requirements")
                requirements = cursor.fetchall()
                for module, version in requirements:
                    subprocess.call(["pip", "install", f"{module}=={version}"])
            else:
                print("Tabelle 'requirements' enthält keine Einträge.")
        else:
            print("Tabelle 'requirements' existiert nicht.")
    except sqlite3.Error as e:
        print(f"Fehler beim Installieren der Requirements: {e}")
    finally:
        if conn:
            conn.close()