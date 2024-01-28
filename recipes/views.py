from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET
from django.db.models import Q

from .models import Product, Recipe, RecipeIngredient


@require_GET
def add_product_to_recipe(request):
    # http://127.0.0.1:8000/add/?recipe_id=1&product_id=5&weight=200
    try:
        recipe_id = request.GET.get('recipe_id')
        product_id = request.GET.get('product_id')
        weight = request.GET.get('weight')

        recipe = Recipe.objects.get(id=recipe_id)
        product = Product.objects.get(id=product_id)

        recipe_ingredient, created = RecipeIngredient.objects.get_or_create(
            recipe=recipe,
            ingredient=product,
            defaults={'weight': weight}
        )
        if not created:  # if recipe_ingredient is already exist we update it:
            recipe_ingredient.weight = weight
            recipe_ingredient.save()
        return JsonResponse({'message': 'Product added/updated successfully.'})

    except Recipe.DoesNotExist:
        return JsonResponse({'message': "Recipe does not exist."})

    except Product.DoesNotExist:
        return JsonResponse({'message': "Product does not exist."})

    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)


@require_GET
def cook_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe.objects.prefetch_related('ingredients'), id=recipe_id)
    recipe_ingredients = recipe.ingredients.all()

    for recipe_ingredient in recipe_ingredients:
        upd_count = recipe_ingredient.ingredient.usage_count + 1
        recipe_ingredient.ingredient.usage_count = upd_count
        recipe_ingredient.ingredient.save()
    return JsonResponse({'message': 'Counts for each product used in recipe was successfully incremented.'})


@require_GET
def show_recipes_without_product(request, product_id):
    filtered_recipes = Recipe.objects.exclude(
        Q(ingredients__ingredient=product_id) &
        Q(ingredients__weight__gt=9)
    ).distinct()
    return render(request, 'recipes/filter-tab.html', {'filtered_recipes': filtered_recipes})
