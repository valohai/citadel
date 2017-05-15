import base64
import time
from collections import Counter

import qrcode
import ulid2
from django.db.models import Count
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DetailView
from io import BytesIO
from ipware.ip import get_ip
from ranking import Ranking

from cicore.models import Round
from civote.models import Vote


class RoundShowView(DetailView):
    model = Round
    template_name = 'show.html'
    context_object_name = 'round'
    queryset = Round.objects.filter(is_visible=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vote_url = self.request.build_absolute_uri(reverse('round-vote', kwargs={'slug': self.object.slug}))
        qr_img = qrcode.make(vote_url, border=0)
        io = BytesIO()
        qr_img.save(io, format='png')
        context['vote_url'] = vote_url
        context['vote_url_qr_image'] = 'data:image/png;base64,%s' % base64.b64encode(io.getvalue()).decode('ascii')
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.accepting_entries:
            return HttpResponse('Show mode is not available when the round is still accepting entries')
        entry_id = request.GET.get('entry')
        if entry_id:
            entry = self.object.entries.get(id=entry_id)
            return HttpResponse(entry.code, content_type='text/html')
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class RoundVoteView(DetailView):
    model = Round
    template_name = 'vote.html'
    context_object_name = 'round'
    queryset = Round.objects.filter(is_visible=True, accepting_entries=False, accepting_votes=True)

    # TODO: Could this be easily made more secure?

    def get_vote_cookie_name(self):
        return 'v_%s' % ulid2.encode_ulid_base32(self.object.pk.bytes)

    def get_context_data(self, **kwargs):
        context = super(RoundVoteView, self).get_context_data(**kwargs)
        context['voted'] = self.has_voted()
        return context

    def has_voted(self):
        cookie_name = self.get_vote_cookie_name()
        voted = bool(self.request.COOKIES.get(cookie_name))
        return voted

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.has_voted():
            entry_id = request.POST['entry']
            entry = self.object.entries.get(id=entry_id)
            Vote.objects.create(
                round=entry.round,
                entry=entry,
                ip=get_ip(request),
                user_agent=(request.META.get('HTTP_USER_AGENT') or ''),
            )
        resp = HttpResponseRedirect(self.request.path)
        resp.set_cookie(self.get_vote_cookie_name(), str(time.time()))
        return resp


class RoundResultsView(DetailView):
    model = Round
    template_name = 'results.html'
    context_object_name = 'round'
    queryset = Round.objects.filter(is_visible=True, accepting_entries=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.object.accepting_votes:
            context['results'] = self.calculate_results(self.object)
        return context

    def calculate_results(self, round):
        entries = list(round.entries.all())
        votes_by_entry_id = dict(
            round.votes
                .values('entry')
                .annotate(count=Count('id'))
                .values_list('entry', 'count')
        )
        detail = [
            {
                'entry': entry,
                'votes': votes_by_entry_id.get(entry.id, 0),
            }
            for entry
            in entries
        ]
        votes_to_rank = {
            score: rank
            for (rank, score)
            in Ranking(sorted(votes_by_entry_id.values(), reverse=True), start=1)
        }
        for detail_entry in detail:
            detail_entry['rank'] = votes_to_rank.get(detail_entry['votes'], None)
        detail.sort(key=lambda detail_entry: detail_entry['votes'], reverse=True)


        return {
            'n_votes': round.votes.count(),
            'detail': detail,
        }
