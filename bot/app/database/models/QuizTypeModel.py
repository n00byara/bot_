from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import CHAR

from database.models import BaseModel

class QuizTypeModel(BaseModel):
    __tablename__ = "quiz_types"

    id = Column(Integer, primary_key=True)
    name = Column(CHAR(10), nullable=False)