import ulid2
from django.db import models


class Vote(models.Model):
    id = models.UUIDField(primary_key=True, default=ulid2.generate_ulid_as_uuid, editable=False)
    ctime = models.DateTimeField(auto_now_add=True, editable=False)
    round = models.ForeignKey("cicore.Round", related_name="votes", on_delete=models.CASCADE)
    entry = models.ForeignKey("cicore.Entry", related_name="votes", on_delete=models.CASCADE)
    ip = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
