import ulid2
from django.db import models


class Entry(models.Model):
    id = models.UUIDField(primary_key=True, default=ulid2.generate_ulid_as_uuid, editable=False)
    ctime = models.DateTimeField(auto_now_add=True, editable=False)
    round = models.ForeignKey("cicore.Round", related_name="entries", on_delete=models.CASCADE)
    contestant_name = models.CharField(max_length=128)
    nonce = models.CharField(max_length=64, unique=True, editable=False)
    code = models.TextField()

    class Meta:
        verbose_name_plural = "entries"
