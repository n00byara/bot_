from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from database.models import BaseModel

class AnswerUserQuizModel(BaseModel):
    __tablename__ = "answer_user_quiz"

    answer_id = Column(Integer, ForeignKey("answers.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    quiz_id = Column(Integer, ForeignKey("polls.id"), primary_key=True)
    value = Column(Integer, nullable=False)

    answer = relationship("AnswerModel", backref="answer")
    user = relationship("UserModel", backref="user_id")
    quiz = relationship("QuizModel", backref="poll")