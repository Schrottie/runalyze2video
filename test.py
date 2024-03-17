import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

runnersite = 'https://runalyze.com/training/show/ymxmqmh6wm'
response = requests.get(runnersite)
soup = BeautifulSoup(response.text, 'html.parser')

activities = []
today = datetime.today().strftime('%d.%m')

# Finden aller Zeilen mit Laufaktivitäten
activity_rows = soup.find_all('tr', class_='r')

for row in activity_rows:
    cols = row.find_all('td')
    
    # Überprüfen, ob die Zeile eine Aktivität enthält
    if cols:
        # Extrahieren von Datum, Strecke, Dauer und Pace
        date_str = cols[1].text.strip().split()[0].replace('.', '')
        distance_str = cols[5].text.strip().split()[0].replace(',', '.') if len(cols) > 5 else ''
        duration_str = cols[6].text.strip() if len(cols) > 6 else ''
        pace_str = cols[7].text.strip() if len(cols) > 7 else ''
        
        # Überprüfen, ob das Datum heute ist
        if date_str == today:
            if row.find('i', class_='icons8-Running'):
                activities.append({'date': date_str, 'type': 'run', 'distance': distance_str + ' km', 'duration': duration_str, 'pace': pace_str})
            else:
                activities.append({'date': date_str, 'type': 'other', 'distance': '', 'duration': '', 'pace': ''})

df = pd.DataFrame(activities)
print(df)
