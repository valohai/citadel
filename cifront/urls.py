from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from cifront.views import AssetRedirectView, RoundEditorView, RoundInstructionsView, RoundSaveView, RoundTimerView

urlpatterns = [
    url(r'^e/(?P<slug>.+?)/$', RoundEditorView.as_view(), name='round-editor'),
    url(r'^i/(?P<pk>.+?)/$', RoundInstructionsView.as_view(), name='round-instructions'),
    url(r'^timer/(?P<pk>.+?)/$', RoundTimerView.as_view(), name='round-timer'),
    url(r'^a/(?P<round_slug>.+?)/(?P<asset_name>.+?)/*$', AssetRedirectView.as_view(), name='asset-redirect'),
    url(r'^save/(?P<pk>.+?)/$', csrf_exempt(RoundSaveView.as_view()), name='round-save'),
]
