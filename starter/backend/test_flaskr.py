import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
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


        self.sample_question = {
            'question': 'Who invented Peanut Butter?',
            'answer': 'George Washington Carver',
            'category': 4,
            'difficulty': 2
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    # 1. test for ('/categories') -> return jsonify({
        #     'success': True,
        #     'categories': categories_dict
        # })
    # 2. test for ('/questions) -> return jsonify({
        #     'success': True,
        #     'questions': current_questions,
        #     'total_questions': len(questions_list),
        #     'categories': categories_dict
        # })

    # 3. test for ('/questions/<int:question_id>' DELETE) -> return jsonify({
            #     'success': True,
            #     'deleted': question_id
            # })

    # 4. ('/questions', methods=['POST']) -> return jsonify({
            #     'success': True,
            #     'created': question.id,
            #     'questions': current_questions,
            #     'total_questions': len(selection)
            # })
    # 5. ('/questions/search', methods=['POST']) ->  return jsonify({
            #     'success': True,
            #     'questions': paginated_questions,
            #     'total_questions':  len(questions)
            # })

    # 6. ('/categories/<int:category_id>/questions') -> return jsonify({
        #     'success': True,
        #     'questions': paginated_questions,
        #     'current_category': category.type,
        #     'total_questions': len(questions)
        # })

    # 7. '/quizzes', methods=['POST']) -> return jsonify({
            #     'question': result
            # })

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()