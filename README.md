# Recipe API

A RESTful API service for managing cooking recipes, built with FastAPI and SQLAlchemy. This API allows users to create, read, update, and delete recipes, with support for advanced filtering, sorting, and search capabilities.

## Features

- Full CRUD operations for recipes (Create, Read, Update, Delete)
- Smart search functionality across recipe names, ingredients, and instructions
- Advanced sorting by name or creation date
- Timestamp tracking (created_at, updated_at)
- SQLite database storage
- RESTful API design
- Proper error handling and HTTP status codes
- OpenAPI documentation (Swagger UI)

## Recipe Data Structure

Each recipe includes:
- `recipe_id`: Unique identifier (UUID)
- `name`: Recipe name
- `ingredients`: List of ingredients
- `instructions`: Cooking instructions
- `prep_time`: Preparation time (optional)
- `cook_time`: Cooking time (optional)
- `servings`: Number of servings (optional)
- `image_url`: URL to recipe image (optional)
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

## Tech Stack

- Python 3.x
- FastAPI (Web Framework)
- SQLAlchemy (ORM)
- Pydantic (Data Validation)
- Uvicorn (ASGI Server)
- python-dotenv (Environment Configuration)

## Prerequisites

- Python 3.x
- pip (Python package manager)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd recipe-api
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows
   .\venv\Scripts\activate
   # On Unix or MacOS
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Start the server:
   ```bash
   python main.py
   ```

2. The API will be available at `http://localhost:8085`
3. Access the interactive API documentation at `http://localhost:8085/docs`

## Testing

The project uses pytest for testing. The test suite includes integration tests that cover all major API endpoints and functionality including:

- Recipe creation
- Recipe retrieval
- Recipe updates
- Recipe deletion
- Search functionality with pagination and sorting
- Error handling

### Running Tests

To run the tests:

```bash
pytest tests/
```

The test suite uses an in-memory SQLite database to ensure tests are isolated and don't affect your development or production database.

### Test Structure

- `tests/conftest.py`: Contains pytest fixtures including:
- `tests/test_recipe.py`: Contains all API endpoint tests

## Running with Docker

The application can be run using Docker Compose, which sets up both the API service and a PostgreSQL database.

1. Make sure you have Docker and Docker Compose installed on your system.

2. Build and start the containers:
   ```bash
   docker compose up --build
   ```

3. The services will be available at:
   - API: `http://localhost:8085`
   - API Documentation: `http://localhost:8085/docs`
   - PostgreSQL Database: `localhost:5432`

To stop the services:
```bash
docker compose down
```

To stop the services and remove persistent data:
```bash
docker compose down -v
```

## API Endpoints

- `POST /recipes` - Create a new recipe
- `GET /recipes/{recipe_id}` - Get a specific recipe
- `PUT /recipes/{recipe_id}` - Update a recipe
- `DELETE /recipes/{recipe_id}` - Delete a recipe
- `POST /recipes/search` - Search and list recipes with:
  - Pagination (`page`, `page_size`)
  - Text search across name, ingredients, and instructions
  - Sorting by name or creation date (asc/desc)
