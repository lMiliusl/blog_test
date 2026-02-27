import pytest
from django.contrib.auth import get_user_model
from ninja.testing import TestClient
from config.api import api
from apps.articles.models import Category, Article
from apps.comments.models import Comment

User = get_user_model()

@pytest.fixture(scope='session')
def api_client():
    return TestClient(api)

@pytest.fixture
def test_user():
    user = User.objects.create_user(
     username = 'test',
     password = 'test',
     email = 'test@mail.com'   
    )
    user.generate_token()
    return user

@pytest.fixture
def another_user():
    user = User.objects.create_user(
     username = 'user',
     password = 'user',
     email = 'user@mail.com'   
    )
    user.generate_token()
    return user

@pytest.fixture
def test_category():
    return Category.objects.create(
        name = 'Test Category',
        description = 'Test Description'
    )

@pytest.fixture
def test_article(test_user, test_category):
    return Article.objects.create(
        title = 'Test Article',
        content = 'Test Content',
        author = test_user,
        category = test_category
    )

@pytest.fixture
def test_comment(db, test_user, test_article):
    return Comment.objects.create(
        content = 'Test Comment',
        author = test_user,
        article = test_article
    )

@pytest.fixture
def auth_headers(test_user):
    return {'Authorization': f'Bearer {test_user.token}'}

@pytest.fixture
def another_auth_headers(another_user):
    return{'Authorization': f'Bearer {another_user.token}'}