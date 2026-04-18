from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.core.database import get_db
from app.core.security import verify_password, create_access_token
from app.crud import users as crud_users
from app.schemas import user as s

router = APIRouter()

# Схема для логіну
class UserLogin(BaseModel):
    email: str
    password: str

@router.post("/register", response_model=s.User, status_code=status.HTTP_201_CREATED)
async def register(user: s.UserCreate, db: AsyncSession = Depends(get_db)):
    """Ручка для реєстрації нового користувача"""
    # Перевіряємо, чи є вже такий email
    existing_user = await crud_users.get_user_by_email(db, email=user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return await crud_users.create_user(db=db, user=user)

@router.post("/login")
async def login(response: Response, user_data: UserLogin, db: AsyncSession = Depends(get_db)):
    """Ручка для аутентифікації та видачі кукі"""
    # 1. Шукаємо юзера в базі
    user = await crud_users.get_user_by_email(db, email=user_data.email)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # 2. Перевіряємо хеш пароля
    if not verify_password(user_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # 3. Генеруємо JWT
    access_token = create_access_token(data={"sub": str(user.id)})
    
    # 4. Записуємо токен у HTTP-Only куку
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,  # Javascript не зможе прочитати цю куку (захист від XSS)
        max_age=1800,   # 30 хвилин
        samesite="lax"  # Захист від CSRF
    )
    
    return {"message": "Login successful"}

@router.post("/logout")
async def logout(response: Response):
    """Видаляє куку"""
    response.delete_cookie("access_token")
    return {"message": "Logged out successfully"}