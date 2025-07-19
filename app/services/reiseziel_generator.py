import requests
import json
import time
from typing import List, Dict

# ===============================================
# KONFIGURATION
# ===============================================

# Zuordnung Kontinentname → Wikidata-ID
# Quelle https://www.wikidata.org/wiki/Wikidata%3AList_of_properties/Summary_table
KONTINENTE = {
    "Europa": "Q46",
    "Asien": "Q48",
    "Afrika": "Q15",
    "Nord-/Mittelamerika": "Q49",
    "Südamerika": "Q18",
    "Australien und Ozeanien": "Q538"
}

# Wikidata IDs: Stadt = Q515, Region = Q82794
INSTANZEN = {
    "Stadt": "Q515",
    "Region": "Q82794"
}

HEADERS = {
    "Accept": "application/sparql-results+json",
    "User-Agent": "ReisequizBot/1.0 (mailto:deine@email.de)"
}

OUTPUT_PATH = "app/static/data/reiseziel.json"

# ===============================================
# FUNKTIONEN
# ===============================================

def get_reiseziele(
    instance_id: str,
    continent_id: str,
    kategorie: str,
    kontinent: str,
    limit: int = 50
) -> List[Dict[str, str]]:
    """
    Fragt deutsche Städtenamen oder Regionen via SPARQL bei Wikidata ab.

    Args:
        instance_id: Wikidata-ID für Stadt/Region (z.B. 'Q515').
        continent_id: Wikidata-ID des Kontinents.
        kategorie: Textuelle Bezeichnung (z.B. 'Stadt').
        kontinent_name: Textuelle Bezeichnung (z.B. 'Europa').
        limit: Maximale Anzahl an Ergebnissen.

    Returns:
        Liste von Reisezielen im Format {"name", "kategorie", "kontinent"}.
    """
    sparql = f"""
    SELECT ?name WHERE {{
      ?place wdt:P31 wd:{instance_id};
             wdt:P30 wd:{continent_id};
             rdfs:label ?name.
      FILTER(LANG(?name) = "de")
    }}
    LIMIT {limit}
    """

    url = "https://query.wikidata.org/sparql"
    response = requests.get(url, params={"query": sparql}, headers=HEADERS)
    response.raise_for_status()
    data = response.json()

    return [
        {
            "name": item["name"]["value"],
            "kategorie": kategorie,
            "kontinent": kontinent
        }
        for item in data["results"]["bindings"]
    ]


def main():
    """
    Lädt Städte und Regionen aus allen Kontinenten über Wikidata
    und speichert sie in einer JSON-Datei für das Reisequiz.
    """
    alle_reiseziele: List[Dict[str, str]] = []

    for kontinent, kontinent_id in KONTINENTE.items():
        for kategorie, instanz_id in INSTANZEN.items():
            print(f"Lade {kategorie} in {kontinent} ...")
            try:
                ziele = get_reiseziele(instanz_id, kontinent_id, kategorie, kontinent)
                alle_reiseziele.extend(ziele)
            except requests.exceptions.HTTPError as e:
                print(f"Fehler bei {kategorie} in {kontinent}: {e}")
            time.sleep(2)  # Pausieren, um API-Rate-Limit nicht zu verletzen

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(alle_reiseziele, f, indent=2, ensure_ascii=False)

    print(f"Fertig! {len(alle_reiseziele)} Reiseziele gespeichert unter '{OUTPUT_PATH}'.")


# ===============================================
# SCRIPT ENTRY POINT
# ===============================================

if __name__ == "__main__":
    main()
