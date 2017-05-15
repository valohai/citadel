from datetime import timedelta

import jwt
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.timezone import now
from django.views.generic import DetailView

from cicore.models import Asset, Entry, Round


class RoundEditorView(DetailView):
    model = Round
    template_name = 'editor.html'
    context_object_name = 'round'

    def get_context_data(self, **kwargs):
        context = super(RoundEditorView, self).get_context_data(**kwargs)
        context['instructions_url'] = reverse('round-instructions', kwargs={'pk': self.object.pk})
        context['save_url'] = reverse('round-save', kwargs={'pk': self.object.pk})
        context['save_token'] = jwt.encode(
            payload={
                'nbf': now(),
                'exp': now() + timedelta(hours=1),
                'nonce': get_random_string(),
            },
            key=settings.JWT_KEY,
        )
        return context


class RoundInstructionsView(DetailView):
    model = Round
    template_name = 'instructions.html'
    context_object_name = 'round'


class AssetRedirectView(DetailView):
    model = Asset

    def get_object(self, queryset=None):
        return Asset.objects.get(round__slug=self.kwargs['round_slug'], name=self.kwargs['asset_name'])

    def dispatch(self, request, *args, **kwargs):
        try:
            asset = self.get_object()
            return HttpResponseRedirect(asset.file.url)
        except ObjectDoesNotExist:
            return HttpResponseNotFound('asset not found')


class RoundSaveView(DetailView):
    model = Round

    def get(self, request, *args, **kwargs):
        return HttpResponseNotFound('GET not allowed')

    def post(self, request, *args, **kwargs):
        token = jwt.decode(
            jwt=request.POST['token'],
            key=settings.JWT_KEY,
        )
        self.object = self.get_object()
        entry = Entry.objects.create(
            round=self.object,
            code=request.POST['code'],
            contestant_name=request.POST['author'],
            nonce=token['nonce'],
        )
        return JsonResponse({'id': entry.id}, status=201)