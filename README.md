# runalyze2video

Python-Tool, das die Daten eines bei runalyze.com eingeloggten Benutzers vom dortigen JSON-Endpunk lädt, in eine Datenbank schreibt und die Laufaktivitäten in einem Video verarbeitet (z. B. für die Instagram-Story). Das Video hat ein Balkendiagramm unten, das die ausgewerteten Aktivitäten zeigt, während die einzelnen Läufe und anschließend eine Zusammenfassung oben angezeigt werden.

## Verwendung

Einfach alle benötigten Module installieren, sofern es noch nicht geschehen ist und anschließend fix die Zugangsdaten für Runalyze in einer Datei namens `.env` hinterlegen. Dazu einfach im Programmverzeichnis eine Datei mit diesem Namen anlegen, die die Zugangsdaten zu runalyze.com enthält.

#### Installation der Module:

`pip install requests pandas matplotlib moviepy numpy python-opencv pillow pytz datetime tzlocal dotenv pyrebase sqlite3`

#### Aufbau der .env:

>RUNALYZE_USERNAME=$username<br/>
>RUNALYZE_PASSWORD=$password

Die .env-Datei ist erforderlich, damit sich das Programm bei Runalyze einloggen kann, denn nur in eingeloggtem Zustand wird an JSON-Endpunkt auch ein Datenpaket ausgeliefert. Dann führt man das Programm entweder in VS Code aus, oder man speichert es als Pythonscript und startet es im Terminal bzw. auf der Kommandozeile.

## Ausführung auf Raspi

Ich benutze das Skript mit einem Raspberry Pi. Dort kann das Script dann mittels crontab automatisch laufen und das Video regelmäßig erzeugen.

Hier ein Beispieeintrag für die crontab:

`0 23 L * * /home/user/runalyze2video/python.py`

Der Pfad zum Skript muss natürlich angepasst werden. Und jetzt noch eine kurze Erklärung des Eintrags:

**Minute:** 0 - Die Minute, in der der Befehl ausgeführt wird. In diesem Fall 59 Minuten nach der 23. Stunde.<br/>
**Stunde:** 23 - Die Stunde, in der der Befehl ausgeführt wird. In diesem Fall 23 Uhr.<br/>
**Tag:** L - Der Tag des Monats, an dem der Befehl ausgeführt wird. In diesem Fall L für den letzten Tag des Monats.<br/>
**Monat:** * - Der Monat, in dem der Befehl ausgeführt wird. In diesem Fall * für jeden Monat.<br/>
**Wochentag:** * - Der Wochentag, an dem der Befehl ausgeführt wird. In diesem Fall * für jeden Wochentag.<br/>
**Befehl:** /home/user/runalyze2video/python.py - Der Pfad zum auszuführenden Python-Skript.

## Wishlist

Wenn die Fehlerliste abgearbeitet ist, könnte ich mir noch folgende Funktionen vorstellen:

- Intro und individuelle Clips könnten auch eingefadet oder - noch besser - überblendet werden.
- Es wäre extrem cool, wenn das Diagramm analog zu den einzelnen Datensatzclips aufgebaut würde und nicht sofort vollständig erscheinen würde.
- Eine Übersichtsseite mit den Titeln der verarbeiteten Aktivitäten wäre ebenso cool, hier muss dann zunächst für jede Zeile die Schriftgröße berechnet und dann alles zusammengeklöppelt werden.

## Radfahren?

Ja sicher, warum auch nicht. Der Datendownload enthält alles, was runalyze.com vom jeweiligen Nutzer hat. Es können also auch Radfahrten und/oder andere Sportarten verwurstet werden. Ich habe versucht, alle wesentlichen Dinge in globalen Variablen zu definieren, damit es ohne viel Eingriffe in den Code angepasst werden kann.

## Helfen?

Aber sicher doch, Hilfe wird definitiv benötigt. Also nur zu!
