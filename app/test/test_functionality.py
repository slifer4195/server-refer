import requests

BASE_URL = "http://127.0.0.1:5000"
session = requests.Session()  # persists cookies

def setup_user():
    print("\n--- Setup: Register + Login ---")
    payload = {
        "company_name": "TestCorp",
        "email": "slifer4195@gmail.com",
        "password": "Slifer4195!"
    }
    r = session.post(f"{BASE_URL}/register", json=payload)
    print("Register:", r.status_code, r.json())

    r = session.post(f"{BASE_URL}/login", json={
        "email": "slifer4195@gmail.com",
        "password": "Slifer4195!"
    })
    print("Login:", r.status_code, r.json())

def test_add_customer():
    print("\n--- Add Customer ---")
    payload = {"email": "customer1@example.com"}
    r = session.post(f"{BASE_URL}/add-customer", json=payload)
    print(r.status_code, r.json())

def test_get_customers():
    print("\n--- Get Customers ---")
    r = session.get(f"{BASE_URL}/customers")
    print(r.status_code, r.json())

def test_customer_count():
    print("\n--- Customer Count ---")
    r = session.get(f"{BASE_URL}/customer-count")
    print(r.status_code, r.json())

def test_delete_customer():
    print("\n--- Delete Customer ---")
    payload = {"email": "customer1@example.com"}
    r = session.delete(f"{BASE_URL}/delete-customer", json=payload)
    print(r.status_code, r.json())

    print("\n--- Confirm Deletion ---")
    r = session.get(f"{BASE_URL}/customers")
    print(r.status_code, r.json())

if __name__ == "__main__":
    setup_user()
    test_add_customer()
    test_get_customers()
    test_customer_count()
    test_delete_customer()
