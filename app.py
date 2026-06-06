from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from config.database import get_db
from repositories.produto_repository import ProdutoRepository

app = FastAPI(
    title="DigitalTech — Agente ADS",
    description="API de produtos com arquitetura em camadas — Michel Freitas",
    version="1.0.0"
)


# Schema [estrutura de validação] dos dados de entrada
class ProdutoInput(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    descricao: str = Field(default="")
    preco: float = Field(..., gt=0)
    estoque: int = Field(..., ge=0)


@app.get("/health")
def health_check():
    """Verifica se a API está no ar"""
    return {"status": "ok", "projeto": "DigitalTech ADS"}


@app.get("/produtos")
def listar_produtos(db: Session = Depends(get_db)):
    repo = ProdutoRepository(db)
    produtos = repo.listar_todos()
    return {"produtos": [dict(p._mapping) for p in produtos]}


@app.get("/produtos/{produto_id}")
def buscar_produto(produto_id: int, db: Session = Depends(get_db)):
    repo = ProdutoRepository(db)
    produto = repo.buscar_por_id(produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return dict(produto._mapping)


@app.post("/produtos", status_code=201)
def criar_produto(dados: ProdutoInput, db: Session = Depends(get_db)):
    repo = ProdutoRepository(db)
    repo.criar(dados.nome, dados.descricao, dados.preco, dados.estoque)
    return {"mensagem": "Produto criado com sucesso"}


@app.put("/produtos/{produto_id}")
def atualizar_produto(produto_id: int, dados: ProdutoInput, db: Session = Depends(get_db)):
    repo = ProdutoRepository(db)
    produto = repo.buscar_por_id(produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    repo.atualizar(produto_id, dados.nome, dados.descricao, dados.preco, dados.estoque)
    return {"mensagem": "Produto atualizado com sucesso"}


@app.delete("/produtos/{produto_id}")
def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    repo = ProdutoRepository(db)
    produto = repo.buscar_por_id(produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    repo.deletar(produto_id)
    return {"mensagem": "Produto desativado com sucesso"}
