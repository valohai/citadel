# Generated by Django 1.11.1 on 2017-05-15 10:16

import django.db.models.deletion
import ulid2
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Asset",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=ulid2.generate_ulid_as_uuid,
                        primary_key=True,
                        serialize=False,
                        editable=False,
                    ),
                ),
                ("ctime", models.DateTimeField(auto_now_add=True)),
                ("name", models.CharField(max_length=128)),
                ("file", models.FileField(upload_to="rounds/assets")),
            ],
        ),
        migrations.CreateModel(
            name="Entry",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=ulid2.generate_ulid_as_uuid,
                        primary_key=True,
                        serialize=False,
                        editable=False,
                    ),
                ),
                ("ctime", models.DateTimeField(auto_now_add=True)),
                ("contestant_name", models.CharField(max_length=128)),
                ("code", models.TextField()),
            ],
            options={"verbose_name_plural": "entries"},
        ),
        migrations.CreateModel(
            name="Event",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=ulid2.generate_ulid_as_uuid,
                        primary_key=True,
                        serialize=False,
                        editable=False,
                    ),
                ),
                ("ctime", models.DateTimeField(auto_now_add=True)),
                ("name", models.CharField(max_length=128)),
            ],
            options={},
        ),
        migrations.CreateModel(
            name="Round",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=ulid2.generate_ulid_as_uuid,
                        primary_key=True,
                        serialize=False,
                        editable=False,
                    ),
                ),
                ("ctime", models.DateTimeField(auto_now_add=True)),
                ("number", models.PositiveIntegerField()),
                ("name", models.CharField(max_length=128)),
                ("screenshot", models.ImageField(blank=True, upload_to="rounds")),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="rounds",
                        to="cicore.Event",
                    ),
                ),
            ],
            options={
                "ordering": ("event", "number"),
            },
        ),
        migrations.AddField(
            model_name="entry",
            name="round",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="entries",
                to="cicore.Round",
            ),
        ),
        migrations.AddField(
            model_name="asset",
            name="round",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="assets",
                to="cicore.Round",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="round",
            unique_together={("event", "number")},
        ),
    ]
