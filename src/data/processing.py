import os
import sys
import json

from utils.paths import DATA_DIR

RAW_PATH = DATA_DIR / 'default-cards.json'
PROCESSED_PATH = DATA_DIR / 'creatures_full.ndjson'

def ensure_dataset():
    
    # Ensure raw dataset exists, otherwise download from Scryfall API
    if not os.path.exists(RAW_PATH):
        print('[pipeline] Raw dataset not found. Downloading...')
    
        try:
            from data.download import download_data
            download_data()
        except Exception as e:
            print('[pipeline] Download failed:', e)
            return
        
    else:
        print('[pipeline] Raw dataset already exists.')

    # Process the dataset
    if not os.path.exists(PROCESSED_PATH):
        print('[pipeline] Processed dataset not found. Creating creatures dataset...')
        
        try:
            import ijson
        except ImportError:
            print('[pipeline] ijson not found. Installing...')
            import subprocess
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'ijson'])
            import ijson

        count = 0
        
        with open(RAW_PATH, 'rb') as f, open(PROCESSED_PATH, 'w') as out:
            for card in ijson.items(f, 'item'):
                if 'Creature' in card.get('type_line', ''):
                    out.write(json.dumps(card, default=float) + '\n')
                    count += 1
        
        print(f'[pipeline] Processing complete! Creatures written: {count}')
    
    else:
        print('[pipeline] Processed dataset already exists.')

if __name__ == '__main__':
    ensure_dataset()