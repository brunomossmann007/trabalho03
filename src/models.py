import enum

from sqlalchemy import TIMESTAMP, Boolean, Column, Enum, String, Text
from sqlalchemy.sql import func

from database import Base


class AcessEnum(str, enum.Enum):
    basic = "basic"
    manager = "manager"
    admin = "admin"


class User(Base):
    __tablename__ = "user"

    matricula = Column(String(100), nullable=False, primary_key=True)
    endereco = Column(String(250), nullable=False)
    name = Column(String(250), nullable=False)
    rg = Column(String(100))
    password = Column(Text, nullable=False)
    active = Column(Boolean, default=True)
    updated_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        server_onupdate=func.current_timestamp(),
    )
    acess = Column(Enum(AcessEnum), nullable=False, default=AcessEnum.basic)

class Disciplina(Base):
    __tablename__ = "disciplina"

    codigo = Column(String(8), nullable=False, primary_key=True)
    nome = Column(String(250), nullable=False)
    horario = Column(String(1), nullable=False)
    turma = Column(String(250), nullable=False)