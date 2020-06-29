import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  formatted_questions = [question.format() for question in selection]
  # questions for given page
  current_questions = formatted_questions[start:end]

  return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

#   '''
#   @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
#   '''
    # set up CORS
    CORS(app)
    cors = CORS(app, resources={r"/": {"origins": "*"}})


#   '''
#   @TODO: Use the after_request decorator to set Access-Control-Allow
#   '''
# CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, PATCH, POST, DELETE, OPTIONS')
        return response

#   '''
#   @TODO:
#   Create an endpoint to handle GET requests
#   for all available categories.
#   '''
    @app.route('/categories')
    # handle GET request for all available categories
    def get_categories():
        categories_list = Category.query.all()
        categories_dict = {}
        for category in categories_list:
            categories_dict[category.id] = category.type

        return jsonify({
            'success': True,
            'categories': categories_dict
        })


#     '''
#   @TODO:
#   Create an endpoint to handle GET requests for questions,
#   including pagination (every 10 questions).
#   This endpoint should return a list of questions,
#   number of total questions, current category, categories.

#   TODO: TEST: At this point, when you start the application
#   you should see questions and categories generated,
#   ten questions per page and pagination at the bottom of the screen for three pages.
#   Clicking on the page numbers should update the questions.
#   '''
    @app.route('/questions')
    # handle GET request for questions
    def get_questions():
        questions_list = Question.query.all()

        # gets questions for given page
        current_questions = paginate_questions(request, questions_list)

        # if no questions for given page - abort
        if len(current_questions) == 0:
            abort(404)

        categories_list = Category.query.all()
        categories_dict = {}
        for category in categories_list:
            categories_dict[category.id] = category.type

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(questions_list),
            'categories': categories_dict
        })

#     '''
#   @TODO:
#   Create an endpoint to DELETE question using a question ID.

#   TODO: TEST: When you click the trash icon next to a question, the question will be removed.
#   This removal will persist in the database and when you refresh the page.
#   '''

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    # handle DELETE method for given question id
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()
            if question is None:
                abort(404)

            question.delete()
            return jsonify({
                'success': True,
                'deleted': question_id
            })
        except:
            abort(422)


#     '''
#   @TODO:
#   Create an endpoint to POST a new question,
#   which will require the question and answer text,
#   category, and difficulty score.

#   TODO: TEST: When you submit a question on the "Add" tab,
#   the form will clear and the question will appear at the end of the last page
#   of the questions list in the "List" tab.
#   '''

    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        created_question = body.get('question')
        created_answer = body.get('answer')
        created_difficulty = body.get('difficulty')
        created_category = body.get('category')

        try:
            question = Question(question=created_question, answer=created_answer, difficulty=created_difficulty, category=created_category)
            question.insert()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)
            return jsonify({
                'success': True,
                'created': question.id,
                'questions': current_questions,
                'total_questions': len(selection)
            })
        except:
            abort(422)

    @app.route('/questions/search', methods=['POST'])
    def search_question():
        print("dupa")
        search_term = request.json.get('searchTerm')
        results = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
        # results=Question.query.filter(Question.question.ilike('%{}%'.format(data['searchTerm']))).all()

        return jsonify({
            'success': True,
            'questions': results
        })

    return app


# INSERT INTO questions (question, answer, difficulty, category) VALUES ('is this cat?', 'yes', '2', '1');

    
#     '''
#   @TODO:
#   Create a POST endpoint to get questions based on a search term.
#   It should return any questions for whom the search term
#   is a substring of the question.

#   TEST: Search by any phrase. The questions list will update to include
#   only question that include that string within their question.
#   Try using the word "title" to start.
#   '''

#     '''
#   @TODO:
#   Create a GET endpoint to get questions based on category.

#   TEST: In the "List" tab / main screen, clicking on one of the
#   categories in the left column will cause only questions of that
#   category to be shown.
#   '''

#     '''
#   @TODO:
#   Create a POST endpoint to get questions to play the quiz.
#   This endpoint should take category and previous question parameters
#   and return a random questions within the given category,
#   if provided, and that is not one of the previous questions.

#   TEST: In the "Play" tab, after a user selects "All" or a category,
#   one question at a time is displayed, the user is allowed to answer
#   and shown whether they were correct or not.
#   '''

#     '''
#   @TODO:
#   Create error handlers for all expected errors
#   including 404 and 422.
#   '''
