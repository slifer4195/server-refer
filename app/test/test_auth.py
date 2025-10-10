import requests

BASE_URL = "http://127.0.0.1:5000"
session = requests.Session()  # persists cookies automatically

def test_register():
    print("\n--- Register User ---")
    payload = {
        "company_name": "TestCorp",
        "email": "slifer4195@gmail.com",
        "password": "Slifer4195!"  # meets password rules
    }
    r = session.post(f"{BASE_URL}/register", json=payload)
    print(r.status_code, r.json())

def test_login():
    print("\n--- Login ---")
    payload = {
        "email": "slifer4195@gmail.com",
        "password": "Slifer4195!"  # same password
    }
    r = session.post(f"{BASE_URL}/login", json=payload)
    print(r.status_code, r.json())

def test_check_session():
    print("\n--- Check Session (/session) ---")
    r = session.get(f"{BASE_URL}/session")
    print(r.status_code, r.json())

    print("\n--- Check Session (/logged) ---")
    r = session.get(f"{BASE_URL}/logged")
    print(r.status_code, r.json())

def test_logout():
    print("\n--- Logout ---")
    r = session.post(f"{BASE_URL}/logout")
    print(r.status_code, r.json())

    print("\n--- Check Session After Logout ---")
    r = session.get(f"{BASE_URL}/logged")
    print(r.status_code, r.json())

if __name__ == "__main__":
    test_register()
    test_login()
    test_check_session()
    test_logout()
