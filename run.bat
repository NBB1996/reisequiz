@echo off
echo [INFO] Starte Reisequiz...

REM Virtuelle Umgebung erstellen, falls nicht vorhanden
if not exist venv (
    echo [INFO] Erstelle virtuelle Umgebung...
    python -m venv venv
)

REM Aktivieren der virtuellen Umgebung
call venv\Scripts\activate.bat

REM Abhängigkeiten installieren
echo [INFO] Installiere Python-Abhängigkeiten...
pip install --upgrade pip
pip install -r requirements.txt

REM Anwendung starten
echo [INFO] Starte Anwendung...
python run.py

REM Fenster offen halten
echo.
echo [INFO] Anwendung wurde beendet. Zum Schließen eine Taste drücken...
pause
