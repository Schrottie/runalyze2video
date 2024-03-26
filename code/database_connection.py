import sqlite3

def dataframe_to_sqlite(df, db_file):
    # Verbindung zur SQLite-Datenbank herstellen
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Tabelle erstellen, wenn sie noch nicht existiert
    cursor.execute('''CREATE TABLE IF NOT EXISTS runalyze_activities (
                        ID INTEGER PRIMARY KEY,
                        date TEXT,
                        distance REAL,
                        duration TEXT,
                        duration_minutes TEXT,
                        pace TEXT,
                        r_type TEXT
                    )''')

    # Index erstellen, um sicherzustellen, dass die ID eindeutig ist
    cursor.execute('''CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_id ON runalyze_activities (ID)''')

    # Daten aus dem DataFrame in die Datenbanktabelle einfügen
    for index, row in df.iterrows():
        # ID aus numerischen Zeichen von 'date' und 'distance' generieren
        ID = int(''.join(filter(str.isdigit, row['date'] + str(row['distance']))))

        # Daten in die Tabelle einfügen
        cursor.execute('''INSERT OR IGNORE INTO runalyze_activities (ID, date, distance, duration, duration_minutes, pace, r_type)
                          VALUES (?, ?, ?, ?, ?, ?, ?)''', (ID, row['date'], row['distance'], row['duration'], row['pace'], row['r_type']))

    # Änderungen speichern und Verbindung schließen
    conn.commit()
    conn.close()