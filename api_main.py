from fastapi import FastAPI, HTTPException
from typing import List, Dict, Any # Import Any for the checkout response model
import core_logic 
import schemas
from Models.produto import Produto # Needed for type checking if not already imported by core_logic

app = FastAPI(title="Mercado API")

# --- Product Endpoints ---

@app.post("/produtos", response_model=schemas.ProdutoResponse, status_code=201)
def criar_produto_api(produto_data: schemas.ProdutoCreate):
    """
    Cria um novo produto.
    """
    novo_produto = core_logic.cadastrar_produto_core(nome=produto_data.nome, preco=produto_data.preço)
    return novo_produto

@app.get("/produtos", response_model=List[schemas.ProdutoResponse])
def listar_produtos_api():
    """
    Lista todos os produtos cadastrados.
    """
    produtos = core_logic.listar_produtos_core()
    return produtos

@app.get("/produtos/{codigo}", response_model=schemas.ProdutoResponse)
def obter_produto_api(codigo: int):
    """
    Obtém um produto específico pelo seu código.
    """
    produto = core_logic.pegar_produto_por_codigo_core(codigo=codigo)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

# --- Cart Endpoints ---

@app.post("/carrinho/items/{codigo}", response_model=schemas.CartItemSchema) # Or a more specific response
def adicionar_item_carrinho_api(codigo: int):
    """
    Adiciona um produto ao carrinho pelo código do produto.
    Assume quantidade 1 por adição. Para mudar quantidade, pode-se chamar múltiplas vezes
    ou implementar um endpoint PUT/PATCH para atualizar quantidade.
    """
    status, item_atualizado_ou_novo = core_logic.comprar_produto_core(codigo=codigo)
    
    if status == "Produto não encontrado": # This check needs to be aligned with comprar_produto_core's actual message
        raise HTTPException(status_code=404, detail=status)
    
    # We need to find the product object to construct CartItemSchema
    produto_obj = core_logic.pegar_produto_por_codigo_core(codigo=codigo)
    if not produto_obj:
        # This should ideally not happen if comprar_produto_core worked, but as a safeguard:
        raise HTTPException(status_code=500, detail="Erro interno ao processar o carrinho")

    # Find the quantity of this specific product in the cart
    quantidade_no_carrinho = 0
    for item_dict in core_logic.carrinho: # Accessing global cart from core_logic
        if produto_obj in item_dict:
            quantidade_no_carrinho = item_dict[produto_obj]
            break
            
    if quantidade_no_carrinho == 0:
        # If not found after 'comprar_produto_core' which should have added it.
        raise HTTPException(status_code=500, detail="Erro ao atualizar a quantidade do item no carrinho.")

    return schemas.CartItemSchema(produto=schemas.ProdutoResponse.from_orm(produto_obj), quantidade=quantidade_no_carrinho)


@app.get("/carrinho", response_model=schemas.CarrinhoResponse)
def visualizar_carrinho_api():
    """
    Visualiza o conteúdo atual do carrinho.
    """
    carrinho_items_core = core_logic.visualizar_carrinho_core()
    
    # Transform the core_logic cart structure to schemas.CarrinhoResponse
    items_response = []
    valor_total_carrinho = 0.0
    for item_dict in carrinho_items_core:
        for produto_obj, quantidade in item_dict.items():
            items_response.append(
                schemas.CartItemSchema(
                    produto=schemas.ProdutoResponse.from_orm(produto_obj),
                    quantidade=quantidade
                )
            )
            valor_total_carrinho += produto_obj.preço * quantidade
            
    return schemas.CarrinhoResponse(items=items_response, valor_total=valor_total_carrinho)

@app.post("/carrinho/checkout", response_model=Dict[str, Any]) # Changed to Dict[str, Any]
def checkout_carrinho_api():
    """
    Finaliza a compra, calcula o valor total e limpa o carrinho.
    """
    if not core_logic.carrinho: # Check if cart is empty
        raise HTTPException(status_code=400, detail="Carrinho está vazio. Nada para finalizar.")

    valor_total, mensagem_core = core_logic.fechar_pedido_core() # mensagem_core from core_logic
    
    # Return both valor_total and a custom message as per test expectation
    return {"valor_total": valor_total, "mensagem": "Pedido finalizado com sucesso!"}


# --- Health Check Endpoint (Optional but good practice) ---
@app.get("/health")
def health_check():
    return {"status": "ok"}
