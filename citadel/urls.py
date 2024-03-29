from unittest.mock import patch

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView

urlpatterns = [
    re_path(r"^admin/", admin.site.urls),
    path("", include("cifront.urls")),
    path("", include("civote.urls")),
    path("", TemplateView.as_view(template_name="index.html")),
    re_path(r"^404.html$", TemplateView.as_view(template_name="404.html")),
]

# `static` refuses to do anything if we're not `DEBUG`ging; static serving is
# discouraged for production use – it should be safe enough for something of
# Citadel's scope, so if the `settings.SERVE_MEDIA` flag is set, we'll serve
# it anyway.
with patch("django.conf.settings.DEBUG", (settings.DEBUG or settings.SERVE_MEDIA)):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
