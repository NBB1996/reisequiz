import requests
import json
import time

# Basierend auf Wikidata wird die reiseziel.json mit zufälligen Reisezielen angereichert. 
# Bei Bedarf könnten durch ausführung des Codes neue Reiseziele im Quiz erzeugt werden. 

# Konfiguration der Kontinente (Name → Wikidata-ID)
kontinente = {
    "Europa": "Q46",
    "Asien": "Q48",
    "Afrika": "Q15",
    "Nord-/Mittelamerika": "Q49",
    "Südamerika": "Q18",
    "Australien und Ozeanien": "Q538"
}

# Wikidata IDs: Stadt = Q515, Region = Q82794
instanzen = {
    "Stadt": "Q515",
    "Region": "Q82794"
}

HEADERS = {
    "Accept": "application/sparql-results+json",
    "User-Agent": "ReisequizBot/1.0 (mailto:beispiel@e-mail.com)"
}

def get_reiseziele(instance_id, continent_id, kategorie, kontinent_name, limit=50):
    """Lädt Reiseziele aus Wikidata über SPARQL"""
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
        {"name": item["name"]["value"], "kategorie": kategorie, "kontinent": kontinent_name}
        for item in data["results"]["bindings"]
    ]

def main():
    alle_reiseziele = []

    for kontinent, kontinent_id in kontinente.items():
        for kategorie, instanz_id in instanzen.items():
            print(f"Lade {kategorie} in {kontinent} ...")
            try:
                ziele = get_reiseziele(instanz_id, kontinent_id, kategorie, kontinent)
                alle_reiseziele.extend(ziele)
            except requests.exceptions.HTTPError as e:
                print(f"Fehler bei {kategorie} in {kontinent}: {e}")
            time.sleep(2)  # Warten, um das Rate-Limit nicht zu verletzen

    with open("app/data/reiseziel.json", "w", encoding="utf-8") as f:
        json.dump(alle_reiseziele, f, indent=2, ensure_ascii=False)

    print(f"Fertig! {len(alle_reiseziele)} Reiseziele gespeichert.")

if __name__ == "__main__":
    main()