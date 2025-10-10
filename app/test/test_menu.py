import requests

BASE_URL = "http://127.0.0.1:5000"
session = requests.Session()

def setup_user():
    print("\n--- Setup User (Register + Login) ---")
    payload = {
        "company_name": "TestCorp",
        "email": "menu_tester@example.com",
        "password": "Password123!"
    }
    r = session.post(f"{BASE_URL}/register", json=payload)
    print("Register:", r.status_code, r.json())

    r = session.post(f"{BASE_URL}/login", json={
        "email": "menu_tester@example.com",
        "password": "Password123!"
    })
    print("Login:", r.status_code, r.json())

def test_create_menu_item():
    print("\n--- Create Menu Item ---")
    payload = {"item": "Burger", "price": 9.99, "required_points": 20}
    r = session.post(f"{BASE_URL}/menu", json=payload)
    print(r.status_code, r.json())
    return r.json().get("item_id")

def test_list_menu_items():
    print("\n--- List Menu Items ---")
    r = session.get(f"{BASE_URL}/list_menu")
    print(r.status_code, r.json())
    return r.json()

def test_update_menu_item(item_id):
    print("\n--- Update Menu Item ---")
    payload = {"item": "Cheeseburger", "price": 10.99, "required_points": 25}
    r = session.put(f"{BASE_URL}/update_menu/{item_id}", json=payload)
    print(r.status_code, r.json())

def test_delete_menu_item(item_id):
    print("\n--- Delete Menu Item ---")
    r = session.delete(f"{BASE_URL}/delete_item/{item_id}")
    print(r.status_code, r.json())

    print("\n--- Confirm Deletion ---")
    r = session.get(f"{BASE_URL}/list_menu")
    print(r.status_code, r.json())

if __name__ == "__main__":
    setup_user()
    item_id = test_create_menu_item()
    test_list_menu_items()
    if item_id:
        test_update_menu_item(item_id)
        test_delete_menu_item(item_id)
