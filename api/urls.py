from django.urls import path, include

from .views import (FavoritesView, ShoppingListView, SubscriptionView,
                    ingredients)

api_v1 = [
    path('ingredients/', ingredients, name='get_ingredients'),
    path('favorites/', FavoritesView.as_view(), name='get_favorites'),
    path('favorites/<int:recipe_id>/', FavoritesView.as_view(),
         name='get_favorites_recipe_by_id'),
    path('subscriptions/', SubscriptionView.as_view(),
         name='get_subscriptions'),
    path('subscriptions/<int:author_id>/', SubscriptionView.as_view(),
         name='get_subscriptions_by_id'),
    path('purchases/', ShoppingListView.as_view(), name='get_shopping_list'),
    path('purchases/<int:recipe_id>/', ShoppingListView.as_view(),
         name='get_shopping_list_by_id'),

]
urlpatterns = [
    path('v1/', include(api_v1)),
]
