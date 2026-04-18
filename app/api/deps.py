from fastapi import Request, Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import SECRET_KEY, ALGORITHM
from app.crud import users as crud_users

async def get_current_user(request: Request, db: AsyncSession = Depends(get_db)):
    """
    Залежність, яка дістає токен з куки, перевіряє його 
    та повертає об'єкт поточного користувача.
    """
    # 1. Дістаємо токен з кук
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        # Прибираємо префікс 'Bearer ', якщо він є
        token = token.replace("Bearer ", "")
        # 2. Декодуємо JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    # 3. Шукаємо юзера в базі
    user = await crud_users.get_user(db, user_id=int(user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    return user