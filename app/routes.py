from flask import Blueprint, render_template, request, session
from app.quiz_engine import generiere_quizfrage, verarbeite_antwort, erzeuge_reiseziel_details
from app.models.quiz import Quiz
from app.models.kategorie import Kategorie
from app.models.kontinent import Kontinent
from app.models.level import Level

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/settings', methods=['GET', 'POST'])
def settings():
    kategorien = Kategorie.get_all()
    kontinente = Kontinent.get_all()
    level_stufen = Level.get_all()
    return render_template('settings.html', kategorien=kategorien, kontinente=kontinente, level_stufen=level_stufen)

@main.route("/quiz", methods=["POST"])
def quiz():
    # 1. Formulareingaben des Nutzers lesen
    kategorie_name = request.form.get("kategorie")
    kontinent_name = request.form.get("kontinent")
    level_name = request.form.get("level")

    # 2. Umwandeln in Objekte (können None sein)
    kategorie = Kategorie.get_by_name(kategorie_name)
    kontinent = Kontinent.get_by_name(kontinent_name)
    level = Level.get_by_name(level_name)

    # 3. Frühzeitiger Abbruch, wenn etwas ungültig ist
    if not kategorie or not kontinent or not level:
        return "Fehler: Ungültige Quiz-Einstellungen übermittelt.", 400  # oder Weiterleitung mit Fehlermeldung

    # 4. Quizfrage generieren
    frage = generiere_quizfrage(kategorie, kontinent, level)

    # 5. Quizobjekt erzeugen und speichern
    quiz = Quiz(kategorie, kontinent, level)
    quiz.frage = frage

    # 6. Session speichern
    session["quiz_config"] = {
        "kategorie": kategorie.name,
        "kontinent": kontinent.name,
        "level": level.name,
        "richtige_antwort": frage.richtige_antwort.name
    }

    # 7. Template anzeigen
    return render_template("quiz.html", frage=frage)

@main.route("/result", methods=["POST"])
def result():
    # 1. Antwort des Nutzers auslesen
    ausgewaehlt = request.form.get("selected_answer")

    # 2. Quizkonfiguration aus Session lesen
    quiz_config = session.get("quiz_config")
    if not quiz_config:
        return "Fehler: Keine gültige Session vorhanden.", 400

    # 3. Einstellungen rekonstruieren
    kategorie = Kategorie.get_by_name(quiz_config["kategorie"])
    kontinent = Kontinent.get_by_name(quiz_config["kontinent"])
    level = Level.get_by_name(quiz_config["level"])

    # 4. Die gleiche Frage erneut generieren (wie im Quiz)
    frage = generiere_quizfrage(kategorie, kontinent, level)

    # 5. Antwort prüfen
    ausgewaehlte_antwort = request.form.get("selected_answer")
    if not ausgewaehlte_antwort:
        return "Fehler: Es wurde keine Antwort übermittelt.", 400   
    korrekt = verarbeite_antwort(frage, ausgewaehlte_antwort)

    # 6. Reiseziel-Details erzeugen
    reiseziel_details = erzeuge_reiseziel_details(frage.richtige_antwort)

    # 7. Template anzeigen mit allen nötigen Daten
    return render_template(
        "result.html",
        korrekt=korrekt,
        reiseziel_name=frage.richtige_antwort.name,
        reiseziel_beschreibung=reiseziel_details.beschreibung,
        booking_link=reiseziel_details.booking_url,
        wikipedia_link=reiseziel_details.wikipedia_url,
        bild_url=reiseziel_details.image_url
    )
