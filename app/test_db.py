from app.core.database import SessionLocal
from app.crud import users as crud_users
from app.crud import blog as crud_blog
from app.schemas.user import UserCreate
from app.schemas.blog import PostCreate, CategoryCreate, CommentCreate

def run_test():
    db = SessionLocal()
    try:
        print("\n Починаємо повну перевірку бази")

        # 1. Створюємо юзера (і автоматично профіль)
        user_in = UserCreate(
            username="misha_test", 
            email="misha@test.com", 
            full_name="Misha Tester", 
            password="123"
        )
        user = crud_users.create_user(db, user_in)
        print(f"✅ Юзер створений: {user.username} (ID: {user.id})")
        print(f"✅ Профіль створений автоматично: {user.profile.bio}")

        # 2. Створюємо категорію
        cat = crud_blog.create_category(db, "Backend Magic")
        print(f"✅ Категорія створена: {cat.name} (ID: {cat.id})")

        # 3. Створюємо пост
        post_in = PostCreate(title="Як я задовбався з лабою", content="Це був довгий шлях...", category_id=cat.id)
        post = crud_blog.create_post(db, post_in, author_id=user.id)
        print(f"✅ Пост створений: '{post.title}' від автора {post.author.username}")

        # 4. Додаємо коментар
        comm_in = CommentCreate(text="Михайло, ти це зробив!", post_id=post.id)
        comment = crud_blog.add_comment(db, comm_in)
        print(f"✅ Коментар додано до поста ID {comment.post_id}")

        print("\n--- ФІНАЛЬНА ПЕРЕВІРКА ЗВ'ЯЗКІВ ---")
        # Беремо пост з бази ще раз, щоб SQLAlchemy підтягнув усі зв'язки
        check_post = crud_blog.get_posts(db)[-1]
        print(f"Пост: {check_post.title}")
        print(f"Категорія: {check_post.category.name}")
        print(f"Автор: {check_post.author.full_name}")
        print(f"Кількість коментарів: {len(check_post.comments)}")
        print(f"Текст коментаря: {check_post.comments[0].text}")
        
        print("\n WELL DONE")

    except Exception as e:
        print(f"\n ERROR  {e}")
    finally:
        db.close()

if __name__ == "__main__":
    run_test()