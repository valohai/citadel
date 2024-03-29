import json
from datetime import timedelta

import jwt
from django.conf import settings
from django.contrib.staticfiles.finders import find as find_staticfile
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.http.response import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.encoding import force_str
from django.utils.safestring import mark_safe
from django.utils.timezone import now
from django.views.generic import DetailView

from cicore.models import Asset, Draft, Entry, Round
from cicore.utils import make_qr_code_data_uri
from citadel.view_mixins import PKOrSlugDetailView

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


class RoundEditorView(PKOrSlugDetailView):
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


class RoundInstructionsView(PKOrSlugDetailView):
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


class RoundSaveView(PKOrSlugDetailView):
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


class RoundTimerView(PKOrSlugDetailView):
    model = Round
    template_name = "timer.html"
    context_object_name = "round"
    queryset = Round.objects.filter(is_visible=True)

    def get(self, request, *args, **kwargs):
        self.object: Round = self.get_object()
        if not self.object.accepting_entries:
            return HttpResponseNotFound("Sorry! This round is not accepting entries at present.")
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["edit_url"] = edit_url = self.object.get_edit_url(self.request)
        context["show_url"] = self.object.get_show_url(self.request)
        context["results_url"] = self.object.get_results_url(self.request)
        context["edit_url_qr_image"] = make_qr_code_data_uri(edit_url)
        context["screenshot_url"] = self.object.screenshot.url if self.object.screenshot else None
        return context


class RoundProgressView(PKOrSlugDetailView):
    model = Round
    context_object_name = "round"
    queryset = Round.objects.filter(is_visible=True)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        # We need to do some gentle extra shenanigans to get the latest draft per team
        # in the absence of `DISTINCT OF` (SQLite, MySQL, etc).
        newest_draft_id_per_team = dict(
            Draft.objects.filter(round=self.object)
            .values("contestant_name")
            .annotate(newest_id=models.Max("id"))  # is fine because of ULIDs
            .values_list("newest_id", "contestant_name"),
        )
        data = {
            "latestDrafts": [
                {
                    "code": draft.code,
                    "contestantName": draft.contestant_name,
                    "ctime": draft.ctime.isoformat(),
                    "id": str(draft.id),
                    "nonce": draft.nonce,
                }
                for draft in Draft.objects.filter(id__in=newest_draft_id_per_team)
            ],
        }
        return JsonResponse(data)
