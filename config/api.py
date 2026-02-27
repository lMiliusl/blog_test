from ninja import NinjaAPI
from apps.users.api import router as user_router
from apps.articles.api import router as articles_router
from apps.comments.api import router as comments_router


api = NinjaAPI(
    title='Blog API',
    description='API для блога',
    version='1.0.0'
)

api.add_router('/users/', user_router)
api.add_router('/articles/', articles_router)
api.add_router('/comments/', comments_router)