from app.schemas.user import UserCreate, UserUpdate


users_db = {}
id_counter = 1

def create_user(user_data: UserCreate):
    global id_counter
    user_id = id_counter
    new_user = {"id": user_id, **user_data.model_dump()}
    users_db[user_id] = new_user
    id_counter += 1
    return new_user

def get_user(user_id: int):
    return users_db.get(user_id)

def get_all_users():
    return list(users_db.values())

def update_user(user_id: int, user_data: UserUpdate):
    if user_id not in users_db:
        return None
    
    current_user = users_db[user_id]
    update_dict = user_data.model_dump(exclude_unset=True)
    current_user.update(update_dict)
    
    users_db[user_id] = current_user
    return current_user

def delete_user(user_id: int):
    if user_id in users_db:
        del users_db[user_id]
        return True
    return False