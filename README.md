# Recipe API

A RESTful API service for managing cooking recipes, built with FastAPI and SQLAlchemy. This API allows users to create, read, update, and delete recipes, with support for advanced filtering, sorting, and search capabilities.

## Features

- CRUD operations for recipes
- Paginated recipe listing
- Search functionality
- Advanced filtering and sorting
- SQLite database storage
- RESTful API design
- Proper error handling and HTTP status codes

## Tech Stack

- Python 3.x
- FastAPI (Web Framework)
- SQLAlchemy (ORM)
- Pydantic (Data Validation)
- SQLite (Database)
- Uvicorn (ASGI Server)

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