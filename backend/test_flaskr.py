import os
import json
import unittest
from random import randint
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'trivia_test'
        self.database_host = 'localhost'
        self.database_path = f"postgresql://{os.environ.get('TEST_DB_USER', 'postgres')}:{os.environ.get('TEST_DB_PASSWORD', 'postgres')}@{self.database_host}/{self.database_name}"
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        # Populate the DB
        categories = [
            {
                "id": 1,
                "type": "Science"
            },
            {
                "id": 2,
                "type": "Art"
            },
            {
                "id": 3,
                "type": "Geography"
            },
            {
                "id": 4,
                "type": "History"
            },
            {
                "id": 5,
                "type": "Entertainment"
            },
            {
                "id": 6,
                "type": "Sports"
            }
        ]

        questions = [
            {
                "answer": "Muhammad Ali",
                "category": 4,
                "difficulty": 1,
                "question": "What boxer's original name is Cassius Clay?"
            },
            {
                "answer": "Apollo 13",
                "category": 5,
                "difficulty": 4,
                "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
            },
            {
                "answer": "Tom Cruise",
                "category": 5,
                "difficulty": 4,
                "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
            },
            {
                "answer": "Edward Scissorhands",
                "category": 5,
                "difficulty": 3,
                "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
            },
            {
                "answer": "Brazil",
                "category": 6,
                "difficulty": 3,
                "question": "Which is the only team to play in every soccer World Cup tournament?"
            },
            {
                "answer": "Uruguay",
                "category": 6,
                "difficulty": 4,
                "question": "Which country won the first ever soccer World Cup in 1930?"
            },
            {
                "answer": "George Washington Carver",
                "category": 4,
                "difficulty": 2,
                "question": "Who invented Peanut Butter?"
            },
            {
                "answer": "The Palace of Versailles",
                "category": 3,
                "difficulty": 3,
                "question": "In which royal palace would you find the Hall of Mirrors?"
            },
            {
                "answer": "Agra",
                "category": 3,
                "difficulty": 2,
                "question": "The Taj Mahal is located in which Indian city?"
            },
            {
                "answer": "Escher",
                "category": 2,
                "difficulty": 1,
                "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
            },
            {
                "answer": "Nobody knows?",
                "category": 3,
                "difficulty": 2,
                "question": "Who and the what now?"
            },
            {
                "answer": "I'm going to cross you.",
                "category": 1,
                "difficulty": 5,
                "question": "What did the chicken say to the road?"
            }
        ]

        for category in categories:
            new_category = Category(
                type=category['type']
            )
            new_category.insert()

        first_id = Category.query.order_by(Category.id.asc()).first()
        last_id = Category.query.order_by(Category.id.desc()).first()

        for question in questions:
            new_question = Question(
                question=question['question'],
                answer=question['answer'],
                difficulty=question['difficulty'],
                category=randint(first_id.id, last_id.id)
            )
            new_question.insert()

    def tearDown(self):
        """Executed after each test"""

        # Ensuring the DB is clean
        questions = Question.query.all()
        categories = Category.query.all()
        for question in questions:
            question.delete()

        for category in categories:
            category.delete()

    '''
    @ [DONE] TODO:
    Write at least one test for each test for successful operation and for expected errors.
    '''

    def test_get_paginated_questions(self):
        res = self.client().get('/questions?page=2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))

    def test_404_get_paginated_questions_with_invalid_page_number(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not found')

    def test_delete_question(self):
        # Insert a new question for deletion.
        first_id = Category.query.order_by(Category.id.asc()).first()
        last_id = Category.query.order_by(Category.id.desc()).first()
        question = Question(
            question='Will this question be deleted?',
            answer='Yes it will',
            difficulty=1,
            category=randint(first_id.id, last_id.id)
        )
        question.insert()
        question_id = question.id

        # Run the deletion test
        res = self.client().delete(f'/questions/{question_id}')
        data = json.loads(res.data)

        question = Question.query.filter(
            Question.id == question.id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], question_id)
        self.assertEqual(question, None)

    def test_404_delete_question_with_invalid_id(self):
        res = self.client().delete('/questions/123155')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not found')

    def test_create_question(self):
        # Setup of new question
        first_id = Category.query.order_by(Category.id.asc()).first()
        last_id = Category.query.order_by(Category.id.desc()).first()
        request_body = {
            'question': 'Was Batman cool?',
            'answer': 'No, he was a bat.',
            'difficulty': 3,
            'category': randint(first_id.id, last_id.id)
        }

        # Run the test
        res = self.client().post('/questions', json=request_body)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])

    def test_422_create_question_with_missing_field(self):
        first_id = Category.query.order_by(Category.id.asc()).first()
        last_id = Category.query.order_by(Category.id.desc()).first()
        request_body = {
            'question': 'My super quizzy new question?',
            'answer': 'Definitely the correct answer.',
            'category': randint(first_id.id, last_id.id)
        }

        res = self.client().post('/questions', json=request_body)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_search_questions(self):
        request_body = {'searchTerm': 'a'}
        res = self.client().post('/questions/search', json=request_body)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['questions'])
        self.assertIsNotNone(data['total_questions'])

    def test_404_search_questions_with_no_results(self):
        request_body = {
            'searchTerm': 'random_test_phrase_that_doesnt_exist',
        }
        res = self.client().post('/questions/search', json=request_body)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "not found")

    def test_422_search_questions_with_missing_searchterm(self):
        request_body = {
            'searchTerm': '',
        }
        res = self.client().post('/questions/search', json=request_body)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_play_quiz(self):
        request_body = {'previous_questions': [],
                          'quiz_category': {'type': 'Entertainment', 'id': 5}}

        res = self.client().post('/quizzes', json=request_body)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_play_quiz_with_missing_quiz_category(self):
        request_body = {'previous_questions': []}
        res = self.client().post('/quizzes', json=request_body)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_get_questions_by_category(self):
        first_id = Category.query.order_by(Category.id.asc()).first()
        last_id = Category.query.order_by(Category.id.desc()).first()
        res = self.client().get(
            f'/categories/{randint(first_id.id, last_id.id)}/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    def test_404_get_questions_by_category(self):
        last_id = Category.query.order_by(Category.id.desc()).first()
        res = self.client().get(f'/categories/{last_id+1}/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "not found")

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_404_get_categories_when_none_exist(self):
        # Ensure no categories exist.
        questions = Question.query.all()
        for question in questions:
            question.delete()

        categories = Category.query.all()
        for category in categories:
            category.delete()

        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
