import random

from django.core.management import BaseCommand

from cicore.models import Round


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=15)
        parser.add_argument("round")

    def handle(self, round, count, **options):
        round = Round.objects.get(slug=round)
        entries = round.entries.all()
        for i in range(count):
            round.votes.create(
                entry=random.choice(entries),
                ip="0.0.0.0",
                user_agent="fake",
            )
        self.stdout.write(f"OK. {round.votes.count()} votes now.")
