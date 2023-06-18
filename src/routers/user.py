from typing import Union

from fastapi import APIRouter, Depends, Path, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import engine, get_db
from modelos.schemas import template_put
from models import Base, User

router = APIRouter()


class UserTemplate(BaseModel):
    matricula: str | None = None
    name: str | None = None
    endereco: str | None = None
    rg: str | None = None
    password: str
    active: bool = True
    updated_at: str | None = None
    acess: str

    class Config:
        schema_extra = {
            "example": {
                "matricula": "001",
                "name": "Estagiario",
                "endereco": "Rua tal de tal",
                "rg": "11111111",
                "password": "Problema123",
                "acess": "basic",
            }
        }


Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(passe):
    return pwd_context.hash(passe)


response_unauthorized = JSONResponse({
    "message": "Acesso negado",
    "error": True,
    "data": None,

}, status.HTTP_401_UNAUTHORIZED)


@router.get("/user", tags=["User"])
async def get_user(db: Session = Depends(get_db),
                   username: Union[str, None] = None,
                   ):

    try:
        if username:
            user = db.query(User).filter(User.username ==
                                         username, User.active == True).one_or_none()  # noqa 712 noqa 501
            if not user:
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content={
                        "message": "Nenhum usuário encontrado.",
                        "error": None,
                        "data": [],
                    }
                )
            else:
                all_data = user

        else:
            all_data = db.query(User).filter_by(active=True).all()
        all_data_json = jsonable_encoder(all_data)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "dados buscados com sucesso",
                "error": None,
                "data": all_data_json,
            },
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "Erro ao obter dados",
                "error": str(e),
                "data": None,
            },
        )


@router.post("/user", tags=["User"])
async def post_user(data: UserTemplate,
                    db: Session = Depends(get_db)):
    try:
        username = (
            db.query(User)
            .filter(User.username == data.username)
            .one_or_none()
        )

        if username:
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={
                    "message": "O username já está em uso",
                    "error": None,
                    "data": None,
                },
            )
        email = db.query(User).filter(
            User.email == data.email).one_or_none()
        if email:
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={
                    "message": "O email já está em uso",
                    "error": None,
                    "data": None,
                },
            )

        else:
            new_object = User(**data.dict())
            new_object.password = str(get_password_hash(new_object.password))
            new_object.username = new_object.username.strip()
            new_object.name = new_object.name.strip()
            db.add(new_object)
            db.commit()
            db.refresh(new_object)

            new_object.updated_at = str(new_object.updated_at)

            new_object_json = jsonable_encoder(new_object)

            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={
                    "message": "Dados cadastrados com sucesso",
                    "error": None,
                    "data": new_object_json,
                },
            )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "Erro ao inserir dados",
                "error": str(e),
                "data": None,
            },
        )


@router.delete("/user/{username}", tags=["User"])
async def delete_user(username: str,
                      db: Session = Depends(get_db)):

    try:
        user = (
            db.query(User)
            .filter(User.username == username)
            .first()
        )
        if user:
            user.active = False
            db.commit()
            return JSONResponse(
                status_code=200,
                content={
                    "message": "Dados deletados com sucesso",
                    "error": None,
                    "data": None,
                },
            )

        else:
            return JSONResponse(
                status_code=200,
                content={
                    "message": "Usuario não encontrado",
                    "error": None,
                    "data": None,
                },
            )

    except Exception as e:
        return JSONResponse(
            status_code=404,
            content={
                "message": "Erro ao processar dados",
                "error": str(e),
                "data": None,
            },
        )


@router.put("/user/{username}", tags=["User"])
async def update_user(
    data: template_put.UserTemp,
    username: str = Path(title="Username"),
    db: Session = Depends(get_db),
):
    if data.password:
        data.password = str(get_password_hash(data.password))

    if data.username:
        data.username = data.username.strip()

    if data.name:
        data.name = data.name.strip()

    if data.username != username:
        if (db.query(User).filter(
                User.username == data.username).one_or_none()):
            return JSONResponse(
                content={
                    "message": "Usuário já cadastrado",
                    "error": None,
                    "data": None,
                }, status_code=status.HTTP_409_CONFLICT
            )

    try:
        user = db.query(User).filter(User.username == username).update(
            data.dict(exclude_none=True))
        print(user)
        if user:
            db.commit()
            if data.username:
                user = (
                    db.query(
                        User).filter_by(
                        username=data.username).first())

            else:
                user = (
                    db.query(
                        User).filter_by(
                        username=username).first())
            user = jsonable_encoder(user)
            response_data = jsonable_encoder(
                {
                    "message": "Dado atualizado com sucesso",
                    "error": None,
                    "data": user,
                }
            )

            return JSONResponse(
                content=response_data, status_code=status.HTTP_200_OK
            )
        else:
            response_data = jsonable_encoder(
                {
                    "message": "Dado não encontrado na base",
                    "error": None,
                    "data": None,
                }
            )

            return JSONResponse(
                content=response_data,
                status_code=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "Erro ao processar dados",
                "error": str(e),
                "data": None,
            },
        )
