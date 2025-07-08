import requests

def get_description(destination):
    url = f'https://de.wikipedia.org/api/rest_v1/page/summary/{destination}'
    r = requests.get(url)
    return r.json().get('extract', 'Beschreibung nicht verfügbar.')

def get_image(destination):
    url = f'https://de.wikipedia.org/api/rest_v1/page/media/{destination}'
    r = requests.get(url)
    items = r.json().get('items', [])
    for item in items:
        if item.get('type') == 'image':
            return item.get('original', {}).get('source')
    return '/static/default.jpg'
