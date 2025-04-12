from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import CHAR
from sqlalchemy.orm import relationship

from database.models import BaseModel

class RoleModel(BaseModel):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(CHAR(20), unique=True, nullable=False)