# 🌍 Reisequiz: Errate das Reiseziel
Du suchst Inspiration für dein nächstes Reiseziel. Wähle deinen präferierten Kontinent aus und errate spanende Reiseziele. 
Im Laufe des Spiels bekommst du ein Bild und Hinweistext zu einer Region oder Stadt angezeigt und musst erraten, um welches Reiseziel es sich handelt.
Wenn du mehr über die Region oder Stadt wissen möchtest kannst du dich auf der Ergebnisseite direkt auf Booking oder Wikipedia zu mehr Details informieren. 

---

## 🚀 Features
- Drei Schwierigkeitsgrade: Sofasurfer, Backpacker, Globetrotter
- Kategorien: Städte oder Regionen weltweit
- Automatisch generierte Hinweise über Wikipedia
- Weiterleitung zum passenden Angebot auf Booking.com

---

## 🖥️ Systemvoraussetzungen
- Windows 10 oder 11  
- Python 3.9 oder neuer (muss im Systempfad verfügbar sein)  
- Internetverbindung (beim ersten Start für Paketinstallation)

---

## ▶️ Schnellstart mit `run.bat` (empfohlen)

### Schritt 1: Repository herunterladen

#### Option A: per Git
```bash
git clone https://github.com/NBB1996/reisequiz.git
cd reisequiz
```

#### Option B: als ZIP
1. Klicke oben rechts auf Code > Download ZIP
2. Entpacke die ZIP-Datei
3. Öffne den Ordner im Windows-Explore

### Schritt 2: Anwendung starten
1. Doppelklicke auf run.bat
2. Ein Konsolenfenster öffnet sich:
    - Es wird automatisch eine virtuelle Umgebung (venv) erstellt (falls noch nicht vorhanden)
    - Notwendige Python-Pakete werden installiert
    - Die App wird gestartet

3. Öffne im Browser:
http://localhost:5000

## Alternative: Manuelle Ausführung über Kommandozeile
Wenn du lieber selbst kontrollieren möchtest, was passiert, folge diesen Schritten:

1. Projekt herunterladen und in das Verzeichnis wechseln (wie oben)
2. Virtuelle Umgebung erstellen
```bash
python -m venv venv 
```
3. Virtuelle Umgebung aktivieren
```bash
venv\Scripts\activate
```
4. Abhängigkeiten installieren
```bash
pip install --upgrade pip
pip install -r requirements.txt
```
5. Anwednung starten
```bash
python app.py
```
6. Im Browser öffnen
http://localhost:5000

## Projektstruktur
reisequiz/
├─ app/
│  ├─ models/                   # Datenmodelle: Kategorien, Level, Reiseziel, etc.
│  ├─ services/                 # API-Zugriff und Link-Generierung
│  ├─ static/                   # CSS, Bilder, JSON-Daten
│  │  ├─ data/reiseziel.json    # Beispieldaten für das Quiz
│  ├─ templates/                # HTML-Vorlagen (Jinja2)
│  ├─ quiz_engine.py            # Spiellogik
│  ├─ routes.py                 # Flask-Routen
│  └─ __init__.py               # App-Initialisierung
├─ tests/                       # Testfälle
├─ run.bat                      # Startskript für Windows
├─ requirements.txt             # Python-Abhängigkeiten
├─ README.md                    # Diese Anleitung
└─ run.py                       # Startpunkt der App, wenn über Python ausgeführt

## Häufige Probleme
| Problem                                | Lösung                                                                   |
| -------------------------------------- | ------------------------------------------------------------------------ |
| `python` nicht gefunden                | Stelle sicher, dass Python in der Systemumgebung (PATH) registriert ist  |
| Leeres Konsolenfenster bei Doppelklick | Öffne `run.bat` per Rechtsklick > Bearbeiten, oder führe es über CMD aus |
| `pip install` schlägt fehl             | Prüfe Internetverbindung und Python-Version                              |
