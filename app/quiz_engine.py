import json
import re
import random
import requests
import base64

from io import BytesIO
from PIL import Image
from PIL.Image import Resampling
from app.models.quizfrage import Quizfrage
from app.models.reiseziel import Reiseziel, ReisezielDetails
from app.services.api_service import APIService
from app.models.kategorie import Kategorie
from app.models.kontinent import Kontinent
from app.models.level import Level
from app.services.link_generator import LinkGenerator

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

def verpixle_bild(bild_url, level):
    """
    Verpixelt ein Bild basierend auf der verpixelung-Auflösung im Level-Objekt.
    Args:
        bild_url (str): Bild-URL (z.B. Wikipedia-Thumbnail).
        level (Level): Objekt mit Attribut 'verpixelung' (z.B. 6, 15, 70)
    Returns:
        str: Base64-codiertes Bild als Data-URL (JPEG oder PNG), oder Original-URL bei Fehlern.
    """
    try:
        verpixelung = level.verpixelung
        if not isinstance(verpixelung, int) or verpixelung < 1:
            raise ValueError("Ungültiger Verpixelungswert im Level.")

        headers = APIService.get_standard_headers()
        response = requests.get(bild_url, headers=headers, timeout=5)
        response.raise_for_status()

        img = Image.open(BytesIO(response.content)).convert("RGB")
        original_size = img.size

        # Sicherheits-Check: nicht stärker verpixeln als Bildgröße
        pixel_size = max(1, min(verpixelung, original_size[0], original_size[1]))

        # Verpixeln durch Runter- und Hochskalierung
        klein = img.resize((pixel_size, pixel_size), resample=Resampling.NEAREST)
        verpixelt = klein.resize(original_size, Resampling.NEAREST)

        # Format erkennen und korrekt speichern (PNG vs JPEG)
        format = "PNG" if bild_url.lower().endswith(".png") else "JPEG"
        mime_type = "image/png" if format == "PNG" else "image/jpeg"

        buffer = BytesIO()
        verpixelt.save(buffer, format=format)
        img_base64 = base64.b64encode(buffer.getvalue()).decode()

        return f"data:{mime_type};base64,{img_base64}"

    except Exception as e:
        print(f"[Fehler beim Verpixeln] {e}")
        return bild_url  # Fallback: nicht verpixelt

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
    original_text = APIService.hole_hinweistext(richtige_antwort)
    hinweistext = zensiere_reiseziel_name(original_text, richtige_antwort.name)
    bild_url = verpixle_bild(APIService.hole_bild_url(richtige_antwort), level)

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
    beschreibung = APIService.hole_hinweistext(reiseziel)
    bild_url = APIService.hole_bild_url(reiseziel)
    booking_url = LinkGenerator.booking_deeplink(reiseziel)
    wikipedia_url = LinkGenerator.wikipedia_link_generator(reiseziel)

    return ReisezielDetails(
        name=reiseziel.name,
        beschreibung=beschreibung,
        image_url=bild_url,
        booking_url=booking_url,
        wikipedia_url=wikipedia_url
    )
