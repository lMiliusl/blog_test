import pytest
from apps.articles.models import Article, Category

@pytest.mark.django_db
class TestArticlesAPI:

    def test_list_articles(self, api_client, test_article):
        response = api_client.get('/api/articles/articles')

        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert data[0]['title'] == 'Test Article'

    def test_get_article_detail(self, api_client, test_article):
        response = api_client.get(f'/api/articles/articles/{test_article.id}')

        assert response.status_code == 200
        data = response.json()
        assert data['title'] == 'Test Article'
        assert data['author_name'] == 'test'

    def test_create_article_success(self, api_client, auth_headers, test_category):
        response = api_client.post(
            '/api/articles/articles',
            json = {
                'title': 'New Article',
                'content': 'New Content',
                'category_id': test_category.id
                },
            headers = auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data['title'] == 'New Article'
        assert data['author_name'] == 'test'
        assert Article.objects.filter(title='New Article').exists()

    def test_create_article_unauthenticated(self, api_client, test_category):
        response = api_client.post(
             "/api/articles/articles",
            json = {
                'title': 'New Article',
                'content': 'New Content',
                'category_id': test_category.id 
            }
        )

        assert response.status_code == 401

    def test_update_article_as_author(self, api_client, auth_headers, test_article):
        response = api_client.put(
            f'/api/articles/articles/{test_article.id}',
            json = {'title': 'Updated Title'},
            headers = auth_headers
        )

        assert response.status_code == 200
        assert response.json()['title'] == 'Updated Title'

        test_article.refresh_from_db()
        assert test_article.title == 'Updated Title'

    
    def test_update_article_as_non_author(self, api_client, another_auth_headers, test_article):
            response = api_client.put(
                f'/api/articles/articles/{test_article.id}',
                json = {'title': 'Updated Title'},
                headers = another_auth_headers
            )

            assert response.status_code == 403
            assert 'error' in response.json()

    def test_delete_article_as_author(self, api_client, auth_headers, test_article):
         article_id = test_article.id
         response = api_client.delete(
              f'/api/articles/articles/{article_id}',
              headers = auth_headers
         )

         assert response.status_code == 200
         assert response.json()['success'] is True

         assert not Article.objects.filter(id = article_id).exists()

    def test_delete_article_as_non_author(self, api_client, another_auth_headers, test_article):
         article_id = test_article.id
         response = api_client.delete(
              f'/api/articles/articles/{article_id}',
              headers = another_auth_headers
         )

         assert response.status_code == 403
         assert Article.objects.filter(id=article_id).exists()
         