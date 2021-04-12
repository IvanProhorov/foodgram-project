import logging
import sys

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RecipeForm
from .models import (FavoriteRecipe, Recipe, ShoppingList, Subscription, User)
from .utils import save_to_file

FORMAT = '[%(asctime)s] {%(pathname)s:%(lineno)d - %(funcName)s()} ' \
         '%(levelname)s - %(message)s'
logging.basicConfig(stream=sys.stdout, format=FORMAT)
logger = logging.getLogger(__name__)


def index(request):
    tags = request.GET.getlist('tag')
    recipe_list = Recipe.objects.tag_filter(tags)
    paginator = Paginator(recipe_list, settings.RECIPES_ON_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html',
                  {'page': page, 'paginator': paginator})


@login_required
def new_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)

    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.save()
        form.save_m2m()
        form.save_recipe(request, recipe)
        return redirect('index')
    return render(request, 'recipes/new_recipe.html', {'form': form})


@login_required
def recipe_edit(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, author__username__exact=username,
                               pk=recipe_id)
    print(username, request.user)
    if username != str(request.user):
        return redirect('recipe_view', username, recipe_id)
    else:
        form = RecipeForm(request.POST or None, files=request.FILES or None,
                          instance=recipe)
        if form.is_valid():
            form.save()
            form.save_recipe(request, recipe)
            return redirect('recipe_view', username, recipe_id)
        return render(request, 'recipes/new_recipe.html',
                      {'form': form, 'recipe': recipe})


@login_required
def recipe_delete(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, author__username__exact=username,
                               pk=recipe_id)
    if username != request.user:
        return redirect('recipe_view', username, recipe_id)
    else:
        recipe.delete()
    return redirect('index')


def profile(request, username):
    tags = request.GET.getlist('tag')
    author = get_object_or_404(User, username=username)
    post_list = Recipe.objects.tag_filter(tags).filter(author=author)
    paginator = Paginator(post_list, settings.RECIPES_ON_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'recipes/profile.html',
                  {'author': author, 'page': page, 'paginator': paginator})


def recipe_view(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, author__username__exact=username,
                               pk=recipe_id)
    return render(request, 'recipes/single_page.html',
                  {'author': username, 'recipe': recipe})


@login_required
def favorite_recipe(request):
    tags = request.GET.getlist('tag')
    favorite_list = FavoriteRecipe.objects.favorite_recipe(request.user, tags)
    paginator = Paginator(favorite_list, settings.RECIPES_ON_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    if not page:
        return render(request, 'recipes/custom_page.html')
    return render(request, 'recipes/favorite.html',
                  {'page': page, 'paginator': paginator})


@login_required
def subscriptions_index(request):
    subscriptions_list = Subscription.objects.subscriptions(user=request.user)
    paginator = Paginator(subscriptions_list, settings.RECIPES_ON_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    if not page:
        return render(request, 'recipes/custom_page.html')
    return render(request, 'recipes/subscription.html',
                  {'page': page, 'paginator': paginator})


def shopping_list(request):
    if request.user.is_authenticated:
        recipes = ShoppingList.objects.shopping_cart(user=request.user)
    else:
        try:
            recipes = Recipe.objects.filter(
                pk__in=request.session[settings.PURCHASE_SESSION_ID])
        except Exception as e:
            logger.error(str(e))
            return render(request, 'recipes/custom_page.html')
    if not recipes:
        return render(request, 'recipes/custom_page.html')
    return render(request, 'recipes/shopping_list.html', {'recipes': recipes})


def delete_purchase(request, recipe_id):
    if request.user.is_authenticated:
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        purchase = get_object_or_404(ShoppingList, user=request.user,
                                     recipe=recipe)
        purchase.delete()
    else:
        try:
            request.session[settings.PURCHASE_SESSION_ID].remove(
                str(recipe_id))
            request.session.save()
        except Exception as e:
            logger.error(str(e))
    return redirect('shopping_list')


def save_shopping_list(request):
    if request.user.is_authenticated:
        recipes = ShoppingList.objects.shopping_cart(user=request.user)
    else:
        try:
            recipes = Recipe.objects.filter(
                pk__in=request.session[settings.PURCHASE_SESSION_ID])
        except Exception as e:
            logger.error(str(e))
            return render(request, 'recipes/custom_page.html')
    if recipes:
        return save_to_file(recipes)
    else:
        return render(request, 'recipes/custom_page.html')
