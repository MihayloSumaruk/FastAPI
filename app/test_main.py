import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.main import app
from app.core.database import get_db, Base
from app.crud import users as crud_users
from app.crud import blog as crud_blog
from app.schemas.user import UserCreate
from app.schemas.blog import PostCreate
from app.models.all_models import Category, Post

# 1. Налаштування тестової БД (Postgres)
TEST_DB_URL = "postgresql+asyncpg://user:password@db:5432/test_db"
engine = create_async_engine(TEST_DB_URL, poolclass=NullPool)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession, expire_on_commit=False
)

# 2. Підміна залежності get_db
async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

# 3. Автоматичне очищення БД перед кожним тестом
@pytest.fixture(autouse=True)
async def prepare_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield

# 4. Фікстури
@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

@pytest.fixture
async def db_session():
    async with TestingSessionLocal() as session:
        yield session

# ==========================================
# ЧАСТИНА 1: ТЕСТИ CRUD (ФУНКЦІЇ БД)
# ==========================================

@pytest.mark.asyncio
async def test_crud_operations(db_session: AsyncSession):
    # Тест створення юзера
    user_in = UserCreate(username="tester", email="t@t.com", full_name="T", password="123")
    user = await crud_users.create_user(db_session, user_in)
    assert user.id is not None

    # Створюємо категорію для поста
    cat = Category(id=1, name="Tech")
    db_session.add(cat)
    await db_session.commit()

    # Тест створення поста
    post_in = PostCreate(title="CRUD Test", content="Content", category_id=1)
    post = await crud_blog.create_post(db_session, post_in, author_id=user.id)
    assert post.title == "CRUD Test"

    # Тест отримання поста
    fetched_post = await crud_blog.get_post(db_session, post.id)
    assert fetched_post.id == post.id

    # Тест видалення поста
    deleted = await crud_blog.delete_post(db_session, post.id)
    assert deleted is True
    assert await crud_blog.get_post(db_session, post.id) is None

# ==========================================
# ЧАСТИНА 2: ТЕСТИ API (РУЧКИ)
# ==========================================

@pytest.mark.asyncio
async def test_full_auth_flow(client: AsyncClient):
    # Реєстрація
    reg = await client.post("/auth/register", json={
        "username": "api", "email": "api@t.com", "full_name": "A", "password": "123"
    })
    assert reg.status_code == 201

    # Логін
    login = await client.post("/auth/login", json={"email": "api@t.com", "password": "123"})
    assert login.status_code == 200
    assert "access_token" in client.cookies

@pytest.mark.asyncio
async def test_post_lifecycle_api(client: AsyncClient, db_session: AsyncSession):
    # Підготовка: категорія + юзер + логін
    cat = Category(id=1, name="News")
    db_session.add(cat)
    await db_session.commit()
    
    await client.post("/auth/register", json={"username":"u","email":"u@u.com","full_name":"U","password":"123"})
    await client.post("/auth/login", json={"email":"u@u.com","password":"123"})

    # 1. Створення поста
    res_create = await client.post("/blog/posts/", json={"title":"T","content":"C","category_id":1})
    post_id = res_create.json()["id"]
    assert res_create.status_code == 200

    # 2. Видалення поста (викликаємо DELETE, як ти й реалізував)
    res_del = await client.delete(f"/blog/posts/{post_id}")
    assert res_del.status_code == 204