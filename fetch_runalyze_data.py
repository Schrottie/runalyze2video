import os
import re
import sys
import requests
from dotenv import load_dotenv
import mysql.connector
import csv


csv_file = "runalyze_activities.csv"
csv_file_fixed = "runalyze_activities_fixed.csv"


def fix_broken_csv(input_file, output_file):
    """
    Repariert CSV-Zeilen, die durch Zeilenumbrüche innerhalb von Feldern beschädigt wurden.
    Jede gültige Zeile beginnt mit einer 8-stelligen ID.
    """
    fixed_lines = []
    current_line = ""

    pattern = re.compile(r"^\d{8},")  # gültige Zeile beginnt mit 8 Ziffern + Komma

    with open(input_file, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.rstrip("\n")

            if pattern.match(line):
                # Neue gültige Zeile beginnt
                if current_line:
                    fixed_lines.append(current_line)
                current_line = line
            else:
                # Zeile gehört zur vorherigen
                current_line += line

        # letzte Zeile anhängen
        if current_line:
            fixed_lines.append(current_line)

    # reparierte Datei speichern
    with open(output_file, "w", encoding="utf-8") as f:
        for line in fixed_lines:
            f.write(line + "\n")

    print(f"Reparierte CSV gespeichert als: {output_file}")


def login_with_username_password():
    load_dotenv()
    username = os.getenv('RUNALYZE_USERNAME')
    password = os.getenv('RUNALYZE_PASSWORD')

    if not username or not password:
        print("Fehler: RUNALYZE_USERNAME oder RUNALYZE_PASSWORD fehlen in der .env-Datei.")
        return None

    login_url = 'https://runalyze.com/login'
    session = requests.Session()

    response = session.get(login_url)
    html_content = response.text

    csrf_token_match = re.search(
        r'<input[^>]*name=["\']?_csrf_token["\']?[^>]*value=["\']?([^"\'>\s]+)',
        html_content
    )

    if csrf_token_match:
        csrf_token = csrf_token_match.group(1)
    else:
        print("CSRF-Token konnte nicht gefunden werden.")
        return None

    payload = {
        '_username': username,
        '_password': password,
        '_remember_me': 'off',
        '_csrf_token': csrf_token
    }

    response = session.post(login_url, data=payload, allow_redirects=True)

    if response.url != login_url:
        print("Anmeldung erfolgreich!")
        return session
    else:
        print("Anmeldung fehlgeschlagen - bitte Zugangsdaten prüfen.")
        return None


def fetch_activity_data_csv(session):
    csv_url = 'https://runalyze.com/_internal/data/activities/all'

    response = session.get(csv_url)

    if response.status_code == 200:
        with open(csv_file, 'wb') as f:
            f.write(response.content)
        print(f"CSV-Datei erfolgreich heruntergeladen: {csv_file}")
    else:
        print(f"Fehler beim Abrufen der CSV-Datei. Statuscode: {response.status_code}")

def import_csv_to_mysql(csv_file):

    load_dotenv()
    db_username = os.getenv('DATABASE_USERNAME')
    db_password = os.getenv('DATABASE_PASSWORD')

    # Verbindung zur MySQL-Datenbank
    conn = mysql.connector.connect(
        host="localhost",
        user=db_username,
        password=db_password,
        database="runalyze",
        charset="utf8mb4"
    )
    cursor = conn.cursor()

    print("Lese CSV und importiere neue Datensätze...")

    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)

        for row in reader:
            if not row:
                continue

            activity_id = row[0]

            # Prüfen, ob ID bereits existiert
            cursor.execute("SELECT id FROM activities WHERE id = %s", (activity_id,))
            exists = cursor.fetchone()

            if exists:
                continue  # überspringen

            # Dynamisches Insert basierend auf Spaltenanzahl
            placeholders = ", ".join(["%s"] * len(row))
            sql = f"INSERT INTO activities VALUES ({placeholders})"

            cursor.execute(sql, row)

    conn.commit()
    cursor.close()
    conn.close()

    print("Import abgeschlossen.")

def main():
    print("Starte Login…")
    session = login_with_username_password()

    if session is None:
        print("Login fehlgeschlagen - Script wird beendet.")
        sys.exit(1)

    print("Lade CSV herunter…")
    fetch_activity_data_csv(session)

    print("Repariere CSV…")
    fix_broken_csv(csv_file, csv_file_fixed)

    print("Importiere CSV in MySQL…")
    import_csv_to_mysql(csv_file_fixed)


    print("Fertig.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Fehler aufgetreten: {str(e)} - Abbruch!")
        sys.exit(1)
