
# Django Cookbook Project

**Cookbook application using Django**

## ✅Done:

- Models: Product, Recipe, RecipeIngredient
- DB: SQLite
- Views:
  - add_product_to_recipe
  - cook_recipe
  - show_recipes_without_product
- Admin panel configured to manage the 
products and recipes included in the database

## ✨Give it a try:

- Clone repo
- Activate venv

`pip install -r requirements.txt`

`python manage.py migrate`

`python manage.py createsuperuser`

- Populate database with test data

`python manage.py shell`

`exec(open('dbscript.py').read())`

## ⚡Example endpoints:

>>/add/?recipe_id=3&product_id=1&weight=1000
> 
>We just added 1000g of Kiwi to Fruits With Fruits recipe. 
> Ingredient update functionality also included

>>/cook/3
>
>usage_count for every product in Fruits With Fruits recipe is incremented

>>/filter/1
>
>Recipes without Kiwi is shown. `10g` rule also implemented
