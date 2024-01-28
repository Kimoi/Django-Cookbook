from django.contrib import admin
from .models import Product, Recipe, RecipeIngredient


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]


admin.site.register(Product)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient)
