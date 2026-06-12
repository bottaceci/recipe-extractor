import re
from bs4 import BeautifulSoup as bs
from copy import copy

from recipe_extractor.extraction.base import RecipeExtractor
from recipe_extractor.extraction.exceptions import UnsupportedSourceError
from recipe_extractor.data.schemas import RecipeData, IngredientData
from recipe_extractor.data.ingredients import normalize_ingredient, amount_convertor

class DeterministicRecipeExtractor(RecipeExtractor):
    def extract(self, html: str, url: str) -> RecipeData:
        if "twoplaidaprons" in url:
            return self._extract_twoplaidaprons(html, url)
        
        if "healthysimpleyum" in url:
            return self._extract_healthysimpleyum(html, url)
        
        if "umamigirl" in url:
            ...
            #use Umami Girl logic

        raise UnsupportedSourceError(f"Unsupported recipe source for URL: {url}")
        
    def _extract_twoplaidaprons(self, html: str, url: str) -> RecipeData:
        ingredients = []

        soup = bs(html, "html.parser")

        # Get name of the recipe
        title = soup.find('h2', class_='wprm-recipe-name wprm-block-text-bold').get_text()

        # Get ingredients
        ings = soup.find_all('li', class_='wprm-recipe-ingredient')
        for ing in ings:
            ing_name = ing.find('span', class_='wprm-recipe-ingredient-name').get_text()
            ing_amount = ing.find('span', class_='wprm-recipe-ingredient-amount')
            if ing_amount:
                ing_amount = amount_convertor(ing_amount.get_text())
            ing_unit = ing.find('span', class_='wprm-recipe-ingredient-unit')
            if ing_unit:
                ing_unit = ing_unit.get_text()
            ing_norm_name = normalize_ingredient(ing_name)
            ingredients.append(
                IngredientData(
                    name=ing_name,
                    normalized_name=ing_norm_name,
                    raw_text=str(ing),
                    quantity=ing_amount,
                    unit=ing_unit,
                )
            )

        # Get preparation time
        time = soup.select('div.wprm-recipe-block-container.wprm-recipe-block-container-table.'+ 
            'wprm-block-text-normal.wprm-recipe-time-container.wprm-recipe-total-time-container '+
            'span.wprm-recipe-time.wprm-block-text-normal')
        
        # Get total time in minutes
        if time:
            time = time[0].get_text()
        else:
            time = '0 minutes'
        
        matches = re.findall(r"(\d+)\s*(hour|hours|hr|minute|minutes|mins)", time, flags=re.IGNORECASE)
        
        total_minutes = 0
        for num, unit in matches:
            num = int(num)
            if unit.lower() in ["hour", "hr", "hours"]:
                total_minutes += num * 60
            else:
                total_minutes += num
        
        # Get thumbnail
        try:
            thumb = soup.select('div.wprm-recipe-container div.wprm-recipe.wprm-recipe-template-template '+
                'div.wprm-container-float-right div.wprm-recipe-image.wprm-block-image-normal img')
            thumbnail = thumb[0].get('data-lazy-srcset').split(" ")[2]
        except:
            thumbnail = None

        recipe = RecipeData(
            title = title,
            url = url,
            source = "Two Plaid Aprons",
            total_time = total_minutes,
            thumbnail_url = thumbnail,
            ingredients = ingredients
        )

        return recipe
    
    def _extract_healthysimpleyum(self, html: str, url: str) -> RecipeData:
        ingredients = []

        soup = bs(html, "html.parser")

        # Get name of the recipe
        title = soup.title.string

        # Get ingredients
        ings = soup.select('div.tasty-recipes-ingredients li')
        for ing in ings:
            raw_text = str(copy(ing))
            if ing.find("span", class_='nutrifox-quantity'):
                amount_span = ing.find("span", class_='nutrifox-quantity')
                ing_amount = amount_convertor(amount_span.get_text())
                amount_span.decompose()
                unit_span = ing.find("span", class_ = 'nutrifox-unit')
                ing_unit = unit_span.get_text()
                unit_span.decompose()
                ing_name = ing.get_text(strip=True)
                ing_norm_name = normalize_ingredient(ing_name)
            elif ing.find("span"):
                amount_spans = ing.find_all("span", attrs={"data-amount": True})

                if amount_spans:
                    ing_amount = amount_convertor(amount_spans[0].get("data-amount"))
                    ing_unit = amount_spans[0].get("data-unit")

                    for span in amount_spans:
                        span.decompose()

                    ing_name = ing.get_text(" ", strip=True)
                    ing_name = re.sub(r"^[–\-—\s]+", "", ing_name)
                    ing_norm_name = normalize_ingredient(ing_name)
                else:
                    span = ing.find("span")
                    ing_amount = amount_convertor(span.get('data-amount'))
                    ing_unit = span.get('data-unit')
                    span.decompose()
                    ing_name = ing.get_text(strip=True)
                    ing_norm_name = normalize_ingredient(ing_name)
            else: 
                ing_name = ing.get_text(strip=True)
                ing_norm_name = normalize_ingredient(ing_name)
                ing_amount = None
                ing_unit = None

            ingredients.append(
                IngredientData(
                    name=ing_name,
                    normalized_name=ing_norm_name,
                    raw_text=raw_text,
                    quantity=ing_amount,
                    unit=ing_unit
                )
            )

        # Get preparation time
        time = soup.select('li.total-time span.tasty-recipes-total-time')

        if time:
            time_text = time[0].get_text(" ", strip=True)
            # Get total time in minutes
            matches = re.findall(r"(\d+)\s*(hour|hours|hr|minute|minutes|mins)", time_text, flags=re.IGNORECASE)

            total_minutes = 0

            for num, unit in matches:
                num = int(num)
                if unit.lower() in ["hour", "hr", "hours"]:
                    total_minutes += num * 60
                else:
                    total_minutes += num
                    
            if total_minutes == 0:
                total_minutes = max(time_text.split("-")) 
        else:
            total_minutes = None

        # Get thumbnail
        try:
            thumb = soup.select('figure.wp-block-image.size-large img, div.img-inner.dark img')
            thumbnail = thumb[0].get('src')
        except (IndexError, AttributeError):
            thumbnail = None

        recipe = RecipeData(
            title = title,
            url = url,
            source = "Healthy Simple Yum",
            total_time = total_minutes,
            thumbnail_url = thumbnail,
            ingredients = ingredients
        )

        return recipe
        