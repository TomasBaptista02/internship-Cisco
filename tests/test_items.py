from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_min_price_filter() -> None:
    response = client.get("/items?min_price=4")
    assert all(item["price"] >= 4 for item in response.json())


def test_short_name() -> None:
    response = client.post("/items", json={"name": "ab", "price": 5})
    assert response.status_code == 422


def test_update_to_duplicate_name() -> None:
    client.post("/items", json={"name": "Grape", "price": 6})
    resp = client.put("/items/1", json={"name": "Grape"})
    assert resp.status_code == 400 or resp.status_code == 422


def test_create_item_sets_correct_name() -> None:
    json = {"name": "fictitious name", "price": 35}
    response = client.post("/items", json=json)
    assert response.status_code == 200
    assert response.json()["name"] == "fictitious name"


def test_item_name_consistency() -> None:
    json = {"name": "fictitious name", "price": 35}
    client.post("/items", json=json)
    response = client.get("/items?min_price=35&offset=0&limit=10000000000000")
    assert any(item["name"] == "fictitious name" for item in response.json())


def test_verify_offset() -> None:
    response = client.get("/items?min_price=0&offset=0&limit=1")
    assert len(response.json()) == 1
    response2 = client.get("/items?min_price=0&offset=0&limit=10")
    assert len(response2.json()) == 10


def test_set_price_below_0() -> None:
    response = client.post("/items", json={"name": "ficticious name", "price": -35})
    assert response.status_code == 422


def test_search_items_price_below_0() -> None:
    response2 = client.get("/items?min_price=-39&offset=0&limit=10000000000000")
    assert response2.status_code == 400


def test_negative_offset() -> None:
    response2 = client.get("/items?min_price=0.0&offset=-1&limit=10000000000000")
    assert response2.status_code == 400


def test_negative_limit() -> None:
    response2 = client.get("/items?min_price=0.0&offset=0&limit=-10")
    assert response2.status_code == 400
