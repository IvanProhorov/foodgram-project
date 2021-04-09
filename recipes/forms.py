from django.forms import ModelForm

from .models import Ingredient, Recipe


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
                           'Добавьте ингредиенты к совему рецепту')
