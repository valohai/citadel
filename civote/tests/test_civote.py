import pytest
from django.shortcuts import resolve_url

from civote.tests.utils import finish_round


@pytest.mark.django_db
def test_show_view(test_event, client):
    round = finish_round(test_event)
    resp = client.get(resolve_url('round-show', slug=round.slug))
    assert resp.status_code == 200


@pytest.mark.django_db
def test_vote_view(test_event, client):
    round = finish_round(test_event)
    resp = client.get(resolve_url('round-vote', slug=round.slug))
    assert resp.status_code == 200


@pytest.mark.django_db
def test_results_view(test_event, client):
    round = finish_round(test_event)
    resp = client.get(resolve_url('round-results', slug=round.slug))
    assert resp.status_code == 200
