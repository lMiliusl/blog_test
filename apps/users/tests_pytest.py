import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestUserAPI:
    
    def test_register_success(self, api_client):
        response = api_client.post("/users/register", json = {
            'username': 'newuser',
            'password': 'newuser',
            'email': 'newuser@mail.com'
        })

        assert response.status_code == 200
        data = response.json()
        assert 'token' in data
        assert data['user']['username'] == 'newuser'

        assert User.objects.filter(username='newuser').exists()

    def test_login_success(self, api_client, test_user):
        response = api_client.post('/users/login', json = {
            'username': test_user.username,
            'password': 'newuser'
        })

        assert response.status_code == 200
        data = response.json()
        assert 'token' in data
        assert data['user']['username'] == test_user.username

    def test_login_wrong_password(sefl, api_client, test_user):
        response = api_client.post('/users/login', json = {
            'username': test_user.username,
            'password': 'usernew'
        })

        assert response.status_code == 401
        assert 'error' in response.json()

    def test_get_me_authenticated(sefl, api_client, auth_headers, test_user):
        response = api_client.post('/users/me', headers = auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data['username'] == test_user.username
        assert data['email'] == test_user.email

    def test_get_me_unauthenticated(self, api_client):
        response = api_client.get('/users/me')

        assert response.status_code == 401

    def test_logout(self, api_client, auth_headers, test_user):
        response = api_client.post('/users/logout', headers = auth_headers)

        assert response.status_code == 200
        assert response.json()['success'] is True

        test_user.refresh_from_db()
        assert test_user.token is None