from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from civote.views import RoundResultsView, RoundShowView, RoundVoteView, VoteRedirectView

urlpatterns = [
    url(r'^show/(?P<slug>.+?)/$', RoundShowView.as_view(), name='round-show'),
    url(r'^vote/(?P<slug>.+?)/$', csrf_exempt(RoundVoteView.as_view()), name='round-vote'),
    url(r'^vote/?$', VoteRedirectView.as_view(), name='vote-redirect'),
    url(r'^results/(?P<slug>.+?)/$', RoundResultsView.as_view(), name='round-results'),
]
