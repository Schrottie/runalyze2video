import pandas as pd
"""
Erstellen eines Test-Dataframes anhand realer und damit 
bekannter Daten. Ziel ist es, eine Pace von 5:53 min/km
zu erhalten.
"""

df = pd.DataFrame({
    "distance": [30.9],
    "s": [10909]
})

# Wie viele Sekunden wurden für einen Kilometer benötigt?
df["pace"] = df["s"] / df["distance"]

# Jetzt aus den Sekunden Minuten machen
df["pace"] = df["pace"] / 60

# Und jetzt noch den dezimalen Wert in eine Zeit umklöppeln
df["pace"] = df["pace"].apply(lambda x: f"{int(x // 1):02d}:{int(x % 1 * 60):02d}")

# Ausgabe des Dataframes
print(df)


# sekunden = 10909
# zeit = lambda x: f"{x // 3600:02d}:{x % 3600 // 60:02d}:{x % 60:02d}"
# print(zeit(sekunden))