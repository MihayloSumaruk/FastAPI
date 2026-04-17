from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas import blog as schemas
from app.crud import blog as crud_blog

router = APIRouter()

# --- Категорії ---
@router.post("/categories/", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    return crud_blog.create_category(db=db, category_name=category.name)

@router.get("/categories/", response_model=list[schemas.Category])
def list_categories(db: Session = Depends(get_db)):
    return crud_blog.get_categories(db)

# --- Пости ---
@router.post("/posts/", response_model=schemas.Post)
def create_new_post(post: schemas.PostCreate, author_id: int, db: Session = Depends(get_db)):
    # В реальному проекті author_id брався б з токена авторизації
    return crud_blog.create_post(db=db, post_data=post, author_id=author_id)

@router.get("/posts/", response_model=list[schemas.Post])
def read_all_posts(db: Session = Depends(get_db)):
    return crud_blog.get_posts(db)

# --- Коментарі ---
@router.post("/comments/", response_model=schemas.Comment)
def leave_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    return crud_blog.add_comment(db=db, comment_text=comment.text, post_id=comment.post_id)