from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import Text
from sqlalchemy.orm import relationship

from database.models import BaseModel

class UserModel(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(Text, unique=True, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"))

    role = relationship("RoleModel", backref="role")