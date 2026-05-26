# ---------------------------------------------------------------------------
# Tests: Full CRUD coverage for /api/v1/employees/
# Run: pytest app/tests/ -v
# ---------------------------------------------------------------------------


def test_create_employee(client):
    response = client.post(
        "/api/v1/employees/",
        json={"name": "Pratik Bidve", "email": "pratik@example.com", "department": "Engineering", "salary": 120000},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Pratik Bidve"
    assert data["email"] == "pratik@example.com"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_create_duplicate_email_returns_400(client):
    payload = {"name": "User A", "email": "dup@example.com", "department": "HR", "salary": 50000}
    client.post("/api/v1/employees/", json=payload)
    response = client.post("/api/v1/employees/", json=payload)
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]


def test_read_employee(client):
    create_res = client.post(
        "/api/v1/employees/",
        json={"name": "Read Test", "email": "read@example.com", "department": "Sales", "salary": 60000},
    )
    emp_id = create_res.json()["id"]

    get_res = client.get(f"/api/v1/employees/{emp_id}")
    assert get_res.status_code == 200
    assert get_res.json()["id"] == emp_id


def test_read_nonexistent_returns_404(client):
    response = client.get("/api/v1/employees/nonexistent-id")
    assert response.status_code == 404


def test_list_employees_with_pagination(client):
    # Seed 3 employees
    for i in range(3):
        client.post(
            "/api/v1/employees/",
            json={"name": f"User {i}", "email": f"user{i}@example.com", "department": "Engineering", "salary": 70000},
        )

    all_res = client.get("/api/v1/employees/?skip=0&limit=10")
    assert all_res.status_code == 200
    assert len(all_res.json()) == 3

    page_res = client.get("/api/v1/employees/?skip=0&limit=2")
    assert len(page_res.json()) == 2

    page2_res = client.get("/api/v1/employees/?skip=2&limit=10")
    assert len(page2_res.json()) == 1


def test_update_employee(client):
    create_res = client.post(
        "/api/v1/employees/",
        json={"name": "Before Update", "email": "update@example.com", "department": "Sales", "salary": 80000},
    )
    emp_id = create_res.json()["id"]

    update_res = client.put(
        f"/api/v1/employees/{emp_id}",
        json={"name": "After Update", "salary": 95000},
    )
    assert update_res.status_code == 200
    data = update_res.json()
    assert data["name"] == "After Update"
    assert data["salary"] == 95000
    # Fields not passed should remain unchanged
    assert data["department"] == "Sales"
    assert data["email"] == "update@example.com"


def test_update_nonexistent_returns_404(client):
    response = client.put("/api/v1/employees/ghost-id", json={"salary": 100000})
    assert response.status_code == 404


def test_update_email_conflict_returns_400(client):
    client.post(
        "/api/v1/employees/",
        json={"name": "Emp A", "email": "a@example.com", "department": "HR", "salary": 50000},
    )
    create_b = client.post(
        "/api/v1/employees/",
        json={"name": "Emp B", "email": "b@example.com", "department": "HR", "salary": 50000},
    )
    emp_b_id = create_b.json()["id"]

    # Try to set Emp B's email to Emp A's email
    res = client.put(f"/api/v1/employees/{emp_b_id}", json={"email": "a@example.com"})
    assert res.status_code == 400


def test_delete_employee(client):
    create_res = client.post(
        "/api/v1/employees/",
        json={"name": "To Delete", "email": "delete@example.com", "department": "HR", "salary": 45000},
    )
    emp_id = create_res.json()["id"]

    del_res = client.delete(f"/api/v1/employees/{emp_id}")
    assert del_res.status_code == 204

    final_get = client.get(f"/api/v1/employees/{emp_id}")
    assert final_get.status_code == 404


def test_delete_nonexistent_returns_404(client):
    response = client.delete("/api/v1/employees/ghost-id")
    assert response.status_code == 404
