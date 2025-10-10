import requests

BASE_URL = "http://127.0.0.1:5000"
session = requests.Session()

def setup_user_and_customer():
    print("\n--- Setup User (Register + Login) ---")
    payload = {
        "company_name": "PointCorp",
        "email": "point_tester@example.com",
        "password": "Password123!"
    }
    r = session.post(f"{BASE_URL}/register", json=payload)
    print("Register:", r.status_code, r.json())

    r = session.post(f"{BASE_URL}/login", json={
        "email": "point_tester@example.com",
        "password": "Password123!"
    })
    print("Login:", r.status_code, r.json())

    print("\n--- Add Customer ---")
    r = session.post(f"{BASE_URL}/add-customer", json={"email": "slifer4195@gmail.com"})
    print(r.status_code, r.json())

    # Grab customer_id
    r = session.get(f"{BASE_URL}/customers")
    customers = r.json()
    print("Customers:", customers)
    customer_id = customers[0]["id"] if customers else None
    return customer_id

def setup_menu_item():
    print("\n--- Create Menu Item ---")
    payload = {"item": "Test Drink", "price": 5.0, "required_points": 5}
    r = session.post(f"{BASE_URL}/menu", json=payload)
    print(r.status_code, r.json())
    return r.json().get("item_id")

def test_send_test_email(user_id, customer_id):
    print("\n--- Send Test Email + Add Points ---")
    payload = {
        "to": "slifer4195@gmail.com",
        "subject": "Test Subject",
        "body": "Test Body",
        "user_id": user_id,
        "customer_id": customer_id,
        "point": 10
    }
    r = session.post(f"{BASE_URL}/send-test-email", json=payload)
    print(r.status_code, r.json())

def test_get_customer_points(customer_id):
    print("\n--- Get Customer Points ---")
    r = session.get(f"{BASE_URL}/customer_point/{customer_id}")
    print(r.status_code, r.json())

def test_deduct_points(customer_id, item_id):
    print("\n--- Deduct Points for Item ---")
    r = session.get(f"{BASE_URL}/deduct_point/{customer_id}/{item_id}")
    print(r.status_code, r.json())

if __name__ == "__main__":
    # Setup
    customer_id = setup_user_and_customer()
    item_id = setup_menu_item()

    # Grab logged in user_id from /session
    r = session.get(f"{BASE_URL}/session")
    user_id = r.json().get("user_id")
    print("Session:", r.json())

    if user_id and customer_id:
        test_send_test_email(user_id, customer_id)
        test_get_customer_points(customer_id)
        if item_id:
            test_deduct_points(customer_id, item_id)
