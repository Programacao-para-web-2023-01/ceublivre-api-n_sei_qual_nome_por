from sqlalchemy.orm import Session
from typing import List
from sql_app.config import HOST, USERNAME, PASSWORD, PORT
from ssl import create_default_context
from email.mime.text import MIMEText
from smtplib import SMTP
from . import models, schemas, mail


# Create


def create_pedido(
        db: Session,
        pedido: schemas.PedidoCreate,
        db_produtos: List[schemas.Produto]
):
    db_pedido = models.Pedido(**pedido.dict())
    db_pedido.produtos = db_produtos
    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)
    return db_pedido


# Read


def get_produto(db: Session, produto_id: int):
    return (db
            .query(models.Produto)
            .filter(models.Produto.id == produto_id)
            .first())


def get_produtos(db: Session):
    products = db.query(models.Produto).all()
    return products


def get_pedidos(db: Session):
    pedidos = db.query(models.Pedido).all()
    return pedidos


# Update


def update_pedido(
        db: Session,
        pedido_id: int,
        pedido_update: schemas.PedidoUpdate
):
    db_pedido = (db
                 .query(models.Pedido)
                 .filter(models.Pedido.id == pedido_id)
                 .first())
    if not db_pedido:
        return None
    db_pedido.endereco_entrega = pedido_update.endereco_entrega
    db.commit()
    db.refresh(db_pedido)
    return db_pedido


def update_produto(db: Session, produto_id: int, updated_data: dict):
    db_produto = db.query(models.Produto).get(produto_id)
    for key, value in updated_data.items():
        setattr(db_produto, key, value)
    db.commit()
    db.refresh(db_produto)
    return db_produto

#Email

def send_mail(data:dict|None=None):
    msg = mail.MailBodyModel(**data)
    message = MIMEText(msg.body, "html")
    message["From"] = USERNAME
    message["To"] = ",".join(msg.to)
    message["Subject"] = msg.subject

    ctx = create_default_context()

    try:
        with SMTP(HOST, PORT) as server:
            server.ehlo()
            server.starttls(context=ctx)
            server.login(USERNAME, PASSWORD)
            server.send_message(message)
            server.quit()
        return {"status": 200, "errors": None}
    except Exception as e:
        return {"status": 500, "errors": e}


