from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import aliased
from sqlalchemy.orm import Session
from sqlalchemy import select

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

                quiz_type_1 = QuizTypeModel(name=Message.GAME_BUTTON.value)
                quiz_type_2 = QuizTypeModel(name=Message.QUIZ_BUTTON.value)
                quiz_type_3 = QuizTypeModel(name=Message.OTHER_BUTTON.value)

                constants = [role_user, role_moderator, role_admin, quiz_type_1, quiz_type_2, quiz_type_3]

                answers = [
                    Message.QUIZ_QUESTION_1.value,
                    Message.QUIZ_QUESTION_2.value,
                    Message.QUIZ_QUESTION_3.value,
                    Message.QUIZ_QUESTION_4.value,
                    Message.QUIZ_QUESTION_5.value,
                    Message.QUIZ_QUESTION_6.value,
                    Message.QUIZ_QUESTION_7.value
                ]

                for answer in answers:
                    constants.append(AnswerModel(text=answer))

                session.add_all(constants)
                session.commit()

    def __find_quiz_type(self, quiz_type_name) -> QuizTypeModel:
        with Session(self.engine) as session:
            quiz_type = session.query(QuizTypeModel).filter(QuizTypeModel.name == quiz_type_name).first()

        return quiz_type

    def find_user(self, username) -> UserModel:
        with Session(self.engine) as session:
            user = session.query(UserModel).filter(UserModel.username.like(username)).first()

        return user

    def get_user(self, id, username = "", phone_number = "") -> UserModel:
        with Session(self.engine) as session:
            user = session.query(UserModel).filter_by(id=id).first()

            if not user:
                user = UserModel(id=id, username=username, phone_number=phone_number,  role_id=1)
                session.add(user)
                session.commit()
                session.refresh(user)

        return user

    def get_user_by_username(self, username) -> UserModel:
        with Session(self.engine) as session:
            user = session.query(UserModel).filter_by(username=username).first()

            return user
        
    def get_role(self, username) -> RoleModel:
        with Session(self.engine) as session:
            return session.query(RoleModel).join(UserModel).filter(UserModel.username == username).first()
        
    def create_quiz(self, fields) -> QuizModel:
        quiz_type = self.__find_quiz_type(fields[0])
        user = self.get_user_by_username(fields[4])
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
        Student = aliased(UserModel, name="students")
        Teacher = aliased(UserModel, name="teachers")

        aq_subq = select(AnswerUserQuizModel).subquery()

        with Session(self.engine) as session:
            query = (
                select(
                    Student.id.label("student_id"),
                    QuizModel.name.label("quiz_name"),
                    Student.username.label("student_username"),
                    Teacher.username.label("teacher_id"),
                    QuizTypeModel.name.label("quiz_type"),
                    aq_subq.c.value.label("answer"),
                    AnswerModel.id.label("answer_id"),
                    QuizModel.date.label("quiz_date")
                )
                .select_from(aq_subq)
                .join(AnswerModel, AnswerModel.id == aq_subq.c.answer_id)
                .join(Student, Student.id == aq_subq.c.user_id)
                .join(QuizModel, QuizModel.id == aq_subq.c.quiz_id)
                .join(Teacher, Teacher.id == QuizModel.teacher_id)
                .join(QuizTypeModel, QuizTypeModel.id == QuizModel.quiz_type_id)
            )

            return session.execute(query).mappings().all()
