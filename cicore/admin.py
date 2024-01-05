from django.contrib import admin
from django.forms.utils import flatatt
from django.urls import reverse
from django.utils.safestring import mark_safe

from cicore.models import Asset, Entry, Event, Round


class AssetInline(admin.TabularInline):
    model = Asset


def format_link(url):
    attrs = {
        "href": url,
        "target": "_blank",
    }
    return mark_safe(
        "<a{}>{}</a>".format(
            flatatt(attrs),
            url,
        ),
    )


class RoundAdmin(admin.ModelAdmin):
    inlines = [AssetInline]
    list_display = (
        "id",
        "event",
        "name",
        "is_visible",
        "accepting_entries",
        "accepting_votes",
        "editor_url",
        "show_url",
        "timer_url",
        "vote_url",
        "results_url",
    )
    list_filter = (
        "event",
        "is_visible",
        "accepting_entries",
        "accepting_votes",
    )

    def editor_url(self, instance):
        if instance.accepting_entries:
            url = reverse("round-editor", kwargs={"slug": instance.slug})
            return format_link(url)
        return ""

    def timer_url(self, instance):
        if instance.accepting_entries:
            url = reverse("round-timer", kwargs={"pk": instance.pk})
            return format_link(url)
        return ""

    def vote_url(self, instance):
        if instance.accepting_votes:
            url = reverse("round-vote", kwargs={"slug": instance.slug})
            return format_link(url)
        return ""

    def show_url(self, instance):
        if not instance.accepting_entries:
            url = reverse("round-show", kwargs={"slug": instance.slug})
            return format_link(url)
        return ""

    def results_url(self, instance):
        if not instance.accepting_entries and not instance.accepting_votes:
            url = reverse("round-results", kwargs={"slug": instance.slug})
            return format_link(url)
        return ""


class EntryAdmin(admin.ModelAdmin):
    readonly_fields = (
        "round",
        "id",
        "code",
    )
    list_display = (
        "id",
        "ctime",
        "round",
        "contestant_name",
    )
    list_filter = ("round",)

    def has_add_permission(self, request):
        return False


admin.site.register(Event)
admin.site.register(Entry, EntryAdmin)
admin.site.register(Round, RoundAdmin)
