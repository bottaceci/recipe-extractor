from pathlib import Path

from recipe_extractor.scraping.discovery import (
    discover_healthysimpleyum_urls, 
    discover_twoplaidaprons_urls,
)
from recipe_extractor.scraping.downloader import (
    download_recipe_page, 
    save_html, 
    save_metadata,
)

# Getting the url list
tpa_urls = discover_twoplaidaprons_urls()[:100] # Only taking first 100 urls for testing
hsy_urls = discover_healthysimpleyum_urls()[:100] # Only taking first 100 urls for testing

urls = tpa_urls + hsy_urls

# Saving the urls and the metadata
for i, url in enumerate(urls, start=1):
    print(f"[{i}/{len(urls)}] Downloading {url}")
    html, metadata = download_recipe_page(url)
    save_html(html, Path(metadata["html_path"]))
    save_metadata(metadata)