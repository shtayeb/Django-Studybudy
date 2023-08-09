from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView

urlpatterns = [
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    path("admin/", admin.site.urls),
    path("", include("base.urls")),
    path("accounts/", include("accounts.urls")),
    path("api/", include("base.api.urls")),
    # Installed apps
    path("invitations/", include("invitations.urls", namespace="invitations")),
    path("__debug__/", include("debug_toolbar.urls")),
    path(r'mdeditor/', include('mdeditor.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
