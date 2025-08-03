import requests
import json
import time
from typing import List, Dict

# ===============================================
# KONFIGURATION
# ===============================================

KONTINENTE = {
    "Europa": "Q46",
    "Asien": "Q48",
    "Afrika": "Q15",
    "Nord-/Mittelamerika": "Q49",
    "Südamerika": "Q18",
    "Australien und Ozeanien": "Q538"
}

INSTANZEN = {
    "Stadt": "Q515",
    "Region": "Q82794"
}

MINIMALE_ANZAHL = {
    "Stadt": 20,
    "Region": 10
}

OZEANIEN_LAENDER = [
    "Q712", "Q678", "Q683", "Q691", "Q686", "Q685", "Q710", "Q672", "Q697"
]
AUSTRALIEN_ID = "Q408"
OZEANIEN_LABEL = "Australien und Ozeanien"

HEADERS = {
    "Accept": "application/sparql-results+json",
    "User-Agent": "ReisequizBot/1.0 (kontakt@mein-reisequiz.de)"
}

OUTPUT_PATH = "app/static/data/reiseziel.json"

# ===============================================
# FUNKTIONEN
# ===============================================

def has_valid_wikipedia_extract(title: str) -> bool:
    url = "https://de.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "titles": title,
        "exintro": True,
        "explaintext": True
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        pages = response.json().get("query", {}).get("pages", {})
        for page in pages.values():
            extract = page.get("extract", "")
            if len(extract.strip()) >= 100:
                return True
    except Exception:
        return False
    return False


def run_query_and_filter(sparql: str, kategorie: str, kontinent: str) -> List[Dict[str, str]]:
    url = "https://query.wikidata.org/sparql"
    response = requests.get(url, params={"query": sparql}, headers=HEADERS)
    response.raise_for_status()
    data = response.json()

    reiseziele = []
    for item in data["results"]["bindings"]:
        name = item["name"]["value"]
        article = item.get("article", {}).get("value")
        if article and has_valid_wikipedia_extract(name):
            reiseziele.append({
                "name": name,
                "kategorie": kategorie,
                "kontinent": kontinent
            })
        time.sleep(1)
    return reiseziele


def query_p30(instance_id: str, continent_id: str, kategorie: str, kontinent: str, limit=200):
    sparql = f"""
    SELECT ?name ?article WHERE {{
      ?place wdt:P31 wd:{instance_id};
             wdt:P30 wd:{continent_id};
             rdfs:label ?name.
      FILTER(LANG(?name) = "de")
      ?article schema:about ?place;
               schema:isPartOf <https://de.wikipedia.org/>.
    }}
    LIMIT {limit}
    """
    return run_query_and_filter(sparql, kategorie, kontinent)


def query_p131_fallback(instance_id: str, continent_id: str, kategorie: str, kontinent: str, limit=300):
    # Region oder Stadt → ist Teil eines Landes → das Land liegt auf Kontinent X
    sparql = f"""
    SELECT ?name ?article WHERE {{
      ?place wdt:P31 wd:{instance_id};
             wdt:P131+ ?land;
             rdfs:label ?name.
      ?land wdt:P30 wd:{continent_id}.
      FILTER(LANG(?name) = "de")
      ?article schema:about ?place;
               schema:isPartOf <https://de.wikipedia.org/>.
    }}
    LIMIT {limit}
    """
    return run_query_and_filter(sparql, kategorie, kontinent)


def query_ozeanien(instance_id: str, kategorie: str, kontinent: str, limit_per_country=50):
    all_results = []
    for country_id in OZEANIEN_LAENDER:
        sparql = f"""
        SELECT ?name ?article WHERE {{
          ?place wdt:P31 wd:{instance_id};
                 wdt:P17 wd:{country_id};
                 rdfs:label ?name.
          FILTER(LANG(?name) = "de")
          ?article schema:about ?place;
                   schema:isPartOf <https://de.wikipedia.org/>.
        }}
        LIMIT {limit_per_country}
        """
        results = run_query_and_filter(sparql, kategorie, kontinent)
        all_results += results
        time.sleep(1)
    return all_results


def query_australien(instance_id: str, kategorie: str, kontinent: str, limit=200):
    sparql = f"""
    SELECT ?name ?article WHERE {{
      ?place wdt:P31 wd:{instance_id};
             wdt:P17 wd:{AUSTRALIEN_ID};
             rdfs:label ?name.
      FILTER(LANG(?name) = "de")
      ?article schema:about ?place;
               schema:isPartOf <https://de.wikipedia.org/>.
    }}
    LIMIT {limit}
    """
    return run_query_and_filter(sparql, kategorie, kontinent)


def get_kontinental_reiseziele(instanz_id: str, kontinent_id: str, kategorie: str, kontinent: str, min_zielanzahl: int):
    print(f"Lade {kategorie} in {kontinent} ...")
    reiseziele = query_p30(instanz_id, kontinent_id, kategorie, kontinent)
    if len(reiseziele) < min_zielanzahl:
        print(f"[INFO] Nur {len(reiseziele)} {kategorie} über P30 gefunden. Nutze Fallback P131+ ...")
        reiseziele += query_p131_fallback(instanz_id, kontinent_id, kategorie, kontinent)
    return reiseziele


# ===============================================
# HAUPTFUNKTION
# ===============================================

def main():
    alle_reiseziele: List[Dict[str, str]] = []
    bekannte_namen = set()

    for kontinent, kontinent_id in KONTINENTE.items():
        for kategorie, instanz_id in INSTANZEN.items():
            min_anzahl = MINIMALE_ANZAHL[kategorie]
            try:
                ziele = get_kontinental_reiseziele(instanz_id, kontinent_id, kategorie, kontinent, min_anzahl)
                for ziel in ziele:
                    key = f"{ziel['name']}|{ziel['kategorie']}"
                    if key not in bekannte_namen:
                        bekannte_namen.add(key)
                        alle_reiseziele.append(ziel)
            except Exception as e:
                print(f"[FEHLER] {e}")
            time.sleep(2)

    # Australien
    for kategorie, instanz_id in INSTANZEN.items():
        try:
            print(f"Lade {kategorie} in Australien ...")
            ziele = query_australien(instanz_id, kategorie, OZEANIEN_LABEL)
            for ziel in ziele:
                key = f"{ziel['name']}|{ziel['kategorie']}"
                if key not in bekannte_namen:
                    bekannte_namen.add(key)
                    alle_reiseziele.append(ziel)
        except Exception as e:
            print(f"[FEHLER] {e}")
        time.sleep(2)

    # Ozeanien
    for kategorie, instanz_id in INSTANZEN.items():
        try:
            print(f"Lade {kategorie} in Ozeanien ...")
            ziele = query_ozeanien(instanz_id, kategorie, OZEANIEN_LABEL)
            for ziel in ziele:
                key = f"{ziel['name']}|{ziel['kategorie']}"
                if key not in bekannte_namen:
                    bekannte_namen.add(key)
                    alle_reiseziele.append(ziel)
        except Exception as e:
            print(f"[FEHLER] {e}")
        time.sleep(2)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(alle_reiseziele, f, indent=2, ensure_ascii=False)

    print(f"Fertig! {len(alle_reiseziele)} Reiseziele gespeichert unter '{OUTPUT_PATH}'.")


if __name__ == "__main__":
    main()
