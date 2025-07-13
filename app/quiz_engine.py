import json
import re
import random

from app.models.quiz import Quiz
from app.models.quizfrage import Quizfrage
from app.models.reiseziel import Reiseziel, ReisezielDetails
from app.services.api_service import APIService
from app.models.kategorie import Kategorie
from app.models.kontinent import Kontinent
from app.models.level import Level
from app.services.booking_link_generator import BookingDeeplinkGenerator


def lade_reiseziele(pfad="app/static/data/reiseziel.json"):
    """
    Lädt alle verfügbaren Reiseziele aus der in data hinterlegten reiseziel.json Datei.

    Args: 
        pfad zur reiseziel Datei 

    Rückgabe:
        Liste von Reiseziel-Objekten.
    """
    with open(pfad, encoding="utf-8") as f:
        daten = json.load(f)

    return [
        Reiseziel(
            name=eintrag["name"],
            kontinent=Kontinent(eintrag["kontinent"]),
            kategorie=Kategorie(eintrag["kategorie"])
        ) for eintrag in daten
    ]

def zensiere_reiseziel_name(text, reiseziel_name):
    """
    Zensiert den Namen des Reiseziels im Hinweistext durch "__", um Spoiler zu vermeiden.
    Groß-/Kleinschreibung wird ignoriert.

    Args:
        text (str): Ursprünglicher Text
        reiseziel_name (str): Zu zensierender Name

    Returns:
        str: Zensierter Text
    """
    muster = re.compile(re.escape(reiseziel_name), re.IGNORECASE)
    return muster.sub("__", text)

def generiere_quizfrage(kategorie, kontinent, level):
    """
    Erstellt eine neue Quizfrage anhand der gewählten Einstellungen.

    Args:
        kategorie (Kategorie): Vom Nutzer gewählte Kategorie
        kontinent (Kontinent): Vom Nutzer gewählter Kontinent
        level (Level): Schwierigkeitsstufe mit Anzahl der Antwortoptionen

    Returns:
        Quizfrage: Objekt mit Hinweistext, Bild und Antwortoptionen
    """
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
    original_text = APIService.holeHinweistext(richtige_antwort)
    hinweistext = zensiere_reiseziel_name(original_text, richtige_antwort.name)
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
    """
    Erzeugt Detailinformationen zu einem Reiseziel über API-Zugriffe.

    Args:
        reiseziel (Reiseziel): Zielort, für den Details generiert werden sollen

    Returns:
        ReisezielDetails: Objekt mit Bild, Beschreibung, Buchungs- und Wikipedia-Link
    """
    beschreibung = APIService.holeHinweistext(reiseziel)
    bild_url = APIService.holeBildURL(reiseziel)
    booking_url = BookingDeeplinkGenerator.bereitstellungDeeplink(reiseziel)
    wikipedia_url = APIService.holeWikipediaLink(reiseziel)

    return ReisezielDetails(
        name=reiseziel.name,
        beschreibung=beschreibung,
        image_url=bild_url,
        booking_url=booking_url,
        wikipedia_url=wikipedia_url
    )
