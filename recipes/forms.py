from django.forms import ModelForm
from django.shortcuts import get_object_or_404

from .models import Ingredient, Recipe, RecipeIngredient
from .utils import get_ingredients


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ('title', 'cooking_time', 'description', 'image',
                  'tags', 'ingredients')

    def clean(self):
        ingredient_added = False
        ingredient_in_db, ingredients_greater_then_zero = True, True
        for key in self.data.keys():

            if 'nameIngredient' in key:
                ingredient_added = True
                if not Ingredient.objects.filter(
                        title=self.data[key]).exists():
                    ingredient_in_db = False

            if 'valueIngredient' in key:
                if int(self.data[key]) <= 0:
                    ingredients_greater_then_zero = False

        if not ingredients_greater_then_zero:
            self.add_error('ingredients',
                           'Количесвто ингредиентов должно быть больше 0')

        if not ingredient_in_db:
            self.add_error('ingredients', 'Выберите ингредиент из списка')

        if not ingredient_added:
            self.add_error('ingredients',
                           'Добавьте ингредиенты к своему рецепту')

    def save_recipe(self, request, recipe):
        ingredients = get_ingredients(request)
        print(ingredients)
        for title, amount in ingredients.items():
            ingredient = get_object_or_404(Ingredient, title=title)
            print(ingredient)
            print(recipe, ingredient, amount)
            recipe_ing = RecipeIngredient(recipe=recipe,
                                          ingredient=ingredient,
                                          amount=amount)
            print(recipe_ing.recipe, recipe_ing.ingredient, recipe_ing.amount)
            recipe_ing.save()
