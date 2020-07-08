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
    CORS(app)
    cors = CORS(app, resources={r"/": {"origins": "*"}})

# CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, PATCH, POST, DELETE, OPTIONS')
        return response

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

    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        created_question = body.get('question')
        created_answer = body.get('answer')
        created_difficulty = body.get('difficulty')
        created_category = body.get('category')

        try:
            question = Question(question=created_question, answer=created_answer,
                                difficulty=created_difficulty, category=created_category)
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
        try:
            data = request.get_json()
            search_term = data.get('searchTerm')
            questions = Question.query.filter(
                Question.question.ilike('%{}%'.format(search_term))).all()
            paginated_questions = paginate_questions(request, questions)

            return jsonify({
                'success': True,
                'questions': paginated_questions,
                'total_questions':  len(questions)
            })
        except:
            abort(422)

    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        category = Category.query.filter(
            Category.id == category_id).one_or_none()

        if category is None:
            abort(404)

        questions = Question.query.filter(
            Question.category == category.id).all()
        paginated_questions = paginate_questions(request, questions)

        return jsonify({
            'success': True,
            'questions': paginated_questions,
            'current_category': category.type,
            'total_questions': len(questions)
        })

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        data = request.get_json()
        previous_questions = data.get('previous_questions', None)
        quiz_category = data.get('quiz_category', None)

        if ((quiz_category is None) or (previous_questions is None)):
            abort(400)

        if quiz_category['id'] == 0:
            questions = Question.query.all()
        else:
            questions = Question.query.filter_by(
                category=quiz_category['id']).all()

        if not questions:
            return abort(422)

        selected = []

        for question in questions:
            if question.id not in previous_questions:
                selected.append(question.format())

        if len(selected) != 0:
            result = random.choice(selected)
            return jsonify({
                'success': True,
                'question': result
            })
        else:
            return jsonify({
                'success': False,
                'question': False
            })

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    return app
