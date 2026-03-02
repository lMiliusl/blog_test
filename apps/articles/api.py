from ninja import Router
from ninja.errors import HttpError
from django.shortcuts import get_object_or_404
from typing import List
from .models import Article, Category
from .schemas import ArticleSchema, ArticleCreateSchema, ArticleUpdateSchema, CategorySchema, CategoryCreateSchema
from apps.users.auth import token_auth
from apps.core.decorators import log_crud_operations

router = Router(tags=['articles'])

@router.get('/categories', response=List[CategorySchema])
def list_categories(request):
    return Category.objects.all()

@router.post('/categories', response=CategorySchema, auth=token_auth)
def create_category(request, data: CategoryCreateSchema):
    if not request.user.is_authenticated:
        return 401, {'Authentication required'}
    
    category = Category.objects.create(**data.dict())
    return category

@router.get('/articles', response=List[ArticleSchema])
def list_articles(request):
    articles = Article.objects.all().select_related('author', 'category')
    result = []
    for article in articles:
        result.append({
            'id': article.id,
            'title': article.title,
            'content': article.content,
            'author_id': article.author.id,
            'author_name': article.author.username,
            'category': article.category,
            'created_at': article.created_at,
            'update_at': article.update_at
        })
    return result

@router.get('/articles{article_id}', response=ArticleSchema)
def get_article(request, article_id: int):
    article = get_object_or_404(Article, id=article_id)
    return {
        'id': article.id,
        'title': article.title,
        'content': article.content,
        'author_id': article.author.id,
        'author_name': article.author.username,
        'category': article.category,
        'created_at': article.created_at,
        'update_at': article.update_at
    }

@router.post('/articles', response=ArticleSchema, auth=token_auth)
@log_crud_operations('Article')
def create_article(request, data: ArticleCreateSchema):
    if not request.user.is_authenticated:
        return 401
    
    article_data = data.dict()
    category_id = article_data.get('category_id', None)

    article = Article.objects.create(
        **article_data,
        author=request.user
    )

    if category_id:
        category = get_object_or_404(Category, id=category_id)
        article.category = category
        article.save()

    return{
        'id': article.id,
        'title': article.title,
        'content': article.content,
        'author_id': article.author.id,
        'author_name': article.author.username,
        'category': article.category,
        'created_at': article.created_at,
        'update_at': article.update_at
    }

@router.put('/articles{article_id}', response=ArticleSchema, auth=token_auth)
@log_crud_operations('Article')
def update_article(request, article_id : int, data: ArticleUpdateSchema):
    article = get_object_or_404(Article, id=article_id)

    if article.author != request.user:
        raise HttpError (403, 'Вы не автор данной статьи')
    
    for attr, value in data.dict(exclude_unset=True).items():
        if attr == 'category_id' and value is not None:
            category = get_object_or_404(Category, id=value)
            article.category = category
        elif attr != 'category_id' and value is not None:
            setattr(article, attr, value)

    article.save()

    return {
        'id': article.id,
        'title': article.title,
        'content': article.content,
        'author_id': article.author.id,
        'author_name': article.author.username,
        'category': article.category,
        'created_at': article.created_at,
        'update_at': article.update_at
        }

@router.delete('/articles{article_id}', auth=token_auth)
@log_crud_operations('Article')
def delete_article(request, article_id: int):
    article = get_object_or_404(Article, id=article_id)

    if article.author != request.user:
        raise HttpError (403, 'Вы не автор данной статьи')
    
    article.delete()
    return{'success': True}