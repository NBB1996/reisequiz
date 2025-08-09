@echo off
setlocal
title Reisequiz Starter

echo [INFO] Suche Python...

REM ---------------------------------------------------------------------------
REM Python-Finder: versucht PATH, py-Launcher, typische Installationspfade
REM ---------------------------------------------------------------------------
set "PYEXE="

REM 1) python im PATH?
where python >nul 2>nul
if %ERRORLEVEL%==0 (
  for /f "delims=" %%I in ('where python') do (
    set "PYEXE=%%I"
    goto FOUND_PY
  )
)

REM 2) Windows Python Launcher?
where py >nul 2>nul
if %ERRORLEVEL%==0 (
  set "PYEXE=py"
  goto FOUND_PY
)

REM 3) Übliche Benutzer-Installation (313 anpassen falls nötig)
if exist "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" (
  set "PYEXE=%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
  goto FOUND_PY
)

REM 4) Andere Python3*-Ordner unter Local\Programs\Python durchsuchen
for /f "delims=" %%D in ('dir /b /ad "%LOCALAPPDATA%\Programs\Python\Python3*" 2^>nul') do (
  if exist "%LOCALAPPDATA%\Programs\Python\%%D\python.exe" (
    set "PYEXE=%LOCALAPPDATA%\Programs\Python\%%D\python.exe"
    goto FOUND_PY
  )
)

REM 5) Systemweite Installation (Program Files)
for /f "delims=" %%P in ('dir /b /ad "C:\Program Files\Python3*" 2^>nul') do (
  if exist "C:\Program Files\%%P\python.exe" (
    set "PYEXE=C:\Program Files\%%P\python.exe"
    goto FOUND_PY
  )
)

echo [ERROR] Keine Python-Installation gefunden.
echo [HINWEIS] Bitte Python installieren oder App-Ausfuehrungsaliase pruefen.
echo [HINWEIS] Windows Einstellungen > Apps > App-Ausfuehrungsaliase
pause
exit /b 1

:FOUND_PY
echo [INFO] Verwende Python: %PYEXE%

echo [INFO] Starte Reisequiz Setup...

REM ---------------------------------------------------------------------------
REM Virtuelle Umgebung erstellen (falls nicht vorhanden)
REM ---------------------------------------------------------------------------
if not exist venv (
  echo [INFO] Erstelle virtuelle Umgebung...
  "%PYEXE%" -m venv venv
  if errorlevel 1 (
    echo [ERROR] Konnte virtuelle Umgebung nicht erstellen.
    pause
    exit /b 1
  )
) else (
  echo [INFO] Virtuelle Umgebung bereits vorhanden.
)

REM ---------------------------------------------------------------------------
REM Aktivieren der virtuellen Umgebung
REM ---------------------------------------------------------------------------
call venv\Scripts\activate.bat
if errorlevel 1 (
  echo [ERROR] Konnte venv nicht aktivieren.
  pause
  exit /b 1
)

REM Optional: Pip-Quiet
set PIP_DISABLE_PIP_VERSION_CHECK=1

REM ---------------------------------------------------------------------------
REM Build-Tools aktualisieren
REM ---------------------------------------------------------------------------
echo [INFO] Aktualisiere pip / setuptools / wheel...
python -m pip install --upgrade pip setuptools wheel
if errorlevel 1 (
  echo [WARN] Konnte Build-Tools nicht aktualisieren. Fahre fort...
)

REM ---------------------------------------------------------------------------
REM Abhaengigkeiten installieren
REM ---------------------------------------------------------------------------
if exist requirements.txt (
  echo [INFO] Installiere Abhaengigkeiten aus requirements.txt...
  pip install -r requirements.txt
  if errorlevel 1 (
    echo [WARN] Installation aus requirements.txt fehlgeschlagen.
    echo [INFO] Versuche Kernpakete zu installieren: flask pillow requests bleach
    pip install flask pillow requests bleach
    if errorlevel 1 (
      echo [ERROR] Konnte Kernpakete nicht installieren.
      echo [TIPP] Internet/Proxy/Firewall pruefen oder 'pip install -v' ausfuehren.
      pause
      exit /b 1
    )
  )
) else (
  echo [WARN] Keine requirements.txt gefunden. Installiere Kernpakete.
  pip install flask pillow requests bleach
  if errorlevel 1 (
    echo [ERROR] Konnte Kernpakete nicht installieren.
    pause
    exit /b 1
  )
)

REM ---------------------------------------------------------------------------
REM Verifikation: Sind Hauptpakete importierbar?
REM ---------------------------------------------------------------------------
python -c "import flask, PIL, requests, bleach; print('[INFO] Paket-Check OK.')"
if errorlevel 1 (
  echo [ERROR] Pakete nicht korrekt installiert. Abbruch.
  pause
  exit /b 1
)

REM ---------------------------------------------------------------------------
REM Hauptdatei feststellen
REM ---------------------------------------------------------------------------
set "MAIN="
if exist run.py set "MAIN=run.py"
if not defined MAIN if exist app.py set "MAIN=app.py"

if not defined MAIN (
  echo [ERROR] Weder run.py noch app.py gefunden.
  echo [HINWEIS] Bitte Dateinamen pruefen oder in run.bat anpassen.
  pause
  exit /b 1
)

REM ---------------------------------------------------------------------------
REM Anwendung starten
REM ---------------------------------------------------------------------------
echo [INFO] Starte Anwendung...
echo [INFO] Oeffne im Browser: http://127.0.0.1:5000/
python "%MAIN%"
set "EXITCODE=%ERRORLEVEL%"

echo.
echo [INFO] Anwendung beendet (Exitcode %EXITCODE%). Zum Schliessen Taste druecken...
pause
endlocal & exit /b %EXITCODE%
