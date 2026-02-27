from ninja import Schema
from typing import Optional, List
from datetime import datetime

class CommentSchema(Schema):
    id: int
    content: str
    author_id: int
    author_name: str
    article_id: int
    parent_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

class CommentCreateSchema(Schema):
    content: str
    article_id: int
    parent_id: Optional[int] = None

class CommentUpdateSchema(Schema):
    content: Optional[str] = None