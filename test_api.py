from fastapi.testclient import TestClient
from api_main import app # Your FastAPI application
import core_logic # To directly manipulate data for setup if needed
import schemas
from Models.produto import Produto # Import Produto from Models.produto

client = TestClient(app)

# --- Test Functions ---

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_criar_produto():
    # Clear products before test for reproducibility
    core_logic.produtos.clear() 
    # Reset product code counter for predictability
    if hasattr(Produto, '_proximo_codigo'): # Corrected to use Produto from Models.produto
         Produto._proximo_codigo = 1

    response = client.post("/produtos", json={"nome": "Test Product", "preço": 10.99})
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["nome"] == "Test Product"
    assert data["preço"] == 10.99
    assert "codigo" in data
    assert data["codigo"] == 1 # Assuming first product gets codigo 1

    response = client.post("/produtos", json={"nome": "Test Product 2", "preço": 1.00})
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["codigo"] == 2 # Assuming second product gets codigo 2

def test_listar_produtos():
    # For isolated tests, setup products here:
    core_logic.produtos.clear()
    if hasattr(Produto, '_proximo_codigo'): # Corrected
         Produto._proximo_codigo = 1
    client.post("/produtos", json={"nome": "List Prod 1", "preço": 1.0})
    client.post("/produtos", json={"nome": "List Prod 2", "preço": 2.0})

    response = client.get("/produtos")
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data) == 2
    assert data[0]["nome"] == "List Prod 1"
    assert data[1]["nome"] == "List Prod 2"

def test_obter_produto_especifico():
    core_logic.produtos.clear()
    if hasattr(Produto, '_proximo_codigo'): # Corrected
         Produto._proximo_codigo = 1
    prod_response = client.post("/produtos", json={"nome": "Specific Product", "preço": 99.99})
    assert prod_response.status_code == 201, prod_response.text # Ensure product created
    produto_codigo = prod_response.json()["codigo"]

    response = client.get(f"/produtos/{produto_codigo}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["nome"] == "Specific Product"
    assert data["codigo"] == produto_codigo

    response_not_found = client.get(f"/produtos/{produto_codigo + 99}") # Non-existent
    assert response_not_found.status_code == 404, response_not_found.text

def test_adicionar_item_carrinho():
    core_logic.produtos.clear()
    core_logic.carrinho.clear()
    if hasattr(Produto, '_proximo_codigo'): # Corrected
         Produto._proximo_codigo = 1
    prod_response = client.post("/produtos", json={"nome": "Cart Product", "preço": 5.0})
    assert prod_response.status_code == 201, prod_response.text # Ensure product created
    produto_codigo = prod_response.json()["codigo"]

    response = client.post(f"/carrinho/items/{produto_codigo}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["produto"]["codigo"] == produto_codigo
    assert data["quantidade"] == 1

    # Add same product again to check quantity update
    response_add_again = client.post(f"/carrinho/items/{produto_codigo}")
    assert response_add_again.status_code == 200, response_add_again.text
    data_again = response_add_again.json()
    assert data_again["produto"]["codigo"] == produto_codigo
    assert data_again["quantidade"] == 2
    
    response_not_found = client.post("/carrinho/items/9999") # Non-existent product
    assert response_not_found.status_code == 404, response_not_found.text

def test_visualizar_carrinho():
    core_logic.produtos.clear()
    core_logic.carrinho.clear()
    if hasattr(Produto, '_proximo_codigo'): # Corrected
         Produto._proximo_codigo = 1
    
    # Cart should be empty initially
    response_empty = client.get("/carrinho")
    assert response_empty.status_code == 200, response_empty.text
    data_empty = response_empty.json()
    assert data_empty["items"] == []
    assert data_empty["valor_total"] == 0.0

    # Add items to cart
    prod1_resp = client.post("/produtos", json={"nome": "Cart View Prod 1", "preço": 10.0})
    assert prod1_resp.status_code == 201
    prod1_cod = prod1_resp.json()["codigo"]
    client.post(f"/carrinho/items/{prod1_cod}")

    prod2_resp = client.post("/produtos", json={"nome": "Cart View Prod 2", "preço": 20.0})
    assert prod2_resp.status_code == 201
    prod2_cod = prod2_resp.json()["codigo"]
    client.post(f"/carrinho/items/{prod2_cod}")
    client.post(f"/carrinho/items/{prod2_cod}") # Add second product twice

    response_filled = client.get("/carrinho")
    assert response_filled.status_code == 200, response_filled.text
    data_filled = response_filled.json()
    assert len(data_filled["items"]) == 2
    assert data_filled["valor_total"] == (10.0 * 1) + (20.0 * 2) # 50.0
    
    # Check item details (order might vary, so check presence)
    found_prod1 = any(item["produto"]["codigo"] == prod1_cod and item["quantidade"] == 1 for item in data_filled["items"])
    found_prod2 = any(item["produto"]["codigo"] == prod2_cod and item["quantidade"] == 2 for item in data_filled["items"])
    assert found_prod1
    assert found_prod2

def test_checkout_carrinho():
    core_logic.produtos.clear()
    core_logic.carrinho.clear()
    if hasattr(Produto, '_proximo_codigo'): # Corrected
         Produto._proximo_codigo = 1

    # Test checkout with empty cart
    response_empty_checkout = client.post("/carrinho/checkout")
    assert response_empty_checkout.status_code == 400, response_empty_checkout.text # Bad Request

    # Add items and then checkout
    prod_resp = client.post("/produtos", json={"nome": "Checkout Product", "preço": 7.5})
    assert prod_resp.status_code == 201
    produto_codigo = prod_resp.json()["codigo"]
    client.post(f"/carrinho/items/{produto_codigo}")
    client.post(f"/carrinho/items/{produto_codigo}") # quantity becomes 2

    response_checkout = client.post("/carrinho/checkout")
    assert response_checkout.status_code == 200, response_checkout.text
    data = response_checkout.json()
    assert data["valor_total"] == 15.0 # 7.5 * 2
    assert data["mensagem"] == "Pedido finalizado com sucesso!" # This now matches api_main.py
    
    # Cart should be empty after checkout
    assert len(core_logic.carrinho) == 0
