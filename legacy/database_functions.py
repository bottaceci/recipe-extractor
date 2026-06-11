def get_or_create_ingredient(session, name, ingredient_cache, Ingredient):
	"""
	Try to get an Ingredient by name from an in-memory cache or the database.
	If not found, create a new Ingredient, add it to the session, and update the cache.
	"""
	# Check in the cache first
	if name in ingredient_cache:
		return ingredient_cache[name]
		
	# Query the database
	ingredient = session.query(Ingredient).filter_by(name=name).first()
	if ingredient:
		ingredient_cache[name] = ingredient
		return ingredient
		
	# Create a new Ingredient if not found
	ingredient = Ingredient(name=name)
	session.add(ingredient)
	# Optionally flush to assign an ID immediately
	session.flush()
	ingredient_cache[name] = ingredient
	return ingredient
	
def process_recipe(session, Recipe, recipe_dict, cache, Ingredient):
	# recipe_dict should have keys: 'name', 'ingredients', 'prep_time', 'link', 'thumbnail'
	try:
		recipe = Recipe(
			name=recipe_dict['name'],
			prep_time=recipe_dict['prep_time'],
			link=recipe_dict['link'],
			thumbnail=recipe_dict['thumbnail'],
			tag=recipe_dict['tag']
			)
	except:
		print(recipe_dict)
	session.add(recipe)
	session.flush()
	# Process each ingredient in the list
	for ingredient_name in recipe_dict['ingredients']:
		ingredient_obj = get_or_create_ingredient(session, ingredient_name, cache, Ingredient)
		recipe.ingredients.append(ingredient_obj)
		
	session.commit()