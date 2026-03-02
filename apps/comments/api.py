from ninja import Router
from django.shortcuts import get_object_or_404
from typing import List
from .models import Comment
from apps.articles.models import Article
from .schemas import CommentSchema, CommentCreateSchema, CommentUpdateSchema
from apps.users.auth import token_auth
from django.http import JsonResponse

router = Router(tags=['comments'])

@router.get('/articles/{article_id}/comments', response=List[CommentSchema])
def list_comments(request, article_id: int):
    article = get_object_or_404(Article, id=article_id)
    comments = Comment.objects.filter(
        article=article,
        parent__isnull=True
    ).select_related('author').prefetch_related('replies__author')

    result = []
    for comment in comments:
        result.append({
            'id': comment.id,
            'content': comment.content,
            'author_id': comment.author.id,
            'author_name': comment.author.username,
            'article_id': article_id,
            'parent_id': None,
            'created_at': comment.created_at.isoformat(),
            'updated_at': comment.updated_at.isoformat()
        })

        for reply in comment.replies.all():
            result.append({
                'id': reply.id,
                'content': reply.content,
                'author_id': reply.author.id,
                'author_name': reply.author.username,
                'article_id': article_id,
                'parent_id': comment.id,
                'created_at': reply.created_at.isoformat(),
                'updated_at': reply.updated_at.isoformat()
            })

    return result

@router.post('/comments', response=CommentSchema, auth=token_auth)
def create_comment(request, data: CommentCreateSchema):
    article = get_object_or_404(Article, id=data.article_id)
    parent = None
    if data.parent_id:
        parent = get_object_or_404(Comment, id=data.parent_id)
        if parent.article.id != article.id:
            return JsonResponse ({'error': 'Родительский комментарий не относится к данной статье.'}, status = 400)
        
    comment = Comment.objects.create(
        content = data.content,
        author = request.user,
        article = article,
        parent = parent
    )

    return {
        'id': comment.id,
        'content': comment.content,
        'author_id': comment.author.id,
        'author_name': comment.author.username,
        'article_id': article.id,
        'parent_id': parent.id if parent else None,
        'created_at': comment.created_at.isoformat(),
        'updated_at': comment.updated_at.isoformat()
    }

@router.put('/comments/{comment_id}', response=CommentSchema, auth=token_auth)
def update_comment(request, comment_id: int, data: CommentUpdateSchema):
    comment = get_object_or_404(Comment, id = comment_id)
    if comment.author != request.user:
        return JsonResponse({'error': 'Вы не являетесь автором этого комментария.'}, status = 403)
    
    if data.content:
        comment.content = data.content
        comment.save()

    return{
        'id': comment.id,
        'content': comment.content,
        'author_id': comment.author.id,
        'author_name': comment.author.username,
        'article_id': comment.article.id,
        'parent_id': comment.parent.id if comment.parent else None,
        'created_at': comment.created_at.isoformat(),
        'updated_at': comment.updated_at.isoformat()
    }

@router.delete('/comments/{comment_id}', auth=token_auth)
def delete_comment(request, comment_id: int):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if comment.author != request.user:
        return JsonResponse ({'error': 'Вы не являетесь автором этого комментария.'}, status = 403)
    
    comment.delete()
    return {'success': True}