import os

from django.contrib.auth.models import User
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.filter(is_superuser=True).exists():
            password = os.environ.get("ADMIN_PASSWORD", "totoro")
            user = User.objects.create_superuser("admin", "admin@example.com", password=password)
            self.stdout.write(self.style.SUCCESS(f"Superuser {user.username!r} created with password {password!r}"))
