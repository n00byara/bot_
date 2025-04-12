from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Text

from database.models import BaseModel

class AnswerModel(BaseModel):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)