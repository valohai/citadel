from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DetailView

from cicore.models import Asset, Round


class RoundEditorView(DetailView):
    model = Round
    template_name = 'editor.html'
    context_object_name = 'round'

    def get_context_data(self, **kwargs):
        context = super(RoundEditorView, self).get_context_data(**kwargs)
        context['instructions_url'] = reverse('round-instructions', kwargs={'pk': self.object.pk})
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
