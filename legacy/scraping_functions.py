import requests
import sys
import re
from bs4 import BeautifulSoup as BS

def get_list_TPA():
	# Change encoding to UTF-8 to avoid encoding mistakes
	sys.stdout.reconfigure(encoding='utf-8')

	categories = ['30-minutes-or-less','app-snack-sides','main','dessert','asian',
				'bakery-recipes','dairy-free','gluten-free','vegan','drinks']
	
	# Empty recipe list
	recipes = []
	
	for cat in categories:
		npage = 1
		
		URL = f"https://twoplaidaprons.com/category/{cat}/page/{npage}/"
		page = requests.get(URL)
		
		soup = BS(page.content, 'lxml')
		
		lastPage = int(max([page.get_text() for page in soup.select("a.page-numbers:not(.next)")], default='1'))
		
		for npage in range(1,lastPage+1):
			URL = f"https://twoplaidaprons.com/category/{cat}/page/{npage}/"
			page = requests.get(URL) 
			soup = BS(page.content, 'lxml')
			recs = soup.select("li.listing-item a")
			recs = [rec.get('href') for rec in recs]
			for rec in recs:
				rec_name = rec.rstrip('/').split('/')[-1]
				recipes.append(rec_name)
	
	recipes = set(recipes)
	return recipes
	
def get_recipe_TPA(rec):
	# Change encoding to UTF-8 to avoid encoding mistakes
	sys.stdout.reconfigure(encoding='utf-8')
	
	# Read list of recipes from file and loop over recipes
	
	URL = f"https://twoplaidaprons.com/{rec}/"
	page = requests.get(URL)
	
	soup = BS(page.content, 'lxml')
	
	# Get name of the recipe, ingredients and preparation time and thumbnail
	name = soup.title.string[:-19]
	ingredients = soup.find_all('span', class_='wprm-recipe-ingredient-name')
	ingredients = set([ing.get_text().lower() for ing in ingredients]) # Turn into a set to avoid duplicates
	time = soup.select('div.wprm-recipe-block-container.wprm-recipe-block-container-table.'+ 
		'wprm-block-text-normal.wprm-recipe-time-container.wprm-recipe-total-time-container '+
		'span.wprm-recipe-time.wprm-block-text-normal')
	thumb = soup.select('div.wprm-recipe-container div.wprm-recipe.wprm-recipe-template-template '+
		'div.wprm-container-float-right div.wprm-recipe-image.wprm-block-image-normal img')
	thumb = thumb[0].get('data-lazy-srcset').split(" ")[2]
	
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
	
	return {'name':name,'ingredients':ingredients, 'prep_time':total_minutes, 
		'link':URL, 'thumbnail':thumb,'tag':'Two Plaid Aprons'}
		
def get_list_HSY():
	# Change encoding to UTF-8 to avoid encoding mistakes
	sys.stdout.reconfigure(encoding='utf-8')
	
	categories = ['breakfast','mains','mexican','pasta','salads','sauces','sides-snacks']
	
	# Empty recipe list
	recipes = []
	
	for cat in categories:	
		URL = f"https://healthysimpleyum.com/{cat}/"
		page = requests.get(URL) 
		soup = BS(page.content, 'lxml')
		recs = soup.select("div.box-text-inner.blog-post-inner h5.post-title.is-large a")
		recs = [rec.get('href') for rec in recs]
		for rec in recs:
			rec_name = rec.rstrip('/').split('/')[-1]
			recipes.append(rec_name)
	
	recipes = set(recipes)
	return recipes
	
def get_recipe_HSY(rec):
	# Change encoding to UTF-8 to avoid encoding mistakes
	sys.stdout.reconfigure(encoding='utf-8')
	
	URL = f"https://healthysimpleyum.com/{rec}/"
	page = requests.get(URL)
	
	soup = BS(page.content, 'lxml')
	
	# Get name of the recipe, ingredients, preparation time and thumbnail, and compile it in a dictionary
	name = soup.title.string
	
	ingredients = soup.select('div.tasty-recipes-ingredients li')
	ingredients = [ing.get_text() for ing in ingredients]
	
	time = soup.select('li.total-time span.tasty-recipes-total-time')
	if time:
		time = time[0].get_text()
	else:
		return
		
	thumb = soup.select('figure.wp-block-image.size-large img, div.img-inner.dark img')
	thumb = thumb[0].get('src')#.split(" ")[2]
	
	matches = re.findall(r"(\d+)\s*(hour|hours|hr|minute|minutes|mins)", time, flags=re.IGNORECASE)
	
	total_minutes = 0
	for num, unit in matches:
		num = int(num)
		if unit.lower() in ["hour", "hr", "hours"]:
			total_minutes += num * 60
		else:
			total_minutes += num
			
	if total_minutes == 0:
		total_minutes = max(time.split("-")) 
	
	return {'name':name,'ingredients':ingredients, 'prep_time':total_minutes, 
		'link':URL, 'thumbnail':thumb,'tag':'Healthy Simple Yum'}

def get_list_UG():
	# Change encoding to UTF-8 to avoid encoding mistakes
	sys.stdout.reconfigure(encoding='utf-8')

	# categories = ['breakfast-and-brunch','burgers','deviled-eggs','fritters','muffins-and-quickbreads',
	#			  'pasta','pizza','platters','salads','sandwiches','sauces','sides','snacks',
	#			  'soups','sourdough','stews','tarts','vegetarian-bakes']

	# Empty recipe list
	recipes = []

	for npage in range(1,43):
		URL = f"https://umamigirl.com/category/recipes/page/{npage}/"
		page = requests.get(URL) 
		soup = BS(page.content, 'lxml')
		recs = soup.select("article.post-summary div.post-summary__content a")
		recs = [rec.get('href') for rec in recs]
		for rec in recs:
			rec_name = rec.rstrip('/').split('/')[-1]
			recipes.append(rec_name)

	recipes = set(recipes)
	return recipes

def get_recipe_UG(rec):
	# Change encoding to UTF-8 to avoid encoding mistakes
	sys.stdout.reconfigure(encoding='utf-8')

	URL = f"https://umamigirl.com/{rec}/"
	page = requests.get(URL)

	soup = BS(page.content, 'lxml')

	# Get name of the recipe, ingredients, preparation time and thumbnail, and compile it in a dictionary
	name = soup.title.string
	try:
		ingredients = soup.select('li.wprm-recipe-ingredient span.wprm-recipe-ingredient-name')
		ingredients = [ing.get_text() for ing in ingredients]
		time1 = soup.select('span.wprm-recipe-time.wprm-block-text-none')
		thumb = soup.select('div.wprm-recipe-image.wprm-block-image-rounded.nopin img')
		thumb = thumb[0].get('src')  #.get('data-lazy-srcset').split(" ")[4]
	except:
		print(name)

	if time1:	
		try:
			time = time1[2].get_text()
		except:
			time = time1[1].get_text()
	else:
		#continue
		pass

	matches = re.findall(r"(\d+)\s*(hour|hours|hr|hrs|minute|minutes|mins)", time, flags=re.IGNORECASE)

	total_minutes = 0
	for num, unit in matches:
		num = int(num)
		if unit.lower() in ["hour", "hr", "hours", "hrs"]:
			total_minutes += num * 60
		else:
			total_minutes += num

	return {'name':name,'ingredients':ingredients, 'prep_time':total_minutes, 
		'link':URL, 'thumbnail':thumb,'tag':'Umami Girl'}