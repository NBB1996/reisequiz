from flask import Blueprint, render_template, request, session
from app.quiz_engine import generiere_quizfrage
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
    return render_template('settings.html')

@main.route('/quiz_view', methods=['GET', 'POST'])
def quiz_view():
    return render_template('quiz_view.html')

@main.route('/result', methods=['GET', 'POST'])
def result():
    return render_template('result.html')

@main.route("/quiz_view", methods=["POST"])
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