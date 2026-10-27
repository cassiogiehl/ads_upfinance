"""T012 · US3 · GET /categorias and GET /pilares (RF003, RN001, RN002, RN004)."""

from collections import defaultdict
from typing import Any

import pytest
from fastapi.testclient import TestClient

from tests.conftest import API

# Seed catalog from research R2
CATALOGO: dict[str | None, set[str]] = {
    "ESSENCIAL": {
        "Moradia",
        "Contas da casa (água, luz, gás, internet)",
        "Alimentação (mercado)",
        "Transporte",
        "Saúde",
        "Educação",
    },
    "PESSOAL": {
        "Lazer",
        "Restaurantes e delivery",
        "Compras",
        "Assinaturas",
        "Viagens",
        "Cuidados pessoais",
    },
    "FUTURO": {
        "Investimentos",
        "Reserva de emergência",
        "Previdência",
        "Pagamento de dívidas",
    },
    None: {"Salário", "Renda extra", "Outras entradas"},
}


def _categorias(client: TestClient, headers: dict[str, str], **params: str) -> list[Any]:
    resp = client.get(f"{API}/categorias", headers=headers, params=params)
    assert resp.status_code == 200, resp.text
    body: list[Any] = resp.json()
    return body


def test_categorias_match_the_seeded_catalog(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    por_pilar: dict[str | None, set[str]] = defaultdict(set)
    for c in _categorias(client, auth_headers):
        assert set(c) == {"id", "nome", "tipo", "pilar"}
        por_pilar[c["pilar"]].add(c["nome"])

    assert por_pilar == CATALOGO


def test_saida_categories_have_a_pilar_and_entrada_have_none(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    for c in _categorias(client, auth_headers):
        if c["tipo"] == "SAIDA":
            assert c["pilar"] in {"ESSENCIAL", "PESSOAL", "FUTURO"}, c
        else:
            assert c["tipo"] == "ENTRADA"
            assert c["pilar"] is None, c


def test_every_pilar_has_at_least_one_category(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    pilares = {c["pilar"] for c in _categorias(client, auth_headers)}

    assert {"ESSENCIAL", "PESSOAL", "FUTURO"} <= pilares


@pytest.mark.parametrize("tipo", ["ENTRADA", "SAIDA"])
def test_categorias_filter_by_tipo(
    client: TestClient, auth_headers: dict[str, str], tipo: str
) -> None:
    filtradas = _categorias(client, auth_headers, tipo=tipo)

    assert filtradas
    assert {c["tipo"] for c in filtradas} == {tipo}
    todas = _categorias(client, auth_headers)
    assert len(filtradas) == sum(1 for c in todas if c["tipo"] == tipo)


def test_categorias_invalid_tipo_is_422(client: TestClient, auth_headers: dict[str, str]) -> None:
    resp = client.get(f"{API}/categorias", headers=auth_headers, params={"tipo": "OUTRO"})

    assert resp.status_code == 422
    assert resp.json()["code"] == "DADOS_INVALIDOS"


def test_categorias_require_authentication(client: TestClient) -> None:
    resp = client.get(f"{API}/categorias")

    assert resp.status_code == 401
    assert resp.json()["code"] == "NAO_AUTENTICADO"


@pytest.mark.parametrize("method", ["post", "put", "patch", "delete"])
def test_categorias_are_read_only(
    client: TestClient, auth_headers: dict[str, str], method: str
) -> None:
    # US3-3: categories are provided by the system
    resp = client.request(method.upper(), f"{API}/categorias", headers=auth_headers, json={})

    assert resp.status_code == 405


def test_pilares_are_fixed(client: TestClient, auth_headers: dict[str, str]) -> None:
    resp = client.get(f"{API}/pilares", headers=auth_headers)

    assert resp.status_code == 200
    assert resp.json() == [
        {"pilar": "ESSENCIAL", "percentual": "0.50", "label": "Essencial"},
        {"pilar": "PESSOAL", "percentual": "0.30", "label": "Pessoal"},
        {"pilar": "FUTURO", "percentual": "0.20", "label": "Futuro"},
    ]
