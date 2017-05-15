import ulid2
from django.db import models


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=ulid2.generate_ulid_as_uuid)
    ctime = models.DateTimeField(auto_now_add=True, editable=False)
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Round(models.Model):
    id = models.UUIDField(primary_key=True, default=ulid2.generate_ulid_as_uuid)
    ctime = models.DateTimeField(auto_now_add=True, editable=False)
    event = models.ForeignKey(Event, related_name='rounds')
    number = models.PositiveIntegerField()
    name = models.CharField(max_length=128)
    screenshot = models.ImageField(upload_to='rounds', blank=True)

    class Meta:
        unique_together = (('event', 'number'),)
        ordering = ('event', 'number')

    def __str__(self):
        return '{} – {}: {}'.format(self.event.name, self.number, self.name)


class Asset(models.Model):
    id = models.UUIDField(primary_key=True, default=ulid2.generate_ulid_as_uuid)
    ctime = models.DateTimeField(auto_now_add=True, editable=False)
    round = models.ForeignKey(Round, related_name='assets')
    name = models.CharField(max_length=128)
    file = models.FileField(upload_to='rounds/assets')


class Entry(models.Model):
    id = models.UUIDField(primary_key=True, default=ulid2.generate_ulid_as_uuid)
    ctime = models.DateTimeField(auto_now_add=True, editable=False)
    round = models.ForeignKey(Round, related_name='entries')
    contestant_name = models.CharField(max_length=128)
    code = models.TextField()
