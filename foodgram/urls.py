from django.conf import settings
from django.contrib import admin
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from django.urls import path, include
from . import views

handler404 = 'recipes.views.page_not_found'  # noqa
handler500 = 'recipes.views.server_error'  # noqa

urlpatterns = [
    path('admin/', admin.site.urls),

    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),

    path('api/', include('api.urls')),

    path('about/author', views.FoodgramAuthorView.as_view(), name='author'),
    path('about/technologies', views.FoodgramTechnologiesView.as_view(),
         name='technologies'),
    path('', include('recipes.urls'))
]
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)