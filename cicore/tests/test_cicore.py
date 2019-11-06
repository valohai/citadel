import pytest
from django.shortcuts import resolve_url

from civote.tests.utils import finish_round


@pytest.mark.django_db
def test_admin(admin_client, test_event):
    finish_round(test_event)
    admin_client.get(resolve_url('admin:cicore_round_changelist'))
