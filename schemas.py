from pydantic import BaseModel
from typing import List, Optional

class ProdutoBase(BaseModel):
    nome: str
    preço: float

class ProdutoCreate(ProdutoBase):
    pass # Inherits fields from ProdutoBase

class ProdutoResponse(ProdutoBase):
    codigo: int

    class Config:
        orm_mode = True

class CartItemSchema(BaseModel):
    produto: ProdutoResponse
    quantidade: int

class CarrinhoResponse(BaseModel):
    items: List[CartItemSchema]
    valor_total: Optional[float] = None
