"""T010 · US1 · POST /auth/register (contracts/openapi.yaml)."""

from typing import Any

import pytest
from fastapi.testclient import TestClient

from tests.conftest import API

URL = f"{API}/auth/register"


def _payload(**overrides: Any) -> dict[str, Any]:
    return {"nome": "Rafael", "email": "rafael@example.com", "senha": "senha1234", **overrides}


def test_register_creates_account_and_signs_in(client: TestClient) -> None:
    resp = client.post(URL, json=_payload())

    assert resp.status_code == 201
    body = resp.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]
    assert body["usuario"] == {"id": body["usuario"]["id"], "nome": "Rafael",
                               "email": "rafael@example.com"}


def test_register_never_returns_the_password(client: TestClient) -> None:
    resp = client.post(URL, json=_payload())

    assert resp.status_code == 201
    assert "senha" not in resp.text
    assert "senha_hash" not in resp.text


def test_register_normalizes_email_and_trims_name(client: TestClient) -> None:
    resp = client.post(URL, json=_payload(nome="  Rafael  ", email="  Rafael@Example.COM "))

    assert resp.status_code == 201
    assert resp.json()["usuario"]["nome"] == "Rafael"
    assert resp.json()["usuario"]["email"] == "rafael@example.com"


def test_register_token_gives_access_to_me(client: TestClient) -> None:
    token = client.post(URL, json=_payload()).json()["access_token"]

    resp = client.get(f"{API}/usuarios/me", headers={"Authorization": f"Bearer {token}"})

    assert resp.status_code == 200
    assert resp.json()["email"] == "rafael@example.com"


@pytest.mark.parametrize("email", ["rafael@example.com", "RAFAEL@example.com"])
def test_register_duplicate_email_is_refused(client: TestClient, email: str) -> None:
    client.post(URL, json=_payload())

    resp = client.post(URL, json=_payload(nome="Outro", email=email))

    assert resp.status_code == 409
    assert resp.json()["code"] == "EMAIL_JA_CADASTRADO"
    assert resp.json()["message"] == "Este e-mail já está cadastrado"


@pytest.mark.parametrize(
    ("overrides", "campo"),
    [
        ({"nome": ""}, "nome"),
        ({"nome": "   "}, "nome"),
        ({"email": "nao-e-email"}, "email"),
        ({"senha": "curta12"}, "senha"),  # FR-008: at least 8 characters
    ],
)
def test_register_invalid_field_is_identified(
    client: TestClient, overrides: dict[str, Any], campo: str
) -> None:
    resp = client.post(URL, json=_payload(**overrides))

    assert resp.status_code == 422
    assert resp.json()["code"] == "DADOS_INVALIDOS"
    assert campo in resp.json()["details"]["campos"]


@pytest.mark.parametrize("missing", ["nome", "email", "senha"])
def test_register_missing_field_is_identified(client: TestClient, missing: str) -> None:
    payload = _payload()
    del payload[missing]

    resp = client.post(URL, json=payload)

    assert resp.status_code == 422
    assert resp.json()["code"] == "DADOS_INVALIDOS"
    assert missing in resp.json()["details"]["campos"]
