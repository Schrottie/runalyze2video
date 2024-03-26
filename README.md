# runalyze2video

Python-Tool, das die Daten von der öffentlichen Athletenseite auf runalyze.com liest und die Laufaktivitäten in einem Video verarbeitet (z. B. für die Instagram-Story). Das Video hat ein Balkendiagramm unten, das die ausgewerteten Aktivitäten zeigt, während die einzelnen Läufe und dann eine Zusammenfassung oben angezeigt werden.

## Ausführung auf Raspi

Ich benutze das Skript mit einem Raspberry Pi. Es wird immer am Ende des Monats gestartet. Es ist wichtig, dies vor Monatsende zu tun, da der nächste Monat bereits am nächsten Tag (am ersten des Monats) auf der öffentlichen Athletenseite erscheint.

Für dies wird der folgende Eintrag in der Crontab empfohlen:

`0 23 L * * /home/user/runalyze2video/python.py`

Der Pfad zum Skript muss natürlich angepasst werden. Eine kurze Erklärung des Eintrags:

**Minute:** 0 - Die Minute, in der der Befehl ausgeführt wird. In diesem Fall 59 Minuten nach der 23. Stunde.
**Stunde:** 23 - Die Stunde, in der der Befehl ausgeführt wird. In diesem Fall 23 Uhr.
**Tag:** L - Der Tag des Monats, an dem der Befehl ausgeführt wird. In diesem Fall L für den letzten Tag des Monats.
**Monat:** * - Der Monat, in dem der Befehl ausgeführt wird. In diesem Fall * für jeden Monat.
**Wochentag:** * - Der Wochentag, an dem der Befehl ausgeführt wird. In diesem Fall * für jeden Wochentag.
**Befehl:** /home/user/runalyze2video/python.py - Der Pfad zum auszuführenden Python-Skript.

## Wishlist

> Intro und individuelle Clips könnten auch eingefadet oder - noch besser - überblendet werden.
> Eine Übersichtsseite mit allen verarbeiteten Aktivitäten, wobei dazu vorher die Größe jedes Textes berechnet werden muss.
> Es wäre extrem cool, wenn das Diagramm analog zu den einzelnen Datensatzclips aufgebaut würde und nicht sofort vollständig erscheinen würde.
> Eine etwas modernere Optik wäre auch ziemlich cool.

## Radfahren?

Auch das ist möglich. Im Grunde kann jede Sportart eingeschlossen/verarbeitet werden.
