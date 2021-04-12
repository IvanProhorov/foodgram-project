from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from . import views

handler404 = 'foodgram.views.page_not_found'  # noqa
handler500 = 'foodgram.views.server_error'  # noqa

urlpatterns = [
    path('admin/', admin.site.urls),

    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('api/', include('api.urls')),
    path('favicon/ico', RedirectView.as_view(
        url='/static/images/favicon.ico'), name='favicon'),
    path('about/author', views.FoodgramAuthorView.as_view(), name='author'),
    path('about/technologies', views.FoodgramTechnologiesView.as_view(),
         name='technologies'),
    path('', include('recipes.urls')),
]
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
