from pydantic import BaseModel


class UserTemp(BaseModel):
    matricula: str | None = None
    endereco: str | None = None
    name: str | None = None
    rg: str | None = None
    password: str | None = None
    active: bool = True
    updated_at: str | None = None
    acess: str | None = None

class DisciplinaTemp(BaseModel):
    codigo: str | None = None
    nome: str | None = None
    horario: str | None = None
    turma: str | None = None