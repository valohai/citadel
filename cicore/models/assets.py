import ulid2
from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property


class Asset(models.Model):
    id = models.UUIDField(primary_key=True, default=ulid2.generate_ulid_as_uuid, editable=False)
    ctime = models.DateTimeField(auto_now_add=True, editable=False)
    round = models.ForeignKey("cicore.Round", related_name="assets", on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    file = models.FileField(upload_to="rounds/assets")
    description = models.TextField(blank=True)

    class Meta:
        unique_together = (
            "round",
            "name",
        )
        ordering = ("name",)

    @cached_property
    def short_url(self):
        return reverse(
            "asset-redirect",
            kwargs={
                "round_slug": self.round.slug,
                "asset_name": self.name,
            },
        )
