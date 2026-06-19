import json
from pathlib import Path

def load_cache(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_cache(cache: dict[str, str], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2, sort_keys=True)

def make_cache_key(name: str) -> str:
    return " ".join(name.lower().strip().split())

def get_cached_normalization(name: str, cache: dict[str, str]) -> str:
    key = make_cache_key(name)
    return cache.get(key)

def set_cached_normalization(name: str, normalized: str, cache: dict[str, str]) -> None:
    key = make_cache_key(name)
    cache[key] = normalized