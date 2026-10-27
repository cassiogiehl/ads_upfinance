from fastapi.testclient import TestClient

from tests.conftest import API


def test_unknown_route_uses_error_shape(client: TestClient) -> None:
    resp = client.get(f"{API}/nao-existe")

    assert resp.status_code == 404
    assert resp.json() == {
        "code": "NAO_ENCONTRADO",
        "message": "Recurso não encontrado.",
        "details": {},
    }
