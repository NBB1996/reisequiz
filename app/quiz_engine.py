import json
from app.models.quiz import Quiz
from app.models.quizfrage import Quizfrage
from app.models.reiseziel import Reiseziel, ReisezielDetails
from app.services.api_service import APIService
from app.models.kategorie import Kategorie
from app.models.kontinent import Kontinent
from app.models.level import Level
from app.services.booking_link_generator import BookingDeeplinkGenerator
import random

def lade_reiseziele():
    with open("app/static/data/reiseziel.json", encoding="utf-8") as f:
        daten = json.load(f)

    reiseziele = []
    for eintrag in daten:
        rz = Reiseziel(
            name=eintrag["name"],
            kontinent=Kontinent(eintrag["kontinent"]),
            kategorie=Kategorie(eintrag["kategorie"])
        )
        reiseziele.append(rz)

    return reiseziele

def generiere_quizfrage(kategorie, kontinent, level):
    # 1. Reiseziel-Auswahl basierend auf Nutzerpräferenzen
    alle_zielorte = lade_reiseziele() 
    gefiltert = [
        rz for rz in alle_zielorte
        if rz.kategorie.name == kategorie.name and rz.kontinent.name == kontinent.name
    ]

    # 2. Zufällige Antwortoptionen bestimmen
    if len(gefiltert) < level.antwortanzahl:
        raise ValueError("Nicht genug Reisezieloptionen für die Auswahl vorhanden.")

    antwortoptionen = random.sample(gefiltert, level.antwortanzahl)
    richtige_antwort = random.choice(antwortoptionen)

    # 3. Hinweise abrufen (Hinweistext & Bild)
    hinweistext = APIService.holeHinweistext(richtige_antwort)
    bild_url = APIService.holeBildURL(richtige_antwort)

    # 4. Quizfrage erzeugen
    frage = Quizfrage(
        hinweistext=hinweistext,
        bild_url=bild_url,
        antwortoptionen=antwortoptionen,
        richtige_antwort=richtige_antwort
    )

    return frage

def erzeuge_reiseziel_details(reiseziel):
    beschreibung = APIService.holeHinweistext(reiseziel)
    bild_url = APIService.holeBildURL(reiseziel)
    booking_url = BookingDeeplinkGenerator.bereitstellungDeeplink(reiseziel)
    wikipedia_url = APIService.holeWikipediaLink(reiseziel)

    details = ReisezielDetails(
        name=reiseziel.name,               
        beschreibung=beschreibung,
        image_url=bild_url,
        booking_url=booking_url,
        wikipedia_url=wikipedia_url         
    )

    return details
