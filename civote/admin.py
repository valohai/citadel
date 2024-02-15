from django.contrib import admin

from civote.models import Vote


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "round",
        "entry",
        "ip",
        "user_agent",
        "ctime",
    )
    list_filter = (
        "round",
        "entry",
    )
    readonly_fields = (
        "id",
        "round",
        "entry",
        "ip",
        "user_agent",
        "ctime",
    )

    def has_add_permission(self, request):
        return False
