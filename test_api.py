import requests

BASE_URL = "http://localhost:8000"

# Створюємо "сесію", яка буде зберігати наші кукі як справжній браузер
session = requests.Session()

def run_tests():
    print("--- 1. ПРОБУЄМО ЗАЛОГІНИТИСЬ ---")
    login_data = {
        "email": "Admin@gmai.com", 
        "password": "3004" 
    }
    res_login = session.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"Статус: {res_login.status_code}")
    print(f"Відповідь: {res_login.text}\n")

    if res_login.status_code != 200:
        print("❌ Логін не вдався, зупиняємо тест.")
        return

    print("--- 2. СТВОРЮЄМО ПОСТ (Захищена ручка) ---")
    post_data = {
        "title": "Створено через Python-файл!",
        "content": "Swagger більше не потрібен.",
        "category_id": 1
    }
    # Зверни увагу: ми не передаємо токен вручну, session робить це за нас
    res_post = session.post(f"{BASE_URL}/blog/posts/", json=post_data)
    print(f"Статус: {res_post.status_code}")
    print(f"Відповідь: {res_post.json()}\n")
    
    post_id = res_post.json().get("id")

    if post_id:
        print(f"--- 3. ВИДАЛЯЄМО ПОСТ (ID: {post_id}) ---")
        res_del = session.delete(f"{BASE_URL}/blog/posts/{post_id}")
        print(f"Статус видалення: {res_del.status_code}")
        if res_del.status_code == 204:
            print("Пост успішно видалено \n")

    print("--- 4. РОБИМО LOGOUT ---")
    res_logout = session.post(f"{BASE_URL}/auth/logout")
    print(f"Статус: {res_logout.status_code}\n")

    print("--- 5. ПЕРЕВІРКА ЗАХИСТУ ПІСЛЯ ВИХОДУ ---")
    res_fail = session.get(f"{BASE_URL}/users/me")
    print(f"Спроба отримати профіль: Статус {res_fail.status_code}")
    if res_fail.status_code == 401:
         print(" Захист працює ")

if __name__ == "__main__":
    run_tests()