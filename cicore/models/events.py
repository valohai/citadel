import ulid2
from django.db import models


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=ulid2.generate_ulid_as_uuid, editable=False)
    ctime = models.DateTimeField(auto_now_add=True, editable=False)
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name
