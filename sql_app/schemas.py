from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, EmailStr


# PEDIDO


class PedidoBase(BaseModel):
    valor_total: Optional[Decimal]
    valor_frete: Optional[Decimal]
    endereco_entrega: str
    status: str


class PedidoCreate(PedidoBase):
    pass


class PedidoUpdate(BaseModel):
    valor_total: Optional[Decimal]
    valor_frete: Optional[Decimal]
    endereco_entrega: str
    status: str

class Pedido(PedidoBase):
    id: int
    criado_em: datetime
    produtos: List['Produto'] = []

    class Config:
        orm_mode = True


# PRODUTO


class ProdutoBase(BaseModel):
    nome: str
    preco: int
    estoque: Optional[Decimal]


class ProdutoCreate(ProdutoBase):
    pass


class Produto(ProdutoBase):
    id: int

    class Config:
        orm_mode = True


class MailBody(BaseModel):
    email: List[EmailStr]


Pedido.update_forward_refs(Pedido=Pedido)
