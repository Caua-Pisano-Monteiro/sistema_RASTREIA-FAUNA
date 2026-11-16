import datetime as dt
import bcrypt
from sqlalchemy import select
from fastapi import FastAPI, Depends, HTTPException 
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import usuario_login, apreensao_fauna
from schema import LoginRequest, usuario_loginCreate
import models
import schema
from typing import List

models.Base.metadata.create_all(bind=engine)

app= FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/login")
def login(dados: LoginRequest, db: Session = Depends(get_db)):
    user = db.scalar(
        select(usuario_login).where(usuario_login.username == dados.username)
    )

    if (
        not user
        or not user.ativo
        or not bcrypt.checkpw(dados.password.encode(), user.password.encode())
    ):
        raise HTTPException(status_code=401, detail="Usuário ou senha incorretos")

    return {"ok": True, "username": user.username, "funcao": user.funcao}


@app.post("/usuarios")
def criar_usuario(dados: usuario_loginCreate, db: Session = Depends(get_db)):
    if db.scalar(select(usuario_login).where(
    (usuario_login.username == dados.username) | (usuario_login.email == dados.email))):
        raise HTTPException(status_code=400, detail="Usuário ou e-mail já existe")

    novo = usuario_login(
        username=dados.username,
        email=dados.email,
        funcao=dados.funcao,
        password=bcrypt.hashpw(dados.password.encode(), bcrypt.gensalt()).decode(),
    )
    db.add(novo)
    db.commit()
    return {"ok": True}

@app.get("/data-usuarios", response_model=list[schema.usuario_loginResponse])
def read_usuarios(db: Session = Depends(get_db)):
    return db.scalars(select(usuario_login)).all()

@app.get("/data-request", response_model= List[schema.ApreensaoFaunaBase])
def read_fauna(db: Session = Depends(get_db)):
    return db.scalars(select(apreensao_fauna)).all()

@app.post("/formulario-apreensao", response_model=schema.ApreensaoFaunaBase, status_code=201)
def Create_apreensao(dados : schema.ApreensaoFaunaCreate, db : Session = Depends(get_db)):
    apreensao_create = db.get(models.apreensao_fauna, dados.seq_apreensao)
    if apreensao_create:
        raise HTTPException(status_code=400, detail="Já existe uma apreensão com este código (seq_apreensao)")

    # Cria a instância do modelo desempacotando o dicionário do Pydantic
    db_apreensao = models.apreensao_fauna(**dados.model_dump())
    
    db.add(db_apreensao)
    db.commit()
    db.refresh(db_apreensao)
    
    return db_apreensao