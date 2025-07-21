from sqlalchemy import  Column, String, DateTime
from datetime import datetime
from sqlalchemy.orm import declarative_mixin
from core.dbutils import Base
import uuid

@declarative_mixin
class Timestamp:
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)


class Recipe(Timestamp, Base):
    __tablename__ ="recipes"

    recipe_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    ingredients = Column(String, nullable=False)
    instructions = Column(String, nullable=False)
    prep_time = Column(String, nullable=True)
    cook_time = Column(String, nullable=True)
    servings = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
