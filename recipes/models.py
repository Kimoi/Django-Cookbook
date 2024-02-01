from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import UniqueConstraint


class Product(models.Model):
    name = models.CharField(max_length=64, unique=True)
    usage_count = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return f'{self.id} - {self.name}'


class Recipe(models.Model):
    name = models.CharField(max_length=128, unique=True)

    class Meta:
        verbose_name = "Recipe"
        verbose_name_plural = "Recipes"

    def __str__(self):
        return f'{self.id} - {self.name}'


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(Product, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
    weight = models.PositiveIntegerField(
        default=100, validators=[MinValueValidator(1), MaxValueValidator(100000)])

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=('ingredient', 'recipe'),
                name='unique_recipe_ingredient')]
        verbose_name = "Recipe Ingredient"
        verbose_name_plural = "Recipe Ingredients"

    def __str__(self):
        return f'{self.ingredient.name} from {self.recipe.name} recipe - {self.weight}g'
