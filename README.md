# Mercado FastAPI API

This project is a web API for a simple market (Mercado) application, built with FastAPI. It allows managing products and a shopping cart.

## Features

*   Create, list, and retrieve products.
*   Add products to a shopping cart.
*   View the shopping cart.
*   Checkout the shopping cart.

## Setup

1.  **Clone the repository (if you haven't already):**
    ```bash
    # git clone <repository_url>
    # cd <repository_directory>
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

To run the FastAPI application, use Uvicorn:

```bash
uvicorn api_main:app --reload
```

The `--reload` flag makes the server restart automatically after code changes. The application will typically be available at `http://127.0.0.1:8000`.

## API Documentation

FastAPI provides automatic interactive API documentation. Once the server is running, you can access:

*   **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
*   **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Available Endpoints

*   `POST /produtos`: Create a new product.
*   `GET /produtos`: List all products.
*   `GET /produtos/{codigo}`: Get a specific product by its code.
*   `POST /carrinho/items/{codigo}`: Add a product to the shopping cart.
*   `GET /carrinho`: View the current shopping cart.
*   `POST /carrinho/checkout`: Finalize the purchase and clear the cart.
*   `GET /health`: Health check for the API.

## Data Storage

**Important:** This application currently uses in-memory data storage. This means all data (products, cart contents) will be lost if the application server is restarted. This is suitable for development and testing but not for production use.

## Running Tests

To run the unit tests, ensure `pytest` is installed (it's included in `requirements.txt`) and then run:

```bash
pytest
```

This will discover and run the tests in the `test_api.py` file.
