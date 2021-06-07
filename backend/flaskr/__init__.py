import sys
import random
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from models import setup_db, Question, Category


RESULTS_PER_PAGE = 10


def paginate(request, selection):
    """Utility function to provide paginated results.

    Args:
        request (flask.request): Flask request received by the route.
        selection (list): Results of query.

    Returns:
        list: Paginated results of query.
    """

    page = request.args.get('page', 1, type=int)
    start = (page - 1) * RESULTS_PER_PAGE
    end = start + RESULTS_PER_PAGE

    results = [result.to_json() for result in selection]
    current_selection = results[start:end]

    return current_selection


def create_app(test_config=None):
    """Creates a Flask app and its routes.

    Args:
        test_config (str, optional): Path to configuration file. Defaults to None.

    Returns:
        Flask: Instance of a Flask app.
    """

    app = Flask(__name__)
    setup_db(app)

    '''
    @ [DONE] TODO:
        Set up CORS. Allow '*' for origins. Delete the sample route after
        completing the TODOs.
    '''
    CORS(app, resources={'/': {'origins': '*'}})

    '''
    @ [DONE] TODO:
        Use the after_request decorator to set Access-Control-Allow.
    '''
    @app.after_request
    def after_request(response):
        """Runs after every request.

        Args:
            response (Flask.response_class): Route response.

        Returns:
            Flask.response_class: Route response.
        """

        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers',
                             'GET, POST, PATCH, DELETE, OPTION')

        return response

    '''
    @ [DONE] TODO:
        Create an endpoint to handle GET requests for all available
        categories.
    '''
    @app.route('/categories')
    def get_categories():
        """Gets all Categories.

        Returns:
            json: {
                'success': bool,
                'categories': dict
            }

        Errors:
            404: Returned if no categories are found.
        """

        categories = {
            category.id: category.type for category in Category.query.all()}

        if len(categories) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': categories
        })

    '''
    @ [DONE] TODO:
        Create an endpoint to handle GET requests for questions,
        including pagination (every 10 questions).
        This endpoint should return a list of questions,
        number of total questions, current category, categories.

        TEST: At this point, when you start the application
        you should see questions and categories generated,
        ten questions per page and pagination at the bottom of the screen for three pages.
        Clicking on the page numbers should update the questions.
    '''
    @app.route('/questions')
    def get_questions():
        """Gets paginated questions.

        Returns:
            json: {
                'success': bool,
                'categories': dict,
                'current_category': None,
                'questions': list,
                'total_questions': int
            }

        Errors:
            404: Returned if no questions are found.
        """

        questions = Question.query.all()
        paginated_questions = paginate(request, questions)

        if len(paginated_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': {category.id: category.type for category in Category.query.all()},
            'current_category': None,
            'questions': paginated_questions,
            'total_questions': len(questions)
        })

    '''
    @ [DONE] TODO:
        Create an endpoint to DELETE question using a question ID.

        TEST: When you click the trash icon next to a question, the question will be removed.
        This removal will persist in the database and when you refresh the page.
    '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        """Deletes a question by id.

        Args:
            id (int): Id of the question to delete.

        Returns:
            json: {
                'success': bool,
                'deleted': int
            }

        Errors:
            404: Returned if question with specified id is not found.
            422: Returned if the request was unprocessable.
        """

        question = Question.query.filter(
            Question.id == question_id).one_or_none()

        if question is None:
            abort(404)

        try:
            question.delete()

            return jsonify({
                'success': True,
                'deleted': question_id
            })

        except:
            print(sys.exc_info())
            abort(422)

    '''
    @ [DONE] TODO:
        Create an endpoint to POST a new question,
        which will require the question and answer text,
        category, and difficulty score.

        TEST: When you submit a question on the "Add" tab,
        the form will clear and the question will appear at the end of the last page
        of the questions list in the "List" tab.
    '''
    @app.route('/questions', methods=['POST'])
    def create_question():
        """Creates a new question.

        Args:
            question (str): Question.
            answer (str): Answer to the question.
            difficulty (int): Value of difficulty.
            category (int): Id of category.

        Returns:
            json: {
                'success': bool,
                'created': int
            }

        Errors:
            422: Returned if the request was unprocessable.
        """

        body = request.get_json()

        question = Question(
            question=body.get('question') if body.get(
                'question') != '' else None,
            answer=body.get('answer') if body.get('answer') != '' else None,
            difficulty=body.get('difficulty', None),
            category=body.get('category', None)
        )

        # Not checking for empty values explicitly. Instead updated model to not allow
        # nullable and catch that way instead. This also results in us catching a more
        # relevant error instead of just 422.

        try:
            question.insert()

            return jsonify({
                'success': True,
                'created': question.id
            })

        except:
            print(sys.exc_info())
            abort(422)

    '''
    @ [DONE] TODO:
        Create a POST endpoint to get questions based on a search term.
        It should return any questions for whom the search term
        is a substring of the question.

        TEST: Search by any phrase. The questions list will update to include
        only question that include that string within their question.
        Try using the word "title" to start.
    '''
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        """Searches all questions using the search term provided.

        Args:
            searchTerm (str): Term to filter results by.

        Returns:
            json: {
                'success': bool,
                'questions': list,
                'total_questions': int,
                'current_category': None
            }

        Errors:
            404: Returned if no questions were found with the search
            term provided.
            422: If no search term is provided.
        """

        body = request.get_json()

        if not body.get("searchTerm"):
            abort(422)

        questions = Question.query.filter(
            Question.question.ilike('%{}%'.format(body.get("searchTerm")))).all()
        paginated_questions = paginate(request, questions)

        if len(paginated_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'current_category': None,
            'questions': paginated_questions,
            'total_questions': len(questions)
        })

    '''
    @ [DONE] TODO:
        Create a GET endpoint to get questions based on category.

        TEST: In the "List" tab / main screen, clicking on one of the
        categories in the left column will cause only questions of that
        category to be shown.
    '''
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        """Gets all questions for a specified category.

        Args:
            id (int): Id of the category to get questions for.

        Returns:
            json: {
                'success': bool,
                'questions': list,
                'total_questions': int,
                'current_category': None
            }

        Errors:
            404: Returned if no questions were found for the
            category.
        """

        questions = Question.query.filter(
            Question.category == category_id).all()
        paginated_questions = paginate(request, questions)

        if len(paginated_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'current_category': category_id,
            'questions': paginated_questions,
            'total_questions': len(questions)
        })

    '''
    @ [DONE] TODO:
        Create a POST endpoint to get questions to play the quiz.
        This endpoint should take category and previous question parameters
        and return a random questions within the given category,
        if provided, and that is not one of the previous questions.

        TEST: In the "Play" tab, after a user selects "All" or a category,
        one question at a time is displayed, the user is allowed to answer
        and shown whether they were correct or not.
    '''
    @app.route('/quizzes', methods=['POST'])
    def get_next_unanswered_question():
        """Get next available unanswered question for a specific category
        or all categories.

        Args:
            quiz_category (dict): Dict of current category.
            previous_questions (list): List of ids for previous questions.

        Returns:
            json: {
                'success': bool,
                'question': str or None
            }

        Errors:
            422: Returned if category or previous_questions were not provided
            in the request body.
        """

        body = request.get_json()

        category = body.get('quiz_category', None)
        previous_questions = body.get('previous_questions', None)

        if category is None:
            abort(422)

        # NOTE: Thought about using the existing API functions such as get_questions
        # and get_questions_by_category, but these are returned paginated, so these
        # functions would need to be enhanced to support providing full results
        # without pagination. Stuck to just creating a new query.
        category_id = category['id']
        if category_id:
            questions = [question.to_json() for question in Question.query.filter(
                Question.category == category_id).all()]
        else:
            questions = [question.to_json()
                         for question in Question.query.all()]

        unanswered_questions = [
            question for question in questions if question['id'] not in previous_questions]

        if len(unanswered_questions):
            return jsonify({
                'success': True,
                'question': random.choice(unanswered_questions)
            })
        else:
            return jsonify({
                'success': True,
                'question': None
            })

    '''
    @ [DONE] TODO:
        Create error handlers for all expected errors
        including 404 and 422.
    '''
    @app.errorhandler(400)
    def bad_request(error):
        """The server could not understand the request due to invalid syntax.

        Args:
            error (BadRequest): http exeption.

        Returns:
            json: {
                'success': bool,
                'error': int,
                'message': str
            }
            int: http status code.
        """

        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        """The requested resource could not be found.

        Args:
            error (NotFound): http exeption.

        Returns:
            json: {
                'success': bool,
                'error': int,
                'message': str
            }
            int: http status code.
        """

        return jsonify({
            'success': False,
            'error': 404,
            'message': 'not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        """The request was well-formed but was unable to be followed
        due to semantic errors.

        Args:
            error (UnprocessableEntity): http exeption.

        Returns:
            json: {
                'success': bool,
                'error': int,
                'message': str
            }
            int: http status code.
        """

        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        """The server has encountered a situation it doesn't know how to handle.

        Args:
            error (InternalServerError): http exeption.

        Returns:
            json: {
                'success': bool,
                'error': int,
                'message': str
            }
            int: http status code.
        """

        return jsonify({
            'success': False,
            'error': 500,
            'message': 'internal server error'
        }), 500

    return app
