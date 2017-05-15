from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('cifront.urls')),
    url(r'^', include('civote.urls')),
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^404.html$', TemplateView.as_view(template_name='404.html')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
