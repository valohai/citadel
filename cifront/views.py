import json
from datetime import timedelta

import jwt
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.staticfiles.finders import find as find_staticfile
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.encoding import force_str
from django.utils.safestring import mark_safe
from django.utils.timezone import now
from django.views.generic import DetailView

from cicore.models import Asset, Draft, Entry, Round
from cicore.utils import make_qr_code_data_uri

RULES_HTML = """
<ol>
    <li>No previews - of either results or assets!</li>
    <li>Stay in this editor at all times</li>
    <li>No measurement tools</li>
    <li>Stop coding when the time's up</li>
    <li>After the round is over, press "Finish" and follow the prompt instructions to see your results</li>
</ol>
Good luck and most important of all; have fun!
""".strip()


class RoundEditorView(DetailView):
    object: Round

    model = Round
    context_object_name = "round"
    queryset = Round.objects.filter(is_visible=True)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.accepting_entries:
            return HttpResponseNotFound("Sorry! This round is no longer accepting entries.")
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["citd_config"] = self.get_citd_config()
        return context

    def get_citd_config(self):
        save_token = force_str(
            jwt.encode(
                payload={
                    "nbf": now(),
                    "exp": now() + timedelta(hours=1),
                    "nonce": get_random_string(length=12),
                },
                key=settings.JWT_KEY,
                algorithm="HS256",
            ),
        )
        assets = [
            {
                "url": asset.short_url,
                "name": asset.name,
                "description": asset.description,
            }
            for asset in self.object.assets.all()
        ]
        return {
            "assets": assets,
            "instructionsUrl": reverse("round-instructions", kwargs={"pk": self.object.pk}),
            "referenceImage": self.object.screenshot.url if self.object.screenshot else None,
            "roundId": self.object.slug,
            "rules": RULES_HTML,
            "saveToken": save_token,
            "saveUrl": reverse("round-save", kwargs={"pk": self.object.pk}),
        }

    def render_to_response(self, context, **response_kwargs):
        file_path = find_staticfile("editor/index.html")
        with open(file_path) as f:
            html = f.read()
        config_json = json.dumps(context["citd_config"], default=str)
        html = html.replace("<head>", f"<head><script>window.CODE_IN_THE_DARK_CONFIGURATION = {config_json};</script>")
        return HttpResponse(html)


class RoundInstructionsView(DetailView):
    model = Round
    template_name = "instructions.html"
    context_object_name = "round"
    queryset = Round.objects.filter(is_visible=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["rules_html"] = mark_safe(RULES_HTML)


class AssetRedirectView(DetailView):
    model = Asset

    def get_object(self, queryset=None):
        return Asset.objects.get(round__slug=self.kwargs["round_slug"], name=self.kwargs["asset_name"])

    def dispatch(self, request, *args, **kwargs):
        try:
            asset = self.get_object()
            return HttpResponseRedirect(asset.file.url)
        except ObjectDoesNotExist:
            return HttpResponseNotFound("asset not found")


class RoundSaveView(DetailView):
    model = Round

    def get(self, request, *args, **kwargs):
        return HttpResponseNotFound("GET not allowed")

    def post(self, request, *args, **kwargs):
        token = jwt.decode(
            jwt=request.POST["token"],
            key=settings.JWT_KEY,
            algorithms=["HS256"],
        )
        self.object = self.get_object()
        if not self.object.accepting_entries:
            return JsonResponse({"error": "not accepting entries"}, status=403)
        mode = request.POST.get("mode")
        code = request.POST["content"]
        kw = {
            "round": self.object,
            "contestant_name": request.POST["author"],
            "nonce": token["nonce"],
        }
        if mode == "draft":
            last_draft = Draft.objects.filter(**kw).order_by("ctime").last()
            if last_draft and last_draft.code == code:
                return JsonResponse({}, status=204)
            obj = Draft.objects.create(**kw, code=code)
        elif mode == "final":
            obj = Entry.objects.create(**kw, code=code)
        else:
            return JsonResponse({"error": f"invalid mode {mode!r}"}, status=400)
        return JsonResponse({"id": obj.id, "mode": mode}, status=201)


class RoundTimerView(LoginRequiredMixin, DetailView):
    model = Round
    template_name = "timer.html"
    context_object_name = "round"
    queryset = Round.objects.filter(is_visible=True)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.accepting_entries:
            return HttpResponseNotFound("Sorry! This round is not accepting entries at present.")
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        edit_url = self.request.build_absolute_uri(reverse("round-editor", kwargs={"slug": self.object.slug}))
        context["edit_url"] = edit_url
        context["edit_url_qr_image"] = make_qr_code_data_uri(edit_url)
        return context
