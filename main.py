from typing import List

from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from sql_app import models, schemas, crud, mail
from sql_app.database import SessionLocal

app = FastAPI()


# Dependency for getting a database session
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# Create


@app.post("/pedidos/")
def create_pedido(pedido: schemas.PedidoCreate,
                  ids_produtos: List[int],
                  db: Session = Depends(get_db)):
    # Gets list of produtos from database
    db_produtos = []
    for id_produto in ids_produtos:
        db_produto = crud.get_produto(db, id_produto)
        if not db_produto:
            raise HTTPException(status_code=404,
                                detail=f"Produto {id_produto} não encontrado")
        db_produtos.append(db_produto)

    for produto in db_produtos:
        novo_estoque = produto.estoque - 1  # Subtrai 1 do estoque atual
        crud.update_produto(db, produto.id, {"estoque": novo_estoque})

    db_pedido = crud.create_pedido(db, pedido, db_produtos)

    return db_pedido


@app.post("/products")
def create_product(product: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    return crud.create_product(product, db)


# Update


@app.put("/pedidos/{pedido_id}")
def update_pedido(pedido_id: int,
                  pedido_update: schemas.PedidoUpdate,
                  db: Session = Depends(get_db)):
    pedido = crud.update_pedido(db, pedido_id, pedido_update)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    return pedido


# Read


@app.get("/products", response_model=List[schemas.Produto])
def get_produtos(db: Session = Depends(get_db)):
    products = db.query(models.Produto).all()
    return products


@app.get("/pedidos/", response_model=List[schemas.Pedido])
def get_pedidos(db: Session = Depends(get_db)):
    pedidos = db.query(models.Pedido).all()
    return pedidos


# Send_Email


@app.post("/send-email")
def schedule_mail(req: mail.MailBodyModel, tasks: BackgroundTasks):
    data = req.dict()
    tasks.add_task(crud.send_mail, data)
    return {"status": 200, "message": "email has been scheduled"}
