def test_create_and_read_employee(client):
    # 1. CREATE
    response = client.post(
        "/api/v1/employees/",
        json={
            "name": "Prateek Bidve",
            "email": "prateek@example.com",
            "department": "Engineering",
            "salary": 120000
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Prateek Bidve"
    emp_id = data["id"]

    # 2. READ
    get_response = client.get(f"/api/v1/employees/{emp_id}")
    assert get_response.status_code == 200
    assert get_response.json()["email"] == "prateek@example.com"

def test_delete_employee(client):
    # Setup: Create an employee first
    create_res = client.post(
        "/api/v1/employees/",
        json={"name": "Test User", "email": "test@hr.com", "department": "HR", "salary": 50000}
    )
    emp_id = create_res.json()["id"]

    # Action: Delete
    del_res = client.delete(f"/api/v1/employees/{emp_id}")
    assert del_res.status_code == 204

    # Verify: Get should now 404
    final_get = client.get(f"/api/v1/employees/{emp_id}")
    assert final_get.status_code == 404