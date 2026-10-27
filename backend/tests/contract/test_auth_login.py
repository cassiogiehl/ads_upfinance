"""T011 · US2 · POST /auth/login and GET /usuarios/me (contracts/openapi.yaml)."""

import pytest
from fastapi.testclient import TestClient

from tests.conftest import API

LOGIN = f"{API}/auth/login"
ME = f"{API}/usuarios/me"


@pytest.fixture
def registered(client: TestClient) -> None:
    resp = client.post(
        f"{API}/auth/register",
        json={"nome": "Rafael", "email": "rafael@example.com", "senha": "senha1234"},
    )
    assert resp.status_code == 201, resp.text


@pytest.mark.usefixtures("registered")
@pytest.mark.parametrize("email", ["rafael@example.com", "  RAFAEL@Example.com "])
def test_login_with_correct_credentials(client: TestClient, email: str) -> None:
    resp = client.post(LOGIN, json={"email": email, "senha": "senha1234"})

    assert resp.status_code == 200
    body = resp.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]
    assert body["usuario"]["email"] == "rafael@example.com"


@pytest.mark.usefixtures("registered")
def test_login_failures_share_one_generic_message(client: TestClient) -> None:
    wrong_password = client.post(LOGIN, json={"email": "rafael@example.com", "senha": "errada123"})
    unknown_email = client.post(LOGIN, json={"email": "ninguem@example.com", "senha": "senha1234"})

    for resp in (wrong_password, unknown_email):
        assert resp.status_code == 401
        assert resp.json()["code"] == "CREDENCIAIS_INVALIDAS"
    # US2-2: the response must not reveal whether the email exists
    assert wrong_password.json() == unknown_email.json()


def test_me_returns_the_signed_in_user(client: TestClient, auth_headers: dict[str, str]) -> None:
    resp = client.get(ME, headers=auth_headers)

    assert resp.status_code == 200
    body = resp.json()
    assert body["nome"] == "Rafael"
    assert body["email"] == "rafael@example.com"
    assert "senha_hash" not in body


@pytest.mark.parametrize(
    "headers",
    [
        {},
        {"Authorization": "Bearer nao-e-um-jwt"},
        {"Authorization": "Basic cmFmYWVsOnNlbmhh"},
    ],
)
def test_me_without_a_valid_token_is_401(client: TestClient, headers: dict[str, str]) -> None:
    resp = client.get(ME, headers=headers)

    assert resp.status_code == 401
    assert resp.json()["code"] == "NAO_AUTENTICADO"
