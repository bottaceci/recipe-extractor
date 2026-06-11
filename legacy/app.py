import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Recipe, Ingredient, recipe_ingredient

def main():
	# Connect to the database
	engine = create_engine('sqlite:///recipes.db')
	Session = sessionmaker(bind=engine)
	session = Session()
	
	# Streamlit app layout
	st.title("Recipe Dashboard")
	
	# A simple sidebar for filtering recipes by prep time
	min_prep_time = st.sidebar.slider("Minimum Prep Time (minutes)", 
		min_value=0, max_value=240, value=0, step=10)
	max_prep_time = st.sidebar.slider("Maximum Prep Time (minutes)", 
		min_value=0, max_value=240, value=240, step=10)
	
	# Checkbox for long recipes
	include_long_recipes = st.sidebar.checkbox("Include recipes with prep time > 240 minutes")
	if include_long_recipes:
		max_prep_time = 9999
	
	# Text input for search (recipe name)
	search_term_1 = st.sidebar.text_input("Search recipes by name:")
	
	# Text input for search (ingredient name)
	search_term_2 = st.sidebar.text_input("Search recipes by ingredient(s):")
	
	# Sidebar tag menu
	all_tags = [t[0] for t in session.query(Recipe.tag).distinct().all()]
	selected_tags = st.sidebar.multiselect("Select website tags", 
		options=all_tags, default=all_tags)
	
	# Query the database for recipes under the selected prep time, name and tag (provenience)
	query = session.query(Recipe).filter(
		Recipe.prep_time <= max_prep_time, 
		Recipe.prep_time >= min_prep_time,
		Recipe.name.ilike(f"%{search_term_1}%"),
		Recipe.tag.in_(selected_tags)
		)
	# Apply a filter for each ingredient term
	if search_term_2:
		search_ingredients = search_term_2.split(",") # make a list
		for ingredient_term in search_ingredients:
			query = query.filter(Recipe.ingredients.any(Ingredient.name.ilike(f"%{ingredient_term.strip()}%")))
	
	recipes = query.all()
	num = len(recipes)
		
	if search_term_2 != "":
		st.write(f"There are {num} recipes with a prep time between {min_prep_time} and {max_prep_time} minutes,"
		+ f" containing {search_term_2}:")
	else:
		st.write(f"There are {num} recipes with a prep time between {min_prep_time} and {max_prep_time} minutes:")
	
	if recipes:
		for recipe in recipes:
			st.subheader(recipe.name)
			# Create two columns: one for the image and one for the text details
			col1, col2 = st.columns([1, 2])
			with col1:
				st.image(recipe.thumbnail, width=280)
			with col2:
				ingredients = [ingr.name for ingr in recipe.ingredients]
				ingredients_str = ", ".join(ingredients)
				# Adjust the padding-top value to move the text down vertically.
				st.markdown(
					f"""
					<div style="padding-top:0px;">
						<p>Prep Time: {recipe.prep_time} minutes</p>
						<p><b>Ingredients:</b> {ingredients_str}</p>
						<p><a href="{recipe.link}" target="_blank">View Recipe</a></p>
					</div>
					""",
					unsafe_allow_html=True,
					)
			st.markdown("<hr style='margin-top: 40px; margin-bottom: 40px;'>", unsafe_allow_html=True)
	else:
		st.write("No recipes found with the selected criteria.")
		
if __name__=="__main__":
	main()
	
	