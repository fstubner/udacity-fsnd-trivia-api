import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy

database_name = 'trivia_test'
database_host = 'localhost'
database_path = f"postgresql://{os.environ.get('DB_USER', 'postgres')}:{os.environ.get('DB_PASSWORD', 'postgres')}@{database_host}/{database_name}"

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    """Binds a Flask application and a SQLAlchemy service.

    Args:
        app (Flask): Instance of a Flask app.
        database_path (str, optional): Database URI. Defaults to database_path.
    """

    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Question(db.Model):
    __tablename__ = 'questions'

    # NOTE: Enhanced to make columns not nullable.
    id = Column(Integer, primary_key=True)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    category = Column(String, nullable=False)
    difficulty = Column(Integer, nullable=False)

    def __init__(self, question, answer, category, difficulty):
        self.question = question
        self.answer = answer
        self.category = category
        self.difficulty = difficulty

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_json(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category,
            'difficulty': self.difficulty
        }


class Category(db.Model):
    __tablename__ = 'categories'

    # NOTE: Enhanced to make columns not nullable.
    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)

    def __init__(self, type):
        self.type = type

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_json(self):
        return {
            'id': self.id,
            'type': self.type
        }
