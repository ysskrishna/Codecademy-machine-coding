from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from core.dbutils import get_db
from models.models import Recipe
from models.schemas import RecipeCreate, Recipe as RecipeSchema, RecipeUpdate, PaginatedRecipeResponse, ListRecipesRequest
from typing import Optional

router = APIRouter()

@router.post("", response_model=RecipeSchema)
def create_recipe(payload: RecipeCreate, db: Session = Depends(get_db)):
    new_recipe = Recipe(
        name=payload.name,
        ingredients=payload.ingredients,
        instructions=payload.instructions,
        prep_time=payload.prep_time,
        cook_time=payload.cook_time,
        servings=payload.servings,
        image_url=payload.image_url
    )
    
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)
    
    return new_recipe

@router.delete("/{recipe_id}")
def delete_recipe(recipe_id: str, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.recipe_id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    db.delete(recipe)
    db.commit()
    
    return {"message": "Recipe deleted successfully"}

@router.put("/{recipe_id}", response_model=RecipeSchema)
def update_recipe(recipe_id: str, payload: RecipeUpdate, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.recipe_id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(recipe, field, value)
    
    db.commit()
    db.refresh(recipe)
    
    return recipe

@router.get("/{recipe_id}", response_model=RecipeSchema)
def get_recipe(recipe_id: str, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.recipe_id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    return recipe

@router.post("/search", response_model=PaginatedRecipeResponse)
def list_recipes(
    payload: ListRecipesRequest,
    db: Session = Depends(get_db)
):
    query = db.query(Recipe)
    
    # Apply search filter if provided
    if payload.search:
        search_filter = or_(
            Recipe.name.ilike(f"%{payload.search}%"),
            Recipe.ingredients.ilike(f"%{payload.search}%"),
            Recipe.instructions.ilike(f"%{payload.search}%")
        )
        query = query.filter(search_filter)
    
    # Get total count before pagination
    total = query.count()
    
    # Apply sorting
    if payload.sort_by:
        if payload.sort_by not in ["name", "created_at"]:
            raise HTTPException(status_code=400, detail="Invalid sort_by field")
        
        sort_column = getattr(Recipe, payload.sort_by)
        if payload.sort_order == "desc":
            sort_column = sort_column.desc()
        query = query.order_by(sort_column)
    
    # Apply pagination
    if payload.page_size > 100:
        payload.page_size = 100
    
    recipes = query.offset((payload.page - 1) * payload.page_size).limit(payload.page_size).all()
    
    return PaginatedRecipeResponse(
        total=total,
        page=payload.page,
        page_size=payload.page_size,
        recipes=recipes
    )