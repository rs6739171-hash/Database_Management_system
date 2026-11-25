import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_seller_signup_success(client: AsyncClient):
    response = await client.post(
        "/seller/signup",
        json={
            "name": "Jane Seller",
            "email": "jane@example.com",
            "password": "securepassword123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Jane Seller"
    assert data["email"] == "jane@example.com"
    assert "id" in data
    assert "password_hash" in data
    # Password should be hashed, not plaintext
    assert data["password_hash"] != "securepassword123"


@pytest.mark.asyncio
async def test_seller_signup_invalid_email(client: AsyncClient):
    response = await client.post(
        "/seller/signup",
        json={
            "name": "Bad Email",
            "email": "not-an-email",
            "password": "password123",
        },
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_seller_login_success(client: AsyncClient):
    # Register first
    await client.post(
        "/seller/signup",
        json={
            "name": "Login User",
            "email": "loginuser@example.com",
            "password": "mypassword123",
        },
    )

    # Login with form data
    response = await client.post(
        "/seller/login",
        data={"username": "loginuser@example.com", "password": "mypassword123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_seller_login_wrong_password(client: AsyncClient):
    await client.post(
        "/seller/signup",
        json={
            "name": "Wrong Pass User",
            "email": "wrongpass@example.com",
            "password": "correctpassword",
        },
    )

    response = await client.post(
        "/seller/login",
        data={"username": "wrongpass@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Email or Password is not correct"


@pytest.mark.asyncio
async def test_seller_login_nonexistent_email(client: AsyncClient):
    response = await client.post(
        "/seller/login",
        data={"username": "nonexistent@example.com", "password": "password123"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Email or Password is not correct"


@pytest.mark.asyncio
async def test_seller_dashboard_authorized(client: AsyncClient):
    # Register seller
    await client.post(
        "/seller/signup",
        json={
            "name": "Dashboard User",
            "email": "dash@example.com",
            "password": "dashpassword",
        },
    )

    # Login to get token
    login_res = await client.post(
        "/seller/login",
        data={"username": "dash@example.com", "password": "dashpassword"},
    )
    token = login_res.json()["access_token"]

    # Access dashboard with token
    response = await client.get(
        "/seller/dashboard",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["Status"] == "Successfully Logged In"
    assert data["Details"]["email"] == "dash@example.com"


@pytest.mark.asyncio
async def test_seller_dashboard_unauthorized_missing_token(client: AsyncClient):
    response = await client.get("/seller/dashboard")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_seller_dashboard_invalid_token(client: AsyncClient):
    response = await client.get(
        "/seller/dashboard",
        headers={"Authorization": "Bearer invalid.token.here"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_seller_dashboard_blacklisted_token(client: AsyncClient):
    from unittest.mock import AsyncMock, patch

    await client.post(
        "/seller/signup",
        json={
            "name": "BL User",
            "email": "bl@example.com",
            "password": "blpassword",
        },
    )
    login_res = await client.post(
        "/seller/login",
        data={"username": "bl@example.com", "password": "blpassword"},
    )
    token = login_res.json()["access_token"]

    with patch("app.api.dependencies.is_jti_blacklisted", new_callable=AsyncMock) as mock_bl:
        mock_bl.return_value = True
        response = await client.get(
            "/seller/dashboard",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid Token"


@pytest.mark.asyncio
async def test_seller_logout_success(client: AsyncClient):
    await client.post(
        "/seller/signup",
        json={
            "name": "Logout User",
            "email": "logout@example.com",
            "password": "logoutpass123",
        },
    )
    login_res = await client.post(
        "/seller/login",
        data={"username": "logout@example.com", "password": "logoutpass123"},
    )
    token = login_res.json()["access_token"]

    response = await client.get(
        "/seller/logout",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Logout Successful"


@pytest.mark.asyncio
async def test_seller_logout_unauthorized(client: AsyncClient):
    response = await client.get("/seller/logout")
    assert response.status_code == 401
