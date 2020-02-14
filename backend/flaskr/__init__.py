import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)

  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  #cors = CORS(app)
  #cors = CORS(app, resources={r"/*": {"origins": "*"}})
  cors = CORS(app, resources=r"/*", origins="*")

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  # CORS Headers 
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,POST,DELETE,OPTIONS')
      return response


  def return_categories():
     # function to return the categories

     categories = Category.query.order_by(Category.id)

     return [c.type.lower() for c in categories]

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  #@cross_origin()
  def get_categories():
     
     return jsonify({ 'categories': return_categories(),
		'success': True 
		})

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  @app.route('/questions', methods=['GET'])
  #@cross_origin()
  def get_questions():
     # this function is used for paginate the get questions by category and get questions by search term

     page = request.args.get('page', 1, type=int)
     category = request.args.get('category', 0, type=int) 
     searchterm = request.args.get('searchTerm', 'null', type=str)

     if category == 0 and searchterm == 'null':
        # if no category and search term is set, assume it is to search questions by query

        category = 1

     if category != 0 and searchterm == 'null':
        # search the questions based on category
        
        questions = Question.query.filter(Question.category==f'{category}').all()
        if not questions:
           abort(404)
 
     if category == 0 and searchterm != 'null':
        # search the questions using the search term

        questions = Question.query.filter(Question.question.ilike(f'%{searchterm}%')).all()
        if not questions:
           abort(404)

     if category != 0 and searchterm != 'null':
        # can't search by category and search term

        abort(404)

     categories = return_categories()
     formatted_questions = []
     #print(len(questions))
     #print(questions[0].category)
     #print(type(questions[0].category))
     for q in questions:
        q.category = int(q.category)
        #q.category -= 1
        formatted_questions.append(q.format())

     return jsonify({
		#'questions': [{'id':1, 'question':'ABC', 'answer':'1', 'category': 0, 'difficulty': 0, 'questionAction': 0}, 
				#{'id':2, 'question': 'DEF', 'answer':'2'}], 
		'questions': formatted_questions[((page - 1) * QUESTIONS_PER_PAGE):page * QUESTIONS_PER_PAGE],
		'total_questions': len(formatted_questions),
		'categories': categories,
		'current_category': category,
		'searchTerm': searchterm,
		'success': True
		})

  
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  #@cross_origin()
  def delete_question(question_id):
     # endpoint for deleting a question
 
     try:
        question = Question.query.get(question_id)
        question.delete()
     except:
        abort(422)
     return jsonify({'success': True})
         

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions', methods=['POST'])
  #@cross_origin()
  def search_questions():
     # this is an endpoint to handle both adding a new question and searching for questions
     # for adding a new question, the searchterm is added to the URL with a value of null, 
     # indiciating that we use the endpoint for adding a question. If no searchterm is in the 
     # URL, then we know that we are searching for the questions by phrase.

     body = request.get_json()
     
     if body is None:
        abort(400)
     else:
        searchterm = request.args.get('searchTerm', '', type=str)
        if searchterm == 'null':
           # Add question

           question = body.get('question')
           answer = body.get('answer')
           difficulty = body.get('difficulty')
           category = body.get('category')
   
           if not question or not answer or not difficulty or not category:
           #if question == '' or answer == '':
              # Error, we must have question, answer, difficulty and category in the request body.

              abort(400)
           else:
              #print(f'Q:{question} A:{answer} D:{difficulty} C:{category}')
              q = Question(question, answer, int(category), difficulty)
              try:
                 q.insert()
              except:
                 abort(422)
              return jsonify({'success': True})
        else:
           searchterm = body.get('searchTerm')
           if searchterm:
              # we search the questions by pharse.

              questions = Question.query.filter(Question.question.ilike(f'%{searchterm}%')).all()
              #questions = Question.query.filter(Question.question.ilike('%Q%')).all()
              formatted_questions = []

              if questions:
                 for q in questions:
                    q.category = int(q.category)
                    #q.category -= 1
                    formatted_questions.append(q.format())

                 return jsonify({
			'questions': formatted_questions[:QUESTIONS_PER_PAGE],
			'total_questions': len(formatted_questions),
			'current_category': 0,
			'searchTerm': searchterm,
			'success': True
			})
              else:
                 abort(404)
           else:
              abort(400)

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  #@cross_origin()
  def get_category_questions(category_id):
     # this is an endpoint for getting the questions by category.

     #category_id += 1  
     #questions = Question.query.filter(Question.category==category_id).all()
     questions = Question.query.filter(Question.category==f'{category_id}').all()
     #formatted_questions = [question.format() for question in questions]
     if len(questions) == 0:
        abort(404)
     formatted_questions = []
     for q in questions:
        q.category = int(q.category)
        #q.category -= 1
        formatted_questions.append(q.format())

     return jsonify({
		'questions': formatted_questions[:QUESTIONS_PER_PAGE],
		#'questions': [{'id':1, 'question':'ABC111', 'answer':'1', 'category': 0, 'difficulty': 0, 'questionAction': 0}, 
	#			{'id':2, 'question': 'DEF111', 'answer':'2'}], 
		'total_questions': len(formatted_questions),
		'current_category': category_id,
		'success': True
		})

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  #@cross_origin()
  def get_quiz():
     # this is the endpoint for getting the quiz questions.

     body = request.get_json()

     if body is None:
        abort(400)
     else:
        previous_questions = body.get('previous_questions')
        quiz_category = body.get('quiz_category')
        categories = return_categories()

        #print(f'A: {previous_questions} B: {quiz_category} ')
        #print(quiz_category['type'])
        try:
           if quiz_category['type'] in categories:
              # get the quiz question by category

              #questions = Question.query.filter(Question.category == int(quiz_category['id']) + 1).all()
              questions = Question.query.filter(Question.category == str(int(quiz_category['id']) + 1)).all()
           elif quiz_category['type'] == 'click':
              # get the quiz question by ALL

              questions = Question.query.all()
           else:
              raise RunTimeError
              
        except:
           abort(400)

        #print(questions)

        if len(questions) != 0:
           random_question = random.choice(questions)
        else:
           abort(404)

        previous_questions = list(previous_questions)
        while questions and random_question.id in previous_questions:
           # this loop is used to select a random question from the list of questions while it is 
           # not in the previous question list.

           l = len(questions)
           for i in range(l):
              if questions[i].id == random_question.id:
                 questions.pop(i)
                 break
           random_question = random.choice(questions) if questions else ''

        formatted_random_question = random_question.format() if random_question else ''

        return jsonify({
			'question': formatted_random_question,
			'previousQuestions': previous_questions,
			'success': True
			})
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
  def method_not_allow(error):
     return jsonify({
		'success': False,
		'error': 400,
		'message': 'bad request'
		}), 400 

  @app.errorhandler(404)
  def method_not_allow(error):
     return jsonify({
		'success': False,
		'error': 404,
		'message': 'not found'
		}), 404 

  @app.errorhandler(405)
  def method_not_allow(error):
     return jsonify({
		'success': False,
		'error': 405,
		'message': 'method not allow'
		}), 405 
     
  @app.errorhandler(422)
  def method_not_allow(error):
     return jsonify({
		'success': False,
		'error': 422,
		'message': 'unprocessable entity'
		}), 422 

  @app.errorhandler(500)
  def method_not_allow(error):
     return jsonify({
		'success': False,
		'error': 500,
		'message': 'internal server error'
		}), 500 
  return app
