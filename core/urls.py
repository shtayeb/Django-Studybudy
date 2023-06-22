
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('accounts/', include('accounts.urls')),
    path('api/', include('base.api.urls')),

    path("__debug__/", include("debug_toolbar.urls")),
    path('accounts/', include('allauth.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
