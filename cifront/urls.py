from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from cifront.views import RoundEditorView, RoundInstructionsView, AssetRedirectView, RoundSaveView

urlpatterns = [
    url(r'^e/(?P<slug>.+?)/$', RoundEditorView.as_view(), name='round-editor'),
    url(r'^i/(?P<pk>.+?)/$', RoundInstructionsView.as_view(), name='round-instructions'),
    url(r'^a/(?P<round_slug>.+?)/(?P<asset_name>.+?)/*$', AssetRedirectView.as_view(), name='asset-redirect'),
    url(r'^save/(?P<pk>.+?)/$', csrf_exempt(RoundSaveView.as_view()), name='round-save'),
]
