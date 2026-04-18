from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import blog as schemas
from app.crud import blog as crud_blog
from app.models.all_models import User
from app.core.database import get_db
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/posts/", response_model=schemas.Post)
async def create_new_post(
    post: schemas.PostCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user) 
):
    """Створити пост може лише авторизований користувач."""
    return await crud_blog.create_post(db=db, post_data=post, author_id=current_user.id)

@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user) 
):
    """
    Видалити пост може ТІЛЬКИ його автор.
    """
    post = await crud_blog.get_post(db=db, post_id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="You don't have permission to delete someone else's post"
        )
    
    await crud_blog.delete_post(db=db, post_id=post_id)