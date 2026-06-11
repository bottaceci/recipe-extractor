from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Recipe, Ingredient

engine = create_engine('sqlite:///recipes.db')
Session = sessionmaker(bind=engine)
session = Session()

# Write the desired query
recipes_under_10 = session.query(Recipe).filter(Recipe.prep_time < 10).all()

for recipe in recipes_under_10:
	print(recipe.name, recipe.prep_time, recipe.link)