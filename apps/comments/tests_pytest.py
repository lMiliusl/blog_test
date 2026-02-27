import pytest
from apps.comments.models import Comment

@pytest.mark.django_db
class TestCommentAPI:

    def test_list_comments(self, api_client, test_article, test_comment):
        response = api_client.get(f'/articles/{test_article.id}/comments')

        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert data[0]['content'] == 'Test comment'

    def test_create_comment_seccess(self, api_client, test_article, auth_headers):
        response = api_client.post(
            '/comments',
            json = {
                'content': 'New comment',
                'article_id': test_article.id
            },
            headers = auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data['comment'] == 'New comment'
        assert data['author_name'] == 'user'
        assert Comment.objects.filter(content = 'New comment').exists()

    def test_create_comment_unauthenticated(self, api_client, test_article):
        response = api_client.post(
            '/comments',
            json = {
                'content': 'New comment',
                'article_id': test_article.id
            }
        )

        assert response.status_code == 401

    def test_create_reply_seccess(self, api_client, test_article, auth_headers, test_comment):
        responce = api_client.post(
            '/comments',
            json={
                'content': 'Reply to comment',
                'article_id': test_article.id,
                'parent_id': test_comment.id
            },
            headers = auth_headers
        )

        assert responce.status_code == 200
        data = responce.json()
        assert data['content'] == 'Reply to comment'
        assert data['parent_id'] == test_comment.id

    def test_update_comment_as_author(self, api_client, auth_headers, test_comment):
        responce = api_client.put(
            f'/comments/{test_comment.id}',
            json = {'content': 'Updated comment'},
            headers = auth_headers
        )

        assert responce.status_code == 200
        assert responce.json()['content'] == 'Update comment'
        test_comment.refresh_from_db()
        assert test_comment.content == 'Update comment'

    def test_update_comment_as_non_author(self, api_client, another_auth_headers, test_comment):
        responce = api_client.put(
            f'/comments/{test_comment.id}',
            json = {'content': 'Updated comment'},
            headers = another_auth_headers
        )

        assert responce.status_code == 403
        assert 'error' in responce.json()

    def test_delete_comment_as_author(self, api_client, auth_headers, test_comment):
        comment_id = test_comment.id
        response = api_client.delete(
            f'/comments/{comment_id}',
            headers = auth_headers
        )

        assert response.status_code == 200
        assert response.json()['success'] is True
        assert not Comment.objects.filter(id=comment_id).exists()

    def test_delete_comment_as_non_author(self, api_client, another_auth_headers, test_comment):
        comment_id = test_comment.id
        response = api_client.delete(
            f'/comments/{comment_id}',
            headers = another_auth_headers 
        )
        
        assert response.status_code == 403
        assert Comment.objects.filter(id=comment_id).exists()
        