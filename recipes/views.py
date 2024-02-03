from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET
from django.db.models import F, Exists, OuterRef
from django.db import transaction

from .models import Product, Recipe, RecipeIngredient


@require_GET
def add_product_to_recipe(request):
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
    try:
        with transaction.atomic():
            recipe = get_object_or_404(Recipe.objects.prefetch_related('ingredients'), id=recipe_id)
            recipe_ingredients_ids = recipe.ingredients.values_list('ingredient_id', flat=True)
            Product.objects.filter(id__in=recipe_ingredients_ids).update(usage_count=F('usage_count') + 1)
            return JsonResponse({'message': 'Counts for each product used in recipe was successfully incremented.'})
    except Exception as e:
        return JsonResponse({'message': 'Error while updating counts: ' + str(e)}, status=500)


@require_GET
def show_recipes_without_product(request, product_id):
    filtered_recipes = Recipe.objects.exclude(
        Exists(RecipeIngredient.objects.filter(
            recipe=OuterRef('pk'),
            ingredient_id=product_id,
            weight__gt=9)))
    return render(request, 'recipes/filter-tab.html', {'filtered_recipes': filtered_recipes})
