from pathlib import Path

def find_root(marker='pyproject.toml'):
    current = Path(__file__).resolve()
    
    for parent in current.parents:
        if (parent / marker).exists():
            return parent
    
    raise RuntimeError('[util] Project root not found.')

PROJECT_ROOT = find_root()
DATA_DIR = PROJECT_ROOT / 'data'
ASSETS_DIR = PROJECT_ROOT / 'notebooks' / 'assets'
IMG_DIR = ASSETS_DIR / 'images'