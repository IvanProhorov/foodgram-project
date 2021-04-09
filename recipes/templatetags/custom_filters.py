import pymorphy2
from django import template
from django.conf import settings
from recipes.models import FavoriteRecipe, ShoppingList, Subscription, Tag

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter
def is_favorite(recipe, user):
    return FavoriteRecipe.objects.filter(recipe=recipe, user=user).exists()


@register.filter
def all_tags(value):
    return Tag.objects.all()


@register.filter
def get_active_tags(value):
    return value.getlist('tag')


@register.filter
def change_tag_link(request, tag):
    copy = request.GET.copy()
    if copy.getlist('page'):
        copy.pop('page')
    tag_link = copy.getlist('tag')
    if tag.slug in tag_link:
        tag_link.remove(tag.slug)
        copy.setlist('tag', tag_link)
    else:
        copy.appendlist('tag', tag.slug)
    return copy.urlencode()


@register.filter
def is_subscribe(author, user):
    return Subscription.objects.filter(author=author, user=user).exists()


@register.filter
def subtract(num1, num2):
    return num1 - num2


@register.filter
def word_form(word, number):
    morph = pymorphy2.MorphAnalyzer()
    default_word = morph.parse(word)[0]
    changed_word = default_word.make_agree_with_number(number).word
    return changed_word


@register.filter
def in_shopping_list(request, recipe):
    if request.user.is_authenticated:
        return ShoppingList.objects.filter(user=request.user, recipe=recipe)
    else:
        try:
            return str(recipe.id) in request.session[
                settings.PURCHASE_SESSION_ID]
        except KeyError:
            return False


@register.filter
def shopping_count(request):
    if request.user.is_authenticated:
        return ShoppingList.objects.filter(user=request.user).count()
    else:
        try:
            return len(request.session[settings.PURCHASE_SESSION_ID])
        except KeyError:
            return 0


@register.filter
def change_page_url(request, page):
    copy = request.GET.copy()
    copy['page'] = page
    return copy.urlencode()
