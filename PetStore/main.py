import json
from time import sleep

import requests

BASE_URL = "https://petstore.swagger.io/v2"
HEADERS = {"Content-Type": "application/json"}
TEST_PET_ID = 987654321
files = {'file': open('dog.jpg', 'rb')}

# Liczniki
success_count = 0
error_count = 0


def run_test(test_func):
    global success_count, error_count
    try:
        test_func()
        print(f"[✅] {test_func.__name__}")
        success_count += 1
    except Exception as e:
        print(f"[❌] {test_func.__name__} failed: {e}")
        error_count += 1
    sleep(0.1)

# ---------------------------
# POST /pet
# ---------------------------

def test_add_pet_positive():
    payload = {
        "id": TEST_PET_ID,
        "name": "Rex",
        "photoUrls": ["http://example.com/photo.jpg"],
        "status": "available"
    }
    response = requests.post(f"{BASE_URL}/pet", headers=HEADERS, json=payload)
    assert response.status_code == 200
    assert response.json()["name"] == "Rex"

def test_add_pet_negative_missing_field():
    payload = {

    }
    response = requests.post(f"{BASE_URL}/pet", headers=HEADERS, json=payload)
    assert response.status_code == 405


# ---------------------------
# GET /pet/{id}
# ---------------------------

def test_get_pet_positive():
    payload = {
        "id": TEST_PET_ID,
        "name": "Rex",
        "photoUrls": ["http://example.com/photo.jpg"],
        "status": "available"
    }
    requests.post(f"{BASE_URL}/pet", headers=HEADERS, json=payload)
    sleep(0.05)

    response = requests.get(f"{BASE_URL}/pet/{TEST_PET_ID}")
    # print(response)
    # print(response.json())
    assert response.status_code == 200
    assert response.json()["id"] == TEST_PET_ID

def test_get_pet_negative_invalid_id():
    response = requests.get(f"{BASE_URL}/pet/000000")
    assert response.status_code == 404


# ---------------------------
# PUT /pet
# ---------------------------

def test_update_pet_positive():
    payload = {
        "id": TEST_PET_ID,
        "name": "RexUpdated",
        "photoUrls": ["http://example.com/photo.jpg"],
        "status": "sold"
    }
    response = requests.put(f"{BASE_URL}/pet", headers=HEADERS, json=payload)
    # print(response)
    # print(response.json())
    assert response.status_code == 200
    assert response.json()["name"] == "RexUpdated"

def test_update_pet_negative_missing_id():
    # expected 404
    payload = {
        "name": "NoID",
        "status": "available"
    }
    response = requests.put(f"{BASE_URL}/pet", headers=HEADERS, json=payload)
    assert response.status_code == 404


# ---------------------------
# DELETE /pet/{id}
# ---------------------------

def test_delete_pet_positive():
    payload = {
        "id": TEST_PET_ID,
        "name": "Rex",
        "photoUrls": ["http://example.com/photo.jpg"],
        "status": "available"
    }
    requests.post(f"{BASE_URL}/pet", headers=HEADERS, json=payload)
    sleep(0.05)

    response = requests.delete(f"{BASE_URL}/pet/{TEST_PET_ID}")
    # print(response)
    # print(response.json())
    assert response.status_code == 200


def test_delete_pet_negative_nonexistent():
    response = requests.delete(f"{BASE_URL}/pet/000000")
    assert response.status_code == 404


# ---------------------------
# GET /pet/findByStatus
# ---------------------------

def test_find_by_status_positive():
    response = requests.get(f"{BASE_URL}/pet/findByStatus", params={"status": "available"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_find_by_status_negative_invalid_status():
    response = requests.get(f"{BASE_URL}/pet/findByStatus", params={"status": "invalidStatus"})
    assert response.status_code == 400
    assert isinstance(response.json(), list)


# ---------------------------
# MAIN: Wywołanie testów
# ---------------------------

if __name__ == "__main__":
    test_functions = [
        #test_add_image_positive,
        test_add_pet_positive,
        test_add_pet_negative_missing_field,
        test_get_pet_positive,
        test_get_pet_negative_invalid_id,
        test_update_pet_positive,
        test_update_pet_negative_missing_id,
        test_delete_pet_positive,
        test_delete_pet_negative_nonexistent,
        test_find_by_status_positive,
        test_find_by_status_negative_invalid_status
    ]

    print("🔍 Rozpoczynanie testów API...\n")
    for test in test_functions:
        run_test(test)

    print("\n📊 Podsumowanie:")
    print(f"✅ Sukcesy: {success_count}")
    print(f"❌ Błędy: {error_count}")

# test_add_pet_negative_missing_field failed
# test_update_pet_negative_missing_id failed
# test_find_by_status_negative_invalid_status failed