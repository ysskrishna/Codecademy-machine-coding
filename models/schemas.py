from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class RecipeBase(BaseModel):
    name: str
    ingredients: str
    instructions: str
    prep_time: Optional[str] = None
    cook_time: Optional[str] = None
    servings: Optional[str] = None
    image_url: Optional[str] = None

class RecipeCreate(RecipeBase):
    pass

class RecipeUpdate(BaseModel):
    name: Optional[str] = None
    ingredients: Optional[str] = None
    instructions: Optional[str] = None
    prep_time: Optional[str] = None
    cook_time: Optional[str] = None
    servings: Optional[str] = None
    image_url: Optional[str] = None

class Recipe(RecipeBase):
    recipe_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PaginatedRecipeResponse(BaseModel):
    total: int
    page: int
    page_size: int
    recipes: List[Recipe]


