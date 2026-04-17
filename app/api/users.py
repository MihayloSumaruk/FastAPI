from fastapi import APIRouter, HTTPException
from app.schemas.user import User, UserCreate, UserUpdate
from app.crud import users as crud_users 

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=User)
def create_user(user_data: UserCreate):
    return crud_users.create_user(user_data)

@router.get("/", response_model=list[User])
def read_users():
    return crud_users.get_all_users()

@router.get("/{user_id}", response_model=User)
def read_user(user_id: int):
    user = crud_users.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user_data: UserUpdate):
    user = crud_users.update_user(user_id, user_data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}")
def delete_user(user_id: int):
    success = crud_users.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}