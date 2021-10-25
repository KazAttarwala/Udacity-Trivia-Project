import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr.app import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.bad_question = {
            "question": "Who killed Roger Rabbit?",
            "answer": "Bunny",
            "category": 2,
            "difficulty": "pretty hard"
        }
        self.good_question = {
            "question": "Who killed Roger Rabbit?",
            "answer": "The Easter Bunny",
            "category": 2,
            "difficulty": 1
        }
        self.search_term = {
            "searchTerm": "what"
        }
        self.empty_search = {
            "searchTerm": ""
        }
        self.good_quiz_arguments = {
            "previous_questions": [
                {
                    "id": 5
                }
            ],
            "quiz_category": {
                "id": 4,
                "type": "History"
            }
        }
        self.bad_quiz_arguments = {
            "previous_questions": [
                {
                    "id": 5
                }
            ],
            "quiz_category": {
                "id": 2000,
                "type": None
            }
        }
    
    def tearDown(self):
        """Executed after each test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], None)

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['categories']))

    def test_delete_question(self):
        res = self.client().delete('/questions/2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_on_delete(self):
        res = self.client().delete('/questions/-1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    def test_400_for_create_without_body(self):
        res = self.client().post('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)

    def test_successful_create_question(self):
        res = self.client().post('/questions', json=self.good_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
    
    def test_400_on_create_with_invalid_body(self):
        res = self.client().post('/questions', json=self.bad_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
    
    def test_404_if_create_question_not_allowed(self):
        res = self.client().post('/questions/hello')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    def test_search_for_question(self):
        res = self.client().post('/questions/search', json=self.search_term)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], None)

    def test_400_if_search_is_empty(self):
        res = self.client().post('/questions/search', json=self.empty_search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)

    def test_404_if_search_not_allowed(self):
        res = self.client().post('/questions/search/hello')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    def test_get_paginated_questions_by_category(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    def test_404_if_no_questions_found_for_category(self):
        res = self.client().get('/categories/2000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    def test_404_if_category_filtering_not_allowed(self):
        res = self.client().get('/categories/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    def test_get_quiz_question_for_category(self):
        res = self.client().post('/quizzes', json=self.good_quiz_arguments)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        assert data['question'] is not None

    def test_404_if_no_questions_found(self):
        res = self.client().post('/quizzes', json=self.bad_quiz_arguments)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    def test_404_if_get_next_quiz_question_not_allowed(self):
        res = self.client().post('/quizzes/1', json=self.good_quiz_arguments)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()