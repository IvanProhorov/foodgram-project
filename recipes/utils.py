from django.db.models import Sum
from django.http import HttpResponse


def get_ingredients(request):
    ingredients = {}
    for key, title in request.POST.items():
        if 'nameIngredient' in key:
            elem = key.split("_")
            ingredients[title] = int(
                request.POST[f'valueIngredient_{elem[1]}'])
    return ingredients


def save_to_file(recipes):
    ingredients = recipes.values(
        'ingredients__title', 'ingredients__dimension').annotate(
        total_amount=Sum('recipe_amount__amount'))
    filename = 'shopping_list.txt'
    content = ''
    for ingredient in ingredients:
        string = f'{ingredient["ingredients__title"]} ' \
                 f'({ingredient["ingredients__dimension"]}) - ' \
                 f'{ingredient["total_amount"]}'
        content += string + '\n'
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(
        filename)
    return response
