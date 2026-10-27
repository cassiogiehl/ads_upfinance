from fastapi import APIRouter

from app.deps import CurrentUser
from app.domain.enums import Pilar
from app.schemas.categoria import PilarInfo

router = APIRouter(prefix="/pilares", tags=["pilares"])


@router.get("")
def listar(_: CurrentUser) -> list[PilarInfo]:
    return [PilarInfo(pilar=p, percentual=str(p.percentual), label=p.label) for p in Pilar]
