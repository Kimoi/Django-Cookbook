from django.urls import path
from . import views


urlpatterns = [
    path('add/', views.add_product_to_recipe, name='add_product_to_recipe'),
    path('cook/<int:recipe_id>', views.cook_recipe, name='cook_recipe'),
    path('filter/<int:product_id>', views.show_recipes_without_product, name='recipes_without_product'),
]
