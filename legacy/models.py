from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Association table for the many-to-many relationship
recipe_ingredient = Table(
	'recipe_ingredient', Base.metadata,
	Column('recipe_id', Integer, ForeignKey('recipes.id')),
	Column('ingredient_id', Integer, ForeignKey('ingredients.id'))
	)

class Recipe(Base):
	__tablename__ = 'recipes'
	id = Column(Integer, primary_key=True)
	name = Column(String, nullable=False)
	prep_time = Column(Integer, nullable=False)  # in minutes
	link = Column(String, nullable=False)
	thumbnail = Column(String, nullable=False)
	tag = Column(String, nullable=False)
	
	# Establishing a many-to-many relationship with ingredients
	ingredients = relationship('Ingredient', secondary=recipe_ingredient, 
		back_populates='recipes')
	
class Ingredient(Base):
	__tablename__ = 'ingredients'
	id = Column(Integer, primary_key=True)
	name = Column(String, unique=True, nullable=False)
	
	recipes = relationship('Recipe', secondary=recipe_ingredient, 
		back_populates='ingredients')