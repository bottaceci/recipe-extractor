import requests
from bs4 import BeautifulSoup as bs
from xml.etree.ElementTree import fromstring
from urllib.parse import urlparse
from pathlib import Path
import json

METADATA_FILE_PATH = Path("data/metadata_web.jsonl")

def discover_urls(xml_map_url, check_english=False) -> dict[str,str]:
    xml_map = requests.get(xml_map_url)
    root = fromstring(xml_map.content)

    recipe_urls: set[str] = set()
    metadata = {}

    for i in range(len(root)):
        recipe_url = root[i][0].text
        thumbnail_url = root[i][2][0].text

        if check_english:
            html = requests.get(recipe_url).content
            soup = bs(html, 'html.parser')
            if not soup.html["lang"] in ['en-US', 'en-UK', 'en']:
                continue

        metadata = {
            "url": recipe_url,
            "source": source_from_url(recipe_url),
            "thumbnail_url": thumbnail_url
        }

def source_from_url(url: str) -> str:
    domain = urlparse(url).netloc.lower()

    return domain[:-4] # take out '.com'

def save_metadata(metadata: dict, metadata_path: Path = METADATA_FILE_PATH) -> None:
    metadata_path.parent.mkdir(parents=True, exist_ok=True)

    with open(metadata_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(metadata) + "\n")

def discover_twoplaidaprons_urls() -> list[str]:
	
    categories = ['30-minutes-or-less','app-snack-sides','main','dessert','asian',
				'bakery-recipes','dairy-free','gluten-free','vegan','drinks']
	
    recipe_urls: set[str] = set()
	
    for category in categories:

        first_page_url = f"https://twoplaidaprons.com/category/{category}/page/1/"
        response = requests.get(first_page_url, timeout=10)
        response.raise_for_status()
        
        soup = bs(response.content, "html.parser")
        
        last_page = int(
            max(
                [page.get_text() for page in soup.select("a.page-numbers:not(.next)")], 
                default='1',
            )
        )
        
        for page_number in range(1, last_page + 1):
            url = f"https://twoplaidaprons.com/category/{category}/page/{page_number}/"
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            soup = bs(response.content, "html.parser")

            for link in soup.select("li.listing-item a"):
                href = link.get("href")
                if href:
                    recipe_urls.add(href)

    return sorted(recipe_urls)

def discover_healthysimpleyum_urls() -> list[str]:

    categories = ['breakfast','mains','mexican','pasta','salads','sauces',
                  'sides-snacks']
    
    recipe_urls: set[str] = set()

    for category in categories:

        url = f"https://healthysimpleyum.com/{category}/"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = bs(response.content, "html.parser")

        for link in soup.select("div.box-text-inner.blog-post-inner h5.post-title.is-large a"):
            href = link.get("href")
            if href:
                recipe_urls.add(href)

    return sorted(recipe_urls)