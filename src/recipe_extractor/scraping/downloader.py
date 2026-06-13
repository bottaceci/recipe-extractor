from urllib.parse import urlparse
from pathlib import Path
import requests
import json

METADATA_FILE_PATH = Path("data/metadata.jsonl")
HTML_PATH_ROOT = Path("data/raw_html")

def download_html(url: str) -> str:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text

def source_from_url(url: str) -> str:
    domain = urlparse(url).netloc.lower()

    if "twoplaidaprons" in domain:
        return "twoplaidaprons"
    if "healthysimpleyum" in domain:
        return "healthysimpleyum"

    return domain.replace(".", "_")

def url_to_slug(url: str) -> str:
    return Path(urlparse(url).path).stem

def build_html_path(url: str) -> Path:
    source = source_from_url(url)
    slug = url_to_slug(url)
    return HTML_PATH_ROOT / source / f"{slug}.html"

def save_html(html: str, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

def save_metadata(metadata: dict, metadata_path: Path = METADATA_FILE_PATH) -> None:
    metadata_path.parent.mkdir(parents=True, exist_ok=True)

    with open(metadata_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(metadata) + "\n")

def download_recipe_page(url: str) -> tuple[str, dict[str, str]]:
    html = download_html(url)
    source = source_from_url(url)
    html_path = build_html_path(url)

    metadata = {
        "url": url,
        "source": source,
        "html_path": str(html_path),
    }

    return html, metadata

