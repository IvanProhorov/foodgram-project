import csv

from django.core.management.base import BaseCommand
from recipes.models import Ingredient, Tag


class Command(BaseCommand):
    help = 'load ingredients data'

    def handle(self, *args, **options):
        with open('recipes/fixtures/ingredients.csv',encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                title, dimension = row
                Ingredient.objects.get_or_create(title=title,
                                                 dimension=dimension)
                print(f'Добавлен ингридиент {title} {dimension}')

        Tag.objects.get_or_create(title='завтрак', slug='breakfast',
                                  color='orange')
        Tag.objects.get_or_create(title='обед', slug='lunch', color='green')
        Tag.objects.get_or_create(title='ужин', slug='dinner', color='purple')
