import os
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter

# 1. Забираємо URL з налаштувань Docker, а не хардкодимо localhost
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql+asyncpg://postgres:postgres@db:5432/postgres"
)
# Переконуємось, що використовуємо правильний асинхронний драйвер
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# 2. Створюємо сам додаток (тепер Uvicorn його знайде!)
app = FastAPI(title="Lab 7 - Monitoring")

# 3. Створюємо кастомну метрику для викладача (Лічильник сумарної ціни)
total_revenue = Counter(
    "total_purchase_price", 
    "Сумарна ціна всіх покупок"
)

# 4. Підключаємо Прометеус: він автоматично створить шлях /metrics
Instrumentator().instrument(app).expose(app)

# 5. Тестовий ендпоінт, щоб ми могли робити "покупки" і міняти метрику
@app.get("/buy/{price}")
async def make_purchase(price: int):
    total_revenue.inc(price)
    return {"message": f"Покупку на суму {price} успішно проведено!", "revenue_updated": True}