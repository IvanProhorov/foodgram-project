from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()

__all__ = [
    'Ingredient',
    'Tag',
    'RecipeManager',
    'Recipe',
    'RecipeIngredient',
    'FavoriteRecipe',
    'FavoriteRecipeManager',
    'SubscriptionManager',
    'Subscription',
    'ShoppingListManager',
    'ShoppingList',
]


class Ingredient(models.Model):
    title = models.CharField(max_length=255, verbose_name='ingredient title')
    dimension = models.CharField(max_length=64,
                                 verbose_name='ingredient dimension')

    def __str__(self):
        return f'{self.pk} - {self.title} - {self.dimension}'

    class Meta:
        verbose_name = "ingredient"
        verbose_name_plural = "ingredients"


class Tag(models.Model):
    title = models.CharField(max_length=50, verbose_name='tag title')
    slug = models.SlugField(max_length=50, verbose_name='tag slug',
                            unique=True)
    color = models.SlugField(verbose_name='tag color')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = "tag"
        verbose_name_plural = "tags"


class RecipeManager(models.Manager):

    @staticmethod
    def tag_filter(tags):
        if tags:
            return Recipe.objects.filter(tags__slug__in=tags).order_by(
                '-pub_date').distinct()
        else:
            return Recipe.objects.order_by('-pub_date').all()

    class Meta:
        verbose_name = "recipe manager"
        verbose_name_plural = "recipe managers"


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='recipe author',
                               related_name='author_recipes')
    title = models.CharField(max_length=255, verbose_name='recipe title')
    image = models.ImageField(upload_to='recipe/', verbose_name='recipe image')
    description = models.TextField(verbose_name='recipe description')
    ingredients = models.ManyToManyField(Ingredient,
                                         through='RecipeIngredient',
                                         verbose_name='recipe ingredient',
                                         blank=True)
    tags = models.ManyToManyField(Tag, related_name='recipes', blank=True,
                                  verbose_name='recipe tag')
    cooking_time = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='recipe cooking time')
    pub_date = models.DateTimeField(verbose_name='date published',
                                    auto_now_add=True,
                                    db_index=True)

    objects = RecipeManager()

    def __str__(self):
        return f'{self.pk} - {self.title} - {self.author}'

    class Meta:
        verbose_name = "recipe"
        verbose_name_plural = "recipes"


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   related_name='amount',
                                   verbose_name='ingredient amount')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='amount',
                               verbose_name='recipe amount')
    amount = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        verbose_name = "recipe ingredient"
        verbose_name_plural = "recipe ingredients"


class FavoriteRecipeManager(models.Manager):

    @staticmethod
    def favorite_recipe(user, tags):
        favorite = FavoriteRecipe.objects.filter(user=user)
        recipes_id = favorite.values_list('recipe', flat=True)
        favorite_list = Recipe.objects.tag_filter(tags).filter(
            pk__in=recipes_id).order_by('-pub_date')
        return favorite_list

    class Meta:
        verbose_name = "favorite recipe manager"
        verbose_name_plural = "favorite recipe managers"


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='favorites',
                             verbose_name='users favorite')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='favorites',
                               verbose_name='favorite recipes')

    objects = FavoriteRecipeManager()

    def __str__(self):
        return f'{self.pk} - {self.user} - {self.recipe}'

    class Meta:
        verbose_name = "favorite recipe"
        verbose_name_plural = "favorite recipes"


class SubscriptionManager(models.Manager):

    @staticmethod
    def subscriptions(user):
        sub_obj = Subscription.objects.filter(user=user)
        author_id = sub_obj.values_list('author', flat=True)
        subscriptions_list = User.objects.filter(pk__in=author_id)
        return subscriptions_list

    class Meta:
        verbose_name = "subscription manager"
        verbose_name_plural = "subscription managers"


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower',
                             verbose_name='user follower')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following',
                               verbose_name='following user')

    objects = SubscriptionManager()

    def __str__(self):
        return f'{self.pk} - {self.user} - {self.author}'

    class Meta:
        verbose_name = "subscription"
        verbose_name_plural = "subscriptions"


class ShoppingListManager(models.Manager):

    @staticmethod
    def shopping_cart(user):
        shop_obj = ShoppingList.objects.filter(user=user)
        recipes_id = shop_obj.values_list('recipe', flat=True)
        cart = Recipe.objects.filter(pk__in=recipes_id)
        return cart

    class Meta:
        verbose_name = "shopping list manager"
        verbose_name_plural = "shopping list managers"


class ShoppingList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='buyer')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               verbose_name='buyer recipe')
    objects = ShoppingListManager()

    def __str__(self):
        return f'{self.pk} - {self.user} - {self.recipe}'

    class Meta:
        verbose_name = "shopping list"
        verbose_name_plural = "shopping lists"
