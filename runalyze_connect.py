import os
from dotenv import load_dotenv
import requests
import re

# Function for runalyze-login 
def login_with_username_password():
    
    load_dotenv()
    username = os.getenv('RUNALYZE_USERNAME')
    password = os.getenv('RUNALYZE_PASSWORD')
    
    login_url = 'https://runalyze.com/login'
    session = requests.Session()
    
    # HTML-Inhalt der Login-Seite holen
    response = session.get(login_url)
    html_content = response.text
    
    # CSRF-Token extrahieren
    csrf_token_match = re.search(r'<input[^>]*name=["\']?_csrf_token["\']?[^>]*value=["\']?([^"\'>\s]+)', html_content)

    if csrf_token_match:
        csrf_token = csrf_token_match.group(1)
    else:
        print("CSRF-Token konnte nicht gefunden werden.")
        return None
    
    # Anmelden
    payload = {
        '_username': username,
        '_password': password,
        '_remember_me' : 'off',
        '_csrf_token': csrf_token
    }
    response = session.post(login_url, data=payload)

    # Überprüfen, ob die Anmeldung erfolgreich war
    if response.status_code == 200:
        print("Anmeldung erfolgreich!")
        return session
    else:
        print(f"Anmeldung fehlgeschlagen. Statuscode: {response.status_code}")
        return None

def fetch_activities_csv(session, csv_file):
    csv_url = 'https://runalyze.com/_internal/data/activities/all'
    
    # Die CSV-Datei mit allen Daten abholen
    response = session.get(csv_url)
    
    # Überprüfen, ob der Abruf erfolgreich war
    if response.status_code == 200:
        with open(csv_file, 'wb') as f:
            f.write(response.content)
        print("CSV-Datei erfolgreich heruntergeladen.")
    else:
        print("Fehler beim Abrufen der CSV-Datei.")

# # Beispielaufruf
# session = login_with_username_password()
# if session:
#      fetch_activities_csv(session, csv_file)