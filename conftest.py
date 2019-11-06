import pytest

from cicore.models import Event


@pytest.fixture
@pytest.mark.django_db
def test_event():
    event = Event.objects.create(name='test')
    event.rounds.create(name='round one', slug='one', number=1)
    event.rounds.create(name='round two', slug='two', number=2)
    return event
