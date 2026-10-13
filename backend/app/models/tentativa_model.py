from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer
from sqlalchemy.sql import func

from app.core.database import Base


class Tentativa(Base):
    """Cada envio de progresso (uma tentativa de resolver uma fase)."""

    __tablename__ = "tentativas"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    fase_id = Column(Integer, nullable=False, index=True)
    concluida = Column(Boolean, nullable=False, default=False)
    movimentos = Column(Integer, nullable=False, default=0)
    tempo_segundos = Column(Integer, nullable=False, default=0)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())