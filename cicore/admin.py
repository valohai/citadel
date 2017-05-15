from django.contrib import admin

from cicore.models import Asset, Entry, Event, Round


class AssetInline(admin.TabularInline):
    model = Asset


class RoundAdmin(admin.ModelAdmin):
    inlines = [AssetInline]


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
