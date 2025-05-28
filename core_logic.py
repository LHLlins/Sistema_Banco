from Models.produto import Produto
from typing import List, Dict, Optional # Optional is a more idiomatic way to say "X | None"

produtos: List[Produto] = []
# The carrinho should store Produto objects as keys and their quantity as values.
# Using Dict[Produto, int] directly in the list.
carrinho: List[Dict[Produto, int]] = []

def cadastrar_produto_core(nome: str, preco: float) -> Produto:
    """
    Creates a Produto object, adds it to the global 'produtos' list,
    and returns the created Produto object.
    """
    produto = Produto(nome=nome, preço=preco) # Use named arguments for clarity
    produtos.append(produto)
    return produto

def listar_produtos_core() -> List[Produto]:
    """Returns the global 'produtos' list."""
    return produtos

def pegar_produto_por_codigo_core(codigo: int) -> Optional[Produto]:
    """
    Iterates through the 'produtos' list and returns the Produto object
    if found, otherwise returns None.
    """
    for produto in produtos:
        if produto.codigo == codigo:
            return produto
    return None

def comprar_produto_core(codigo: int) -> tuple[str, Optional[Dict[Produto, int]]]:
    """
    Handles the logic for buying a product.
    Uses pegar_produto_por_codigo_core to find the product.
    Updates the 'carrinho' list.
    Returns a status message and the updated cart item or None.
    """
    produto_obj = pegar_produto_por_codigo_core(codigo)

    if not produto_obj:
        return f"Produto com código {codigo} não encontrado.", None

    # Check if product is already in cart
    for item_dict in carrinho:
        if produto_obj in item_dict: # product_obj is the key we are looking for
            item_dict[produto_obj] += 1
            return f"Quantidade do produto '{produto_obj.nome}' atualizada no carrinho.", item_dict

    # If not found in cart, add as a new item
    novo_item_carrinho = {produto_obj: 1}
    carrinho.append(novo_item_carrinho)
    return f"Produto '{produto_obj.nome}' adicionado ao carrinho.", novo_item_carrinho

def visualizar_carrinho_core() -> List[Dict[Produto, int]]:
    """Returns the global 'carrinho' list."""
    return carrinho

def fechar_pedido_core() -> tuple[float, str]:
    """
    Calculates the total value from the 'carrinho'.
    Clears the 'carrinho'.
    Returns the calculated total value and a confirmation message.
    """
    if not carrinho:
        return 0.0, "Carrinho está vazio. Nenhum pedido a fechar."

    valor_total: float = 0.0
    for item_dict in carrinho:
        for produto_obj, quantidade in item_dict.items():
            valor_total += produto_obj.preço * quantidade
    
    carrinho.clear()
    return valor_total, "Pedido fechado com sucesso. Carrinho esvaziado."
