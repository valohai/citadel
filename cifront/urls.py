from django.conf.urls import url

from cifront.views import RoundEditorView, RoundInstructionsView, AssetRedirectView

urlpatterns = [
    url(r'^e/(?P<slug>.+?)/$', RoundEditorView.as_view(), name='round-editor'),
    url(r'^i/(?P<pk>.+?)/$', RoundInstructionsView.as_view(), name='round-instructions'),
    url(r'^a/(?P<round_slug>.+?)/(?P<asset_name>.+?)/*$', AssetRedirectView.as_view(), name='asset-redirect'),
]
