from django.contrib import admin
from django.db import models
from django.forms.utils import flatatt
from django.utils.safestring import mark_safe

from cicore.models import Asset, Draft, Entry, Event, Round


class AssetInline(admin.TabularInline):
    model = Asset


def format_link(url, name):
    attrs = {
        "href": url,
        "target": "_blank",
    }
    return mark_safe(f"<a{flatatt(attrs)}>{name}</a>")


@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    inlines = [AssetInline]
    list_display = (
        "id",
        "event",
        "name",
        "is_visible",
        "accepting_entries",
        "accepting_votes",
        "n_votes",
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

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .annotate(
                n_votes=models.Count("votes"),
            )
        )

    def n_votes(self, instance: Round):
        return getattr(instance, "n_votes", None)

    def editor_url(self, instance: Round):
        return format_link(instance.get_edit_url(), "Edit")

    def timer_url(self, instance: Round):
        return format_link(instance.get_timer_url(), "Timer")

    def vote_url(self, instance: Round):
        return format_link(instance.get_vote_url(), "Vote")

    def show_url(self, instance: Round):
        return format_link(instance.get_show_url(), "Show")

    def results_url(self, instance: Round):
        return format_link(instance.get_results_url(), "Results")


@admin.register(Entry)
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


@admin.register(Draft)
class DraftAdmin(EntryAdmin):
    pass


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass
