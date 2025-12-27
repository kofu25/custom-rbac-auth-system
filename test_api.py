import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def print_res(name, response):
    status = response.status_code
    color = "\033[92m" if status < 400 else "\033[91m"
    reset = "\033[0m"
    print(f"[*] Test: {name}")
    print(f"    Status: {color}{status}{reset}")
    try:
        print(f"    Response: {response.json()}")
    except:
        print(f"    Response: {response.text}")
    print("-" * 40)

def run_tests():
    # 1. Тест Админа (созданного через init_db.py)
    print("\n--- PHASE 1: ADMIN CHECK ---")
    admin_login_data = {"email": "admin@test.com", "password": "admin123"}
    resp = requests.post(f"{BASE_URL}/login/", json=admin_login_data)
    print_res("Admin Login", resp)
    admin_token = resp.json().get('token')
    admin_headers = {"Authorization": f"Bearer {admin_token}"}

    # Проверка доступа к правилам (только для админа)
    resp = requests.get(f"{BASE_URL}/admin/rules/", headers=admin_headers)
    print_res("Admin Get Access Rules", resp)

    # 2. Тест Регистрации нового пользователя
    print("\n--- PHASE 2: USER LIFECYCLE ---")
    new_user = {
        "full_name": "Test User",
        "email": "tester@test.com",
        "password_hash": "pass123",
        "password_repeat": "pass123"
    }
    resp = requests.post(f"{BASE_URL}/register/", json=new_user)
    print_res("User Registration", resp)

    # Логин
    login_data = {"email": "tester@test.com", "password": "pass123"}
    resp = requests.post(f"{BASE_URL}/login/", json=login_data)
    print_res("User Login", resp)
    user_token = resp.json().get('token')
    user_headers = {"Authorization": f"Bearer {user_token}"}

    # Проверка профиля
    resp = requests.get(f"{BASE_URL}/profile/", headers=user_headers)
    print_res("Get Profile", resp)

    # Обновление профиля (PATCH)
    resp = requests.patch(f"{BASE_URL}/profile/", json={"full_name": "Updated Tester"}, headers=user_headers)
    print_res("Update Profile", resp)

    # 3. Тест Авторизации (403 Forbidden)
    print("\n--- PHASE 3: RBAC CHECK ---")
    # Обычный юзер пытается посмотреть правила админа
    resp = requests.get(f"{BASE_URL}/admin/rules/", headers=user_headers)
    print_res("User access Admin Rules (Should be 403)", resp)

    # 4. Тест Мягкого удаления
    print("\n--- PHASE 4: SOFT DELETE ---")
    resp = requests.delete(f"{BASE_URL}/profile/", headers=user_headers)
    print_res("Soft Delete Account", resp)

    # Попытка залогиниться удаленным аккаунтом
    resp = requests.post(f"{BASE_URL}/login/", json=login_data)
    print_res("Login after delete (Should be 401)", resp)

if __name__ == "__main__":
    try:
        run_tests()
    except Exception as e:
        print(f"Connection error: {e}. Is server running?")