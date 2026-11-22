import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_unauthorized_product_access(client: AsyncClient):
    # Unauthenticated requests should be rejected
    get_res = await client.get("/product/?id=1")
    assert get_res.status_code == 401

    post_res = await client.post(
        "/product/",
        json={"name": "Wireless Mouse", "price": 29.99, "stock": 50},
    )
    assert post_res.status_code == 401


@pytest.mark.asyncio
async def test_create_product_success(auth_client: AsyncClient):
    response = await auth_client.post(
        "/product/",
        json={"name": "Wireless Mouse", "price": 29.99, "stock": 50},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Wireless Mouse"
    assert data["price"] == 29.99
    assert data["stock"] == 50
    assert "id" in data


@pytest.mark.asyncio
async def test_create_product_validation_error(auth_client: AsyncClient):
    # Invalid price (must be > 0)
    response = await auth_client.post(
        "/product/",
        json={"name": "Cheap Item", "price": -5.0, "stock": 10},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_product_success(auth_client: AsyncClient):
    create_res = await auth_client.post(
        "/product/",
        json={"name": "Mechanical Keyboard", "price": 89.99, "stock": 20},
    )
    product_id = create_res.json()["id"]

    response = await auth_client.get(f"/product/?id={product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product_id
    assert data["name"] == "Mechanical Keyboard"


@pytest.mark.asyncio
async def test_get_product_not_found(auth_client: AsyncClient):
    response = await auth_client.get("/product/?id=99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"


@pytest.mark.asyncio
async def test_patch_product_success(auth_client: AsyncClient):
    create_res = await auth_client.post(
        "/product/",
        json={"name": "Gaming Monitor", "price": 199.99, "stock": 15},
    )
    product_id = create_res.json()["id"]

    # Partial update price & stock
    patch_res = await auth_client.patch(
        f"/product/?id={product_id}",
        json={"price": 179.99, "stock": 10},
    )
    assert patch_res.status_code == 200
    updated = patch_res.json()
    assert updated["price"] == 179.99
    assert updated["stock"] == 10
    assert updated["name"] == "Gaming Monitor"


@pytest.mark.asyncio
async def test_patch_product_empty_body(auth_client: AsyncClient):
    create_res = await auth_client.post(
        "/product/",
        json={"name": "USB Cable", "price": 9.99, "stock": 100},
    )
    product_id = create_res.json()["id"]

    response = await auth_client.patch(f"/product/?id={product_id}", json={})
    assert response.status_code == 400
    assert response.json()["detail"] == "No data provided"


@pytest.mark.asyncio
async def test_patch_product_not_found(auth_client: AsyncClient):
    response = await auth_client.patch(
        "/product/?id=99999",
        json={"price": 50.0},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"


@pytest.mark.asyncio
async def test_delete_product_success(auth_client: AsyncClient):
    create_res = await auth_client.post(
        "/product/",
        json={"name": "Desk Lamp", "price": 24.99, "stock": 30},
    )
    product_id = create_res.json()["id"]

    delete_res = await auth_client.delete(f"/product/?id={product_id}")
    assert delete_res.status_code == 200
    assert delete_res.json()["message"] == f"Product {product_id} deleted successfully"

    # Confirm product is gone
    get_res = await auth_client.get(f"/product/?id={product_id}")
    assert get_res.status_code == 404


@pytest.mark.asyncio
async def test_delete_product_not_found(auth_client: AsyncClient):
    response = await auth_client.delete("/product/?id=99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"
