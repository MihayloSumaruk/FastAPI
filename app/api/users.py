from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import user as s  
from app.crud import users as crud_users
from app.core.database import get_db 
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/", response_model=s.User)
async def create_user(user: s.UserCreate, db: AsyncSession = Depends(get_db)): # Додано async
    return await crud_users.create_user(db=db, user=user) # Додано await

@router.get("/me", response_model=s.User)
async def read_user_me(current_user: s.User = Depends(get_current_user)):
    """Повертає дані поточного користувача (себе)"""
    return current_user

@router.put("/{user_id}", response_model=s.User)
def update_user(user_id: int, user: s.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud_users.update_user(db=db, user_id=user_id, user_data=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    if not crud_users.delete_user(db=db, user_id=user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return None