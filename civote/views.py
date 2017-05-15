from django.http.response import HttpResponse
from django.views.generic import DetailView

from cicore.models import Round


class RoundShowView(DetailView):
    model = Round
    template_name = 'show.html'
    context_object_name = 'round'
    queryset = Round.objects.filter(is_visible=True)

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
