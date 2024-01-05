import ulid2
from django.db import models


class Round(models.Model):
    id = models.UUIDField(primary_key=True, default=ulid2.generate_ulid_as_uuid, editable=False)
    slug = models.SlugField(max_length=64, unique=True)
    ctime = models.DateTimeField(auto_now_add=True, editable=False)
    event = models.ForeignKey("cicore.Event", related_name="rounds", on_delete=models.CASCADE)
    number = models.PositiveIntegerField()
    name = models.CharField(max_length=128)
    screenshot = models.ImageField(upload_to="rounds", blank=True)
    accepting_entries = models.BooleanField(default=True)
    accepting_votes = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=True)

    class Meta:
        unique_together = (("event", "number"),)
        ordering = ("event", "number")

    def __str__(self):
        return f"{self.event.name} – {self.number}: {self.name}"
