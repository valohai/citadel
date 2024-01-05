from django.urls import re_path
from django.views.decorators.csrf import csrf_exempt

from civote.views import RoundResultsView, RoundShowView, RoundVoteView, VoteRedirectView

urlpatterns = [
    re_path(r"^show/(?P<slug>.+?)/$", RoundShowView.as_view(), name="round-show"),
    re_path(r"^vote/(?P<slug>.+?)/$", csrf_exempt(RoundVoteView.as_view()), name="round-vote"),
    re_path(r"^vote/?$", VoteRedirectView.as_view(), name="vote-redirect"),
    re_path(r"^results/(?P<slug>.+?)/$", RoundResultsView.as_view(), name="round-results"),
]
