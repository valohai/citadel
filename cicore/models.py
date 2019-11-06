import ulid2
from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=ulid2.generate_ulid_as_uuid, editable=False)
    ctime = models.DateTimeField(auto_now_add=True, editable=False)
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Round(models.Model):
    id = models.UUIDField(primary_key=True, default=ulid2.generate_ulid_as_uuid, editable=False)
    slug = models.SlugField(max_length=64, unique=True)
    ctime = models.DateTimeField(auto_now_add=True, editable=False)
    event = models.ForeignKey(Event, related_name='rounds', on_delete=models.CASCADE)
    number = models.PositiveIntegerField()
    name = models.CharField(max_length=128)
    screenshot = models.ImageField(upload_to='rounds', blank=True)
    accepting_entries = models.BooleanField(default=True)
    accepting_votes = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=True)

    class Meta:
        unique_together = (('event', 'number'),)
        ordering = ('event', 'number')

    def __str__(self):
        return '{} – {}: {}'.format(self.event.name, self.number, self.name)


class Asset(models.Model):
    id = models.UUIDField(primary_key=True, default=ulid2.generate_ulid_as_uuid, editable=False)
    ctime = models.DateTimeField(auto_now_add=True, editable=False)
    round = models.ForeignKey(Round, related_name='assets', on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    file = models.FileField(upload_to='rounds/assets')
    description = models.TextField(blank=True)

    class Meta:
        unique_together = (('round', 'name',))
        ordering = ('name',)

    @cached_property
    def short_url(self):
        return reverse(
            'asset-redirect',
            kwargs={
                'round_slug': self.round.slug,
                'asset_name': self.name,
            }
        )


class Entry(models.Model):
    id = models.UUIDField(primary_key=True, default=ulid2.generate_ulid_as_uuid, editable=False)
    ctime = models.DateTimeField(auto_now_add=True, editable=False)
    round = models.ForeignKey(Round, related_name='entries', on_delete=models.CASCADE)
    contestant_name = models.CharField(max_length=128)
    nonce = models.CharField(max_length=64, unique=True, editable=False)
    code = models.TextField()

    class Meta:
        verbose_name_plural = 'entries'
