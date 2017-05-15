from django.contrib import admin
from django.forms.utils import flatatt
from django.urls import reverse
from django.utils.safestring import mark_safe

from cicore.models import Asset, Entry, Event, Round


class AssetInline(admin.TabularInline):
    model = Asset


class RoundAdmin(admin.ModelAdmin):
    inlines = [AssetInline]
    list_display = (
        'id',
        'event',
        'name',
        'is_visible',
        'accepting_entries',
        'editor_url',
    )
    list_filter = (
        'event',
        'is_visible',
        'accepting_entries',
    )

    def editor_url(self, instance):
        url = reverse('round-editor', kwargs={'slug': instance.slug})
        attrs = {
            'href': url,
            'target': '_blank',
        }
        return mark_safe('<a{}>{}</a>'.format(
            flatatt(attrs),
            url,
        ))


class EntryAdmin(admin.ModelAdmin):
    readonly_fields = (
        'round',
        'id',
        'contestant_name',
        'code',
    )
    list_display = (
        'id',
        'ctime',
        'round',
        'contestant_name',
    )
    list_filter = (
        'round',
    )

    def has_add_permission(self, request):
        return False


admin.site.register(Event)
admin.site.register(Entry, EntryAdmin)
admin.site.register(Round, RoundAdmin)
