from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import Text
from sqlalchemy import Date
from sqlalchemy.orm import relationship

from database.models import BaseModel

class QuizModel(BaseModel):
    __tablename__ = "polls"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    date = Column(Date, nullable=False)
    client = Column(Text, nullable=False)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    quiz_type_id = Column(Integer, ForeignKey("quiz_types.id"), nullable=False)

    teacher = relationship("UserModel", backref="user")
    quiz_type = relationship("QuizTypeModel", backref="quiz_type")