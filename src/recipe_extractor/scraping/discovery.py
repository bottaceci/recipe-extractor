import requests
from bs4 import BeautifulSoup as bs

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