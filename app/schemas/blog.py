from pydantic import BaseModel, ConfigDict
from typing import List, Optional

# --- Category ---
class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- Comment ---
class CommentBase(BaseModel):
    text: str

class CommentCreate(CommentBase):
    post_id: int

class Comment(CommentBase):
    id: int
    post_id: int
    model_config = ConfigDict(from_attributes=True)

# --- Post ---
class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    category_id: int

class Post(PostBase):
    id: int
    author_id: int
    category: Optional[Category] = None
    comments: List[Comment] = []
    model_config = ConfigDict(from_attributes=True)