from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.all_models import User, Profile 
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash 

async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalars().first()

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()

async def get_all_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()

async def create_user(db: AsyncSession, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    
    db_user = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        password=hashed_password  
    )
    db.add(db_user)
    await db.commit() 
    await db.refresh(db_user)
    
    db_profile = Profile(bio="Новий користувач", user_id=db_user.id)
    db.add(db_profile)
    await db.commit()
    
    await db.refresh(db_user) 
    return db_user

async def update_user(db: AsyncSession, user_id: int, user_data: UserUpdate):
    db_user = await get_user(db, user_id)
    if not db_user:
        return None

    update_data = user_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if key == "password":
            value = get_password_hash(value)
        setattr(db_user, key, value)
    
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def delete_user(db: AsyncSession, user_id: int):
    db_user = await get_user(db, user_id)
    if db_user:
        await db.delete(db_user)
        await db.commit()
        return True
    return False