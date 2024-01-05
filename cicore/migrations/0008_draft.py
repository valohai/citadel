# Generated by Django 5.0.1 on 2024-01-05 22:33

import django.db.models.deletion
import ulid2
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cicore", "0007_round_accepting_votes"),
    ]

    operations = [
        migrations.CreateModel(
            name="Draft",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=ulid2.generate_ulid_as_uuid,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("ctime", models.DateTimeField(auto_now_add=True)),
                ("contestant_name", models.CharField(max_length=128)),
                ("nonce", models.CharField(editable=False, max_length=64)),
                ("code", models.TextField()),
                (
                    "round",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="drafts",
                        to="cicore.round",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "drafts",
            },
        ),
    ]
