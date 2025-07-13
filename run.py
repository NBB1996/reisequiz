from app import create_app

# Anwendung über die Factory-Funktion erstellen
app = create_app()

# Lokaler Entwicklungsserver starten, wenn direkt ausgeführt
if __name__ == '__main__':
    # Achtung: debug=True nur in Entwicklung setzen, niemals in Produktion
    app.run(debug=True)