# My functions for getting recipes data and processing recipes
import scraping_functions as sf
from database_functions import process_recipe
# My classes for recipes and ingredients
from models import Base, Recipe, Ingredient
# SQL functions
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

engine = create_engine('sqlite:///recipes.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Add the recipes to the database 
ingredient_cache = {}

# Websites
tags = ['TPA','HSY','UG']

for tag in tags:
	get_list = getattr(sf, f"get_list_{tag}")
	get_recipe = getattr(sf, f"get_recipe_{tag}")
	recipe_list = get_list()
	
	for rec in recipe_list:
		try:
			recipe_dict = get_recipe(rec)
		except:
			continue
		if recipe_dict:
			rec1 = session.query(Recipe).filter_by(name=recipe_dict['name']).first()
			if rec1:
				continue
			else:
				process_recipe(session, Recipe, recipe_dict, ingredient_cache, Ingredient)
		else:
			continue
	
print('Database created!')
