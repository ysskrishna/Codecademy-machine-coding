from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from core.dbutils import get_db
from models.models import Recipe
from models.schemas import RecipeCreate, Recipe as RecipeSchema, RecipeUpdate, PaginatedRecipeResponse
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

@router.get("", response_model=PaginatedRecipeResponse)
def list_recipes(
    db: Session = Depends(get_db),
    page: int = Query(1, gt=0),
    page_size: int = Query(10, gt=0, le=100),
    search: Optional[str] = None,
    sort_by: Optional[str] = Query(None, enum=["name", "created_at", "prep_time"]),
    sort_order: Optional[str] = Query("asc", enum=["asc", "desc"])
):
    query = db.query(Recipe)
    
    # Apply search filter if provided
    if search:
        search_filter = or_(
            Recipe.name.ilike(f"%{search}%"),
            Recipe.ingredients.ilike(f"%{search}%"),
            Recipe.instructions.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    # Get total count before pagination
    total = query.count()
    
    # Apply sorting
    if sort_by:
        sort_column = getattr(Recipe, sort_by)
        if sort_order == "desc":
            sort_column = sort_column.desc()
        query = query.order_by(sort_column)
    
    # Apply pagination
    recipes = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return PaginatedRecipeResponse(
        total=total,
        page=page,
        page_size=page_size,
        recipes=recipes
    )