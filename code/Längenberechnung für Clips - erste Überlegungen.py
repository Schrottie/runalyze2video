# maximale Länge der einzelnen Clips berechnen und Variablen ggf. anpassen

# Ermitteln der Anzahl der Zeilen im DataFrame
num_rows = len(df)

# Gesamtdauer aller festen Clips berechnen (intro, outro, totals)
total_clip_duration = intro_clip_duration + final_duration + outro_clip_duration

# Anpassen der Dauer pro Zeile, um die Gesamtdauer auf 60 Sekunden zu begrenzen
duration_per_row_adjusted = min((60 - total_clip_duration) / (num_rows + 2), duration_per_row)

# Anpassen der Dauer der anderen Clips, falls erforderlich, um sicherzustellen, dass die Gesamtdauer 60 Sekunden nicht überschreitet
if duration_per_row_adjusted < duration_per_row:
    fade_duration_adjusted = max(fade_duration + (duration_per_row - duration_per_row_adjusted), 1)
    final_duration_adjusted = max(final_duration - (fade_duration - fade_duration_adjusted), 3)
    outro_clip_duration_adjusted = max(outro_clip_duration - (fade_duration - fade_duration_adjusted), 2)

# Verbleibende Dauer nach Anpassung berechnen
remaining_duration = 60 - ((num_rows + 2) * duration_per_row_adjusted + total_clip_duration_adjusted)

# Überprüfen, ob die verbleibende Dauer ausreicht, um die Gesamtdauer auf 60 Sekunden zu bringen
if remaining_duration > 0:
    intro_clip_duration_adjusted += remaining_duration / 3
    outro_clip_duration_adjusted += remaining_duration / 3
    fade_duration_adjusted += remaining_duration / 3

# Verbleibende Dauer nach Anpassung berechnen
total_clip_duration_adjusted = intro_clip_duration_adjusted + fade_duration_adjusted + final_duration_adjusted + outro_clip_duration_adjusted

# Überprüfen, ob die Gesamtdauer 60 Sekunden überschreitet und gegebenenfalls eine Warnung ausgeben
if total_clip_duration_adjusted > 60:
    print("Warnung: Die Gesamtdauer des Videos überschreitet 60 Sekunden.")

# Verwende die angepassten Dauern
duration_per_row = duration_per_row_adjusted
intro_clip_duration = intro_clip_duration_adjusted
fade_duration = fade_duration_adjusted
final_duration = final_duration_adjusted
outro_clip_duration = outro_clip_duration_adjusted

print("duration_per_row: " + duration_per_row)
print("intro_clip_duration: " + intro_clip_duration)
print("fade_duration: " + fade_duration)
print("final_duration: " + final_duration)
print("outro_clip_duration: " + outro_clip_duration)