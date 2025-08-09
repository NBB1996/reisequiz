@echo off
setlocal
title Reisequiz Starter

echo [INFO] Suche Python...

REM --- Python-Finder ---------------------------------------------------------
set "PYEXE="

REM 1) Falls python im PATH ist
where python >nul 2>nul && for /f "delims=" %%I in ('where python') do (
  set "PYEXE=%%I"
  goto :FOUND_PY
)

REM 2) Windows-Python-Launcher (py)
where py >nul 2>nul && (
  set "PYEXE=py"
  goto :FOUND_PY
)

REM 3) Übliche Benutzer-Installation
if exist "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" (
  set "PYEXE=%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
  goto :FOUND_PY
)

REM 4) Andere Python3*-Ordner unter Local\Programs\Python durchsuchen
for /f "delims=" %%D in ('dir /b /ad "%LOCALAPPDATA%\Programs\Python\Python3*" 2^>nul') do (
  if exist "%LOCALAPPDATA%\Programs\Python\%%D\python.exe" (
    set "PYEXE=%LOCALAPPDATA%\Programs\Python\%%D\python.exe"
    goto :FOUND_PY
  )
)

REM 5) Systemweite Installation
for /f "delims=" %%P in ('dir /b /ad "C:\Program Files\Python3*" 2^>nul') do (
  if exist "C:\Program Files\%%P\python.exe" (
    set "PYEXE=C:\Program Files\%%P\python.exe"
    goto :FOUND_PY
  )
)

echo [ERROR] Keine Python-Installation gefunden.
echo         Bitte Python installieren ODER App-Execution-Aliasse pruefen
echo         (Windows Einstellungen > Apps > App-Ausfuehrungsaliase).
echo         Alternativ PATH setzen oder Python-Pfad hier fest eintragen.
pause
exit /b 1

:FOUND_PY
echo [INFO] Verwende: %PYEXE%

echo [INFO] Starte Reisequiz...

REM Virtuelle Umgebung erstellen, falls nicht vorhanden
if not exist venv (
  echo [INFO] Erstelle virtuelle Umgebung...
  "%PYEXE%" -m venv venv
  if errorlevel 1 (
    echo [ERROR] Konnte virtuelle Umgebung nicht erstellen.
    pause
    exit /b 1
  )
)

REM Aktivieren der virtuellen Umgebung
call venv\Scripts\activate.bat

REM Abhängigkeiten installieren (requirements optional)
echo [INFO] Installiere Python-Abhaengigkeiten...
python -m pip install --upgrade pip
if exist requirements.txt (
  python -m pip install -r requirements.txt
) else (
  echo [WARN] Keine requirements.txt gefunden. Ueberspringe Installation.
)

REM Hauptdatei finden (run.py bevorzugt, sonst app.py)
set "MAIN="
if exist run.py set "MAIN=run.py"
if not defined MAIN if exist app.py set "MAIN=app.py"

if not defined MAIN (
  echo [ERROR] Weder run.py noch app.py gefunden.
  echo         Bitte Dateinamen pruefen oder in der BAT anpassen.
  pause
  exit /b 1
)

REM Anwendung starten
echo [INFO] Starte Anwendung...
python "%MAIN%"
set "EXITCODE=%ERRORLEVEL%"

echo.
echo [INFO] Anwendung beendet (Exitcode %EXITCODE%). Zum Schliessen Taste druecken...
pause
endlocal & exit /b %EXITCODE%

