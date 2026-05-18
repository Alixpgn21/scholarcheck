"""
Gestion du cache SQLite pour les requêtes API académiques.
"""
import sqlite3
import json
import hashlib
import functools
from pathlib import Path

# Création de la base de données de cache
CACHE_DIR = Path(__file__).parent.parent.parent / ".cache"
CACHE_DIR.mkdir(exist_ok=True)
DB_PATH = CACHE_DIR / "api_cache.db"

def _init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS api_cache (
                key TEXT PRIMARY KEY,
                value TEXT
            )
            """
        )

_init_db()

def _generate_key(func_name: str, args: tuple, kwargs: dict) -> str:
    # Créer une clé unique basée sur le nom de la fonction et ses arguments
    key_data = {"func": func_name, "args": args, "kwargs": kwargs}
    key_str = json.dumps(key_data, sort_keys=True)
    return hashlib.sha256(key_str.encode("utf-8")).hexdigest()

def get_cache(key: str) -> dict | None:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("SELECT value FROM api_cache WHERE key = ?", (key,))
        row = cursor.fetchone()
        if row:
            return json.loads(row[0])
    return None

def set_cache(key: str, value: dict | None):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT OR REPLACE INTO api_cache (key, value) VALUES (?, ?)",
            (key, json.dumps(value))
        )

def cached_api_call(func):
    """
    Décorateur pour mettre en cache les résultats des appels API.
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        key = _generate_key(func.__name__, args, kwargs)
        cached_result = get_cache(key)
        
        if cached_result is not None:
            # Si le résultat mis en cache est un dictionnaire spécial {"__null__": True},
            # cela signifie que la précédente requête n'a rien trouvé (None).
            if cached_result.get("__null__") is True:
                return None
            return cached_result
            
        # Sinon, on exécute la vraie fonction
        result = await func(*args, **kwargs)
        
        # On met en cache le résultat
        if result is None:
            set_cache(key, {"__null__": True})
        else:
            set_cache(key, result)
            
        return result
        
    return wrapper
