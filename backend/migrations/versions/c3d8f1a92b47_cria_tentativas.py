"""cria tabela tentativas

Revision ID: c3d8f1a92b47
Revises: a1c4e7f20b35
Create Date: 2026-10-12

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "c3d8f1a92b47"
down_revision: Union[str, None] = "a1c4e7f20b35"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "tentativas",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("fase_id", sa.Integer(), nullable=False),
        sa.Column("concluida", sa.Boolean(), nullable=False),
        sa.Column("movimentos", sa.Integer(), nullable=False),
        sa.Column("tempo_segundos", sa.Integer(), nullable=False),
        sa.Column("criado_em", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_tentativas_id"), "tentativas", ["id"], unique=False)
    op.create_index(op.f("ix_tentativas_user_id"), "tentativas", ["user_id"], unique=False)
    op.create_index(op.f("ix_tentativas_fase_id"), "tentativas", ["fase_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_tentativas_fase_id"), table_name="tentativas")
    op.drop_index(op.f("ix_tentativas_user_id"), table_name="tentativas")
    op.drop_index(op.f("ix_tentativas_id"), table_name="tentativas")
    op.drop_table("tentativas")