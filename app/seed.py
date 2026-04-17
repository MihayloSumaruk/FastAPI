import asyncio
from app.core.database import AsyncSessionLocal
from app.models.all_models import User, Category, Post

async def seed():
    async with AsyncSessionLocal() as session:
        # Додаємо категорії
        cat1 = Category(name="Electronics")
        cat2 = Category(name="Books")
        session.add_all([cat1, cat2])
        
        # Додаємо юзера
        user = User(username="misha_dev", email="dev@misha.com", full_name="Misha Dev", password="123")
        session.add(user)
        
        await session.commit()
        print("✅ База наповнена!")

if __name__ == "__main__":
    asyncio.run(seed())