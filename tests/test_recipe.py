import pytest
from fastapi import status

def test_create_recipe(client, sample_recipe):
    """Test creating a new recipe."""
    response = client.post("/api/v1/recipe", json=sample_recipe)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == sample_recipe["name"]
    assert "recipe_id" in data

def test_get_recipe(client, sample_recipe):
    """Test retrieving a recipe."""
    # First create a recipe
    create_response = client.post("/api/v1/recipe", json=sample_recipe)
    recipe_id = create_response.json()["recipe_id"]
    
    # Then get it
    response = client.get(f"/api/v1/recipe/{recipe_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == sample_recipe["name"]
    assert data["recipe_id"] == recipe_id

def test_get_nonexistent_recipe(client):
    """Test getting a recipe that doesn't exist."""
    response = client.get("/recipes/nonexistent-id")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_recipe(client, sample_recipe):
    """Test updating a recipe."""
    # First create a recipe
    create_response = client.post("/api/v1/recipe", json=sample_recipe)
    recipe_id = create_response.json()["recipe_id"]
    
    # Update it
    updated_data = {"name": "Updated Recipe Name"}
    response = client.put(f"/api/v1/recipe/{recipe_id}", json=updated_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Updated Recipe Name"
    assert data["ingredients"] == sample_recipe["ingredients"]  # Other fields unchanged

def test_delete_recipe(client, sample_recipe):
    """Test deleting a recipe."""
    # First create a recipe
    create_response = client.post("/api/v1/recipe", json=sample_recipe)
    recipe_id = create_response.json()["recipe_id"]
    
    # Delete it
    response = client.delete(f"/api/v1/recipe/{recipe_id}")
    assert response.status_code == status.HTTP_200_OK
    
    # Verify it's gone
    get_response = client.get(f"/api/v1/recipe/{recipe_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND

def test_search_recipes(client, sample_recipe):
    """Test searching recipes."""
    # Create a few recipes
    client.post("/api/v1/recipe", json=sample_recipe)
    client.post("/api/v1/recipe", json={
        **sample_recipe,
        "name": "Another Recipe",
        "ingredients": "special ingredient"
    })
    
    # Test search by name
    response = client.post("/api/v1/recipe/search", json={
        "search": "Test",
        "page": 1,
        "page_size": 10,
        "sort_by": "name",
        "sort_order": "asc"
    })
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total"] == 1
    assert len(data["recipes"]) == 1
    assert data["recipes"][0]["name"] == "Test Recipe"
    
    # Test search by ingredient
    response = client.post("/api/v1/recipe/search", json={
        "search": "special",
        "page": 1,
        "page_size": 10,
        "sort_by": "name",
        "sort_order": "asc"
    })
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total"] == 1
    assert len(data["recipes"]) == 1
    assert data["recipes"][0]["name"] == "Another Recipe"

def test_pagination_and_sorting(client, sample_recipe):
    """Test pagination and sorting functionality."""
    # Create multiple recipes
    recipes = [
        {**sample_recipe, "name": f"Recipe {i}"} 
        for i in range(1, 4)
    ]
    for recipe in recipes:
        client.post("/api/v1/recipe", json=recipe)
    
    # Test pagination
    response = client.post("/api/v1/recipe/search", json={
        "page": 1,
        "page_size": 2,
        "sort_by": "name",
        "sort_order": "asc"
    })
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total"] == 3
    assert len(data["recipes"]) == 2
    assert data["page"] == 1
    assert data["page_size"] == 2
    
    # Test sorting
    response = client.post("/api/v1/recipe/search", json={
        "page": 1,
        "page_size": 10,
        "sort_by": "name",
        "sort_order": "desc"
    })
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    names = [recipe["name"] for recipe in data["recipes"]]
    assert names == sorted(names, reverse=True) 