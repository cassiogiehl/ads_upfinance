"""usuario and categoria tables, plus the category seed (research R2)

Revision ID: 0001
Revises:
Create Date: 2026-10-26
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

TIPOS = ("ENTRADA", "SAIDA")
PILARES = ("ESSENCIAL", "PESSOAL", "FUTURO")

CATEGORIAS: list[tuple[str, str, str | None]] = [
    ("Moradia", "SAIDA", "ESSENCIAL"),
    ("Contas da casa (água, luz, gás, internet)", "SAIDA", "ESSENCIAL"),
    ("Alimentação (mercado)", "SAIDA", "ESSENCIAL"),
    ("Transporte", "SAIDA", "ESSENCIAL"),
    ("Saúde", "SAIDA", "ESSENCIAL"),
    ("Educação", "SAIDA", "ESSENCIAL"),
    ("Lazer", "SAIDA", "PESSOAL"),
    ("Restaurantes e delivery", "SAIDA", "PESSOAL"),
    ("Compras", "SAIDA", "PESSOAL"),
    ("Assinaturas", "SAIDA", "PESSOAL"),
    ("Viagens", "SAIDA", "PESSOAL"),
    ("Cuidados pessoais", "SAIDA", "PESSOAL"),
    ("Investimentos", "SAIDA", "FUTURO"),
    ("Reserva de emergência", "SAIDA", "FUTURO"),
    ("Previdência", "SAIDA", "FUTURO"),
    ("Pagamento de dívidas", "SAIDA", "FUTURO"),
    ("Salário", "ENTRADA", None),
    ("Renda extra", "ENTRADA", None),
    ("Outras entradas", "ENTRADA", None),
]


def upgrade() -> None:
    op.create_table(
        "usuario",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("nome", sa.String(120), nullable=False),
        sa.Column("email", sa.String(254), nullable=False, unique=True),
        sa.Column("senha_hash", sa.String(255), nullable=False),
        sa.Column(
            "criado_em", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
        ),
    )

    categoria = op.create_table(
        "categoria",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("nome", sa.String(80), nullable=False, unique=True),
        sa.Column("tipo", sa.String(7), nullable=False),
        sa.Column("pilar", sa.String(9), nullable=True),
        sa.CheckConstraint(f"tipo IN {TIPOS}", name="ck_tipo"),
        sa.CheckConstraint(f"pilar IN {PILARES}", name="ck_pilar"),
        sa.CheckConstraint(
            "(tipo = 'SAIDA' AND pilar IS NOT NULL) OR (tipo = 'ENTRADA' AND pilar IS NULL)",
            name="ck_categoria_pilar_por_tipo",
        ),
    )

    op.bulk_insert(
        categoria,
        [{"nome": nome, "tipo": tipo, "pilar": pilar} for nome, tipo, pilar in CATEGORIAS],
    )


def downgrade() -> None:
    op.drop_table("categoria")
    op.drop_table("usuario")
