from dataclasses import dataclass, field
from typing import ClassVar

@dataclass
class Produto:
    nome: str
    preço: float
    codigo: int = field(init=False)
    _proximo_codigo: ClassVar[int] = 1  # Class variable to auto-increment codigo

    def __post_init__(self):
        # Assign a unique code upon initialization
        self.codigo = Produto._proximo_codigo
        Produto._proximo_codigo += 1

    def __str__(self) -> str:
        return f'Código: {self.codigo} 
Nome: {self.nome} 
Preço: {self.preço}'
