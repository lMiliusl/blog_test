from ninja import Schema
from typing import Optional, List
from datetime import datetime

class CategorySchema(Schema):
    id: int
    name: str
    description: Optional[str] = None

class CategoryCreateSchema(Schema):
    name: str
    description: Optional[str] = None

class ArticleSchema(Schema):
    id:int
    title: str
    content: str
    author_id: int
    author_name: str
    category: Optional[CategorySchema] = None
    created_at: datetime
    update_at: datetime

class ArticleCreateSchema(Schema):
    title: str
    content: str
    category_id: Optional[int] = None

class ArticleUpdateSchema(Schema):
    title: Optional[str] = None
    comtent: Optional[str] = None
    category_id: Optional[int] = None