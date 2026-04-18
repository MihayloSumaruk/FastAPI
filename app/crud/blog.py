from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload 
from app.models.all_models import Post
from app.schemas.blog import PostCreate

async def create_post(db: AsyncSession, post_data: PostCreate, author_id: int):
    db_post = Post(**post_data.model_dump(), author_id=author_id)
    db.add(db_post)
    await db.commit()
    
    result = await db.execute(
        select(Post)
        .options(selectinload(Post.category), selectinload(Post.comments))
        .filter(Post.id == db_post.id)
    )
    return result.scalars().first()

async def get_post(db: AsyncSession, post_id: int):
    result = await db.execute(
        select(Post)
        .options(selectinload(Post.category), selectinload(Post.comments))
        .filter(Post.id == post_id)
    )
    return result.scalars().first()

async def delete_post(db: AsyncSession, post_id: int):
    post = await get_post(db, post_id)
    if post:
        await db.delete(post)
        await db.commit()
        return True
    return False