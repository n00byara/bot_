from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from configuration import config
from database.models import BaseModel
from database.models import UserModel
from database.models import RoleModel
from database.models import QuizModel
from database.models import QuizTypeModel
from database.models import AnswerModel
from database.models import AnswerUserQuizModel
from text import Message

config = config.postgres

class DataBase:
    def __init__(self):
        self.engine = create_engine(
            f"postgresql+psycopg2://{config.username}:{config.userpassword}@{config.host}:{config.port}/{config.database}"
        )

        self.conn = self.engine.connect()

        BaseModel.metadata.create_all(bind=self.engine)

        self.__init_constants()

    def __check_constants(self) -> bool:
        with Session(self.engine) as session:
            roles_len = len(session.query(RoleModel).all()) == 0
            answers_len = len(session.query(AnswerModel).all()) == 0
            quiz_types_len = len(session.query(QuizTypeModel).all()) == 0

            return roles_len == 0 and answers_len == 0 and quiz_types_len == 0

    # Добавление данных при инициализации базы
    def __init_constants(self):
        if not self.__check_constants():
            with Session(self.engine) as session:
                role_user = RoleModel(name="user")
                role_moderator = RoleModel(name="moderator")
                role_admin = RoleModel(name="admin")

                answer_1 = AnswerModel(text=Message.QUIZ_QUESTION_2.value)
                answer_2 = AnswerModel(text=Message.QUIZ_QUESTION_3.value)
                answer_3 = AnswerModel(text=Message.QUIZ_QUESTION_4.value)

                quiz_type_1 = QuizTypeModel(name=Message.GAME_BUTTON.value)
                quiz_type_2 = QuizTypeModel(name=Message.QUIZ_BUTTON.value)
                quiz_type_3 = QuizTypeModel(name=Message.OTHER_BUTTON.value)

                session.add_all(
                    [role_user, role_moderator, role_admin, answer_1, answer_2, answer_3, quiz_type_1, quiz_type_2, quiz_type_3]
                )
                session.commit()

    def __find_quiz_type(self, quiz_type_name) -> QuizTypeModel:
        with Session(self.engine) as session:
            quiz_type = session.query(QuizTypeModel).filter(QuizTypeModel.name == quiz_type_name).first()

        return quiz_type

    def find_user(self, username) -> UserModel:
        with Session(self.engine) as session:
            user = session.query(UserModel).filter(UserModel.username.like(username)).first()

        return user

    def get_user(self, username) -> UserModel:
        with Session(self.engine) as session:
            user = session.query(UserModel).filter(UserModel.username.like(username)).first()

            if not user:
                user = UserModel(username=username, role_id=1)
                session.add(user)
                session.commit()
                session.refresh(user)

        return user
        
    def get_role(self, username) -> RoleModel:
        with Session(self.engine) as session:
            return session.query(RoleModel).join(UserModel).filter(UserModel.username == username).first()
        
    def create_quiz(self, fields) -> QuizModel:
        quiz_type = self.__find_quiz_type(fields[0])
        user = self.get_user(fields[4])
        date = datetime.strptime(fields[3], "%d.%m.%Y").date()
        
        with Session(self.engine) as session:
            quiz = QuizModel(name=fields[1], date=date, client=fields[2], teacher_id=user.id, quiz_type_id=quiz_type.id)
            session.add(quiz)
            session.commit()
            session.refresh(quiz)

        return quiz
        
    def get_quiz(self):
        with Session(self.engine) as session:
            quiz = session.query(QuizModel).filter(QuizModel.date == datetime.now().date()).first()

        return quiz
    
    def check_user_from_quiz(self, username, quiz_id) -> bool:
        with Session(self.engine) as session:
            return True if session.query(AnswerUserQuizModel).filter(
                AnswerUserQuizModel.quiz_id == quiz_id
            ).join(UserModel).filter(UserModel.username == username).first() else False

    def add_quiz_answers(self, value, answer_id, user_id, quiz_id):
        with Session(self.engine) as session:
            answer_user_quiz = AnswerUserQuizModel(answer_id=answer_id, user_id=user_id, quiz_id=quiz_id, value=value)

            session.add(answer_user_quiz)
            session.commit()

    def get_quiz_result(self):
        with Session(self.engine) as session:
            return session.query(AnswerUserQuizModel.value, UserModel.username.label("student"), AnswerModel.text, UserModel.username.label("teacher"))\
                .join(AnswerModel)\
                .join(UserModel.id == AnswerUserQuizModel.user_id)\
                .join(QuizModel)\
                .join(UserModel.id == QuizModel.teacher_id).all()