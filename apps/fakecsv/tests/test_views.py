import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

from apps.fakecsv.models import Schema


# Tests login-logout 


@pytest.mark.django_db
def test_user_login(client, create_test_user, user_data):
    url = reverse('fakecsv:login')
    response = client.post(url, user_data)
    assert response.status_code == 302


@pytest.mark.django_db
def test_user_logout(client):
    url = reverse('fakecsv:logout')
    response = client.get(url)
    assert response.status_code == 302


# End tests login-logout


# Tests schema views


def test_list_view_no_login(client):
    url = reverse('fakecsv:schema_list')
    response = client.get(url)
    assert response.status_code == 302


def test_create_schema_view_no_login(client):
    url = reverse('fakecsv:create_schema')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_list_view_login(client, authenticated_user):
    user = authenticated_user
    url = reverse('fakecsv:schema_list')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_schema_view_login(client, authenticated_user):
    url = reverse('fakecsv:create_schema')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_schema_view_post(authenticated_user, schema_data):
    url = reverse('fakecsv:create_schema')
    assert Schema.objects.count() == 0
    response = authenticated_user.post(url, data=schema_data)
    assert response.status_code == 302
    assert Schema.objects.count() == 1


# End tests schema views
