from django.urls import re_path
from django.views.decorators.csrf import csrf_exempt

from cifront.views import AssetRedirectView, RoundEditorView, RoundInstructionsView, RoundSaveView, RoundTimerView

urlpatterns = [
    re_path(r"^e/(?P<slug>.+?)/$", RoundEditorView.as_view(), name="round-editor"),
    re_path(r"^i/(?P<pk>.+?)/$", RoundInstructionsView.as_view(), name="round-instructions"),
    re_path(r"^timer/(?P<pk>.+?)/$", RoundTimerView.as_view(), name="round-timer"),
    re_path(r"^a/(?P<round_slug>.+?)/(?P<asset_name>.+?)/*$", AssetRedirectView.as_view(), name="asset-redirect"),
    re_path(r"^save/(?P<pk>.+?)/$", csrf_exempt(RoundSaveView.as_view()), name="round-save"),
]
