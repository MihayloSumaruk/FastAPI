from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.all_models import Post, Category, Comment
from app.schemas.blog import PostCreate

async def get_categories(db: AsyncSession):
    result = await db.execute(select(Category))
    return result.scalars().all()

async def create_post(db: AsyncSession, post_data: PostCreate, author_id: int):
    db_post = Post(
        title=post_data.title,
        content=post_data.content,
        category_id=post_data.category_id,
        author_id=author_id
    )
    db.add(db_post)
    await db.commit() # Асинхронний комміт
    await db.refresh(db_post)
    return db_post