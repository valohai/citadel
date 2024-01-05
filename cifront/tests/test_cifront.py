import pytest
from django.shortcuts import resolve_url


@pytest.mark.django_db
def test_editor_view(test_event, client):
    resp = client.get(resolve_url("round-editor", slug=test_event.rounds.first().slug))
    assert resp.status_code == 200


@pytest.mark.django_db
def test_instructions_view(test_event, client):
    resp = client.get(resolve_url("round-instructions", pk=test_event.rounds.first().pk))
    assert resp.status_code == 200


@pytest.mark.django_db
def test_timer_view(test_event, admin_client):
    resp = admin_client.get(resolve_url("round-timer", pk=test_event.rounds.first().pk))
    assert resp.status_code == 200
