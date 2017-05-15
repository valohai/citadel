from django.conf.urls import url

from civote.views import RoundShowView

urlpatterns = [
    url(r'^show/(?P<slug>.+?)/$', RoundShowView.as_view(), name='round-show'),
]
