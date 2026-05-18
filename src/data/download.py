import requests
from utils.paths import DATA_DIR

DATA_PATH = DATA_DIR / 'default-cards.json'

def download_data():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    print('[download] Fetching Scryfall bulk data metadata...')
    res = requests.get('https://api.scryfall.com/bulk-data', timeout=30)
    res.raise_for_status()
    
    data = res.json()

    download_url = None
    for item in data['data']:
        if item['type'] == 'default_cards':
            download_url = item['download_uri']
            break

    if not download_url:
        raise Exception('[download] Could not find default_cards dataset.')
    
    print('[download] Download URL:', download_url)

    print('[download] Downloading dataset (this may take ~30-90 seconds)...')
    r = requests.get(download_url, stream=True, timeout=120)
    r.raise_for_status()

    with open(DATA_PATH, 'wb') as f:
        for chunk in r.iter_content(1024 * 1024):
            if chunk:
                f.write(chunk)

    print('[download] Download complete!')

if __name__ == '__main__':
    download_data()