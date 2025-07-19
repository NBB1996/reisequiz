from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from app.quiz_engine import generiere_quizfrage,lade_reiseziele, erzeuge_reiseziel_details
from app.models.quiz import Quiz
from app.models.kategorie import Kategorie
from app.models.kontinent import Kontinent
from app.models.level import Level
from app.models.reiseziel import ReisezielDetails

main = Blueprint('main', __name__)

@main.route('/')
def index():
    # Startseite mit Begrüßung und Quiz-Start-Button
    return render_template('index.html')

@main.route('/settings', methods=['GET', 'POST'])
def settings():
    # Anzeige des Quiz-Einstellungsformulars (Festlegung von Level, Kategorie, Kontinent)
    kategorien = Kategorie.get_all()
    kontinente = Kontinent.get_all()
    level_stufen = Level.get_all()

    # Übergebae der Auswahlmöglichkeiten an das Template 
    return render_template(
        'settings.html', 
        kategorien=kategorien, 
        kontinente=kontinente, 
        level_stufen=level_stufen
        )

@main.route("/quiz", methods=["POST"])
def quiz():
    # 1. Formulareingaben des Nutzers lesen
    kategorie_name = request.form.get("kategorie", "")
    kontinent_name = request.form.get("kontinent", "")
    level_name = request.form.get("level", "")

    # 2. Umwandeln in Objekte
    kategorie = Kategorie.get_by_name(kategorie_name)
    kontinent = Kontinent.get_by_name(kontinent_name)
    level = Level.get_by_name(level_name)

    # 3. Frühzeitiger Abbruch, wenn etwas ungültig ist
    if kategorie is None or kontinent is None or level is None:
        flash("Ungültige Einstellungen. Bitte erneut versuchen.")
        return redirect(url_for("main.settings"))

    # 4. Quizfrage generieren
    frage, details = generiere_quizfrage(kategorie, kontinent, level)

    # 5. Quizobjekt erzeugen und speichern
    quiz = Quiz(kategorie, kontinent, level)
    quiz.frage = frage

    # 6. Session speichern
    session["quiz_config"] = {
        "richtige_antwort": frage.richtige_antwort.name, 
        "details": {
            "beschreibung": details.beschreibung,
            "booking_link": details.booking_url,
            "wikipedia_link": details.wikipedia_url,
            "bild_url": details.image_url
        }
    }

    # 7. Template anzeigen
    return render_template("quiz.html", frage=frage)

@main.route("/result", methods=["POST"])
def result():
    # 1. Antwort des Nutzers auslesen
    ausgewaehlt = request.form.get("selected_answer")

    # 2. Session auslesen
    quiz_config = session.get("quiz_config")
    if not quiz_config:
        flash("Keine aktive Quizrunde gefunden.")
        return redirect(url_for("main.settings"))

    # 3. Daten rekonstruieren
    richtige_antwort_name = quiz_config["richtige_antwort"]
    alle_zielorte = lade_reiseziele()
    richtige_antwort = next((rz for rz in alle_zielorte if rz.name == richtige_antwort_name), None)

    if not richtige_antwort:
        flash("Reiseziel nicht gefunden.")
        return redirect(url_for("main.settings"))

    # 4. Vergleich mit Nutzereingabe 
    korrekt = (ausgewaehlt == richtige_antwort.name)

    # 5. Detailinformationen aus Session laden
    details_data = quiz_config.get("details")
    if not details_data:
        flash("Fehlende Reisedetails in der Session.")
        return redirect(url_for("main.settings"))

    reiseziel_details = ReisezielDetails(
        name=richtige_antwort.name,
        beschreibung=details_data["beschreibung"],
        image_url=details_data["bild_url"],
        booking_url=details_data["booking_link"],
        wikipedia_url=details_data["wikipedia_link"]
    )

    # 6. Ergebnis anzeigen mit Reisedetails und Links für weitere Details, Booking Buchungslink
    return render_template(
        "result.html",
        korrekt=korrekt,
        reiseziel_name=richtige_antwort.name,
        reiseziel_beschreibung=reiseziel_details.beschreibung,
        booking_link=reiseziel_details.booking_url,
        wikipedia_link=reiseziel_details.wikipedia_url,
        bild_url=reiseziel_details.image_url
    )
