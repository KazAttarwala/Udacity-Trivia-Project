import os
from flask import Flask, request, abort, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_cors import CORS
import random
import sys
import json
import re 
from re import search
import numbers

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__, static_folder='frontend/build', static_url_path='')
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources={r"/*" : {"origins": '*'}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
      response.headers.add('Access-Control-Allow-Headers', 'GET, POST, DELETE, OPTIONS')
      return response

  def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start =  (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

  @app.route('/')
  def index():
    return send_from_directory(app.static_folder, 'index.html')

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    
    categories = list(map(Category.format, Category.query.order_by(Category.id).all()))

    catDict = {}
    for item in categories:
      catDict[item['id']] = item['type']

    if (len(catDict) == 0):
      abort(404)
    
    return jsonify({
      "categories": catDict
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
  @app.route('/questions')
  def get_questions():
    selection = Question.query.order_by(Question.id).all()
    current_questions = paginate_questions(request, selection)

    categories = []
    for question in current_questions:
      categories.append(question['category'])
    
    #convert to set to remove duplicates and then reconvert to list for json serialization
    unique_categories = set(categories)
    unique_categories = list(unique_categories)

    catObjDict = {}
    for item in unique_categories:
      category = Category.query.get(item).format()
      catObjDict[category['id']] = category['type']

    total_questions = len(current_questions)
    if (total_questions == 0):
      abort(404)

    return jsonify({
      "questions": current_questions,
      "total_questions": total_questions,
      "categories": catObjDict,
      "current_category": None
    })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:

      question = Question.query.get(question_id)
      
      if (question is None):
        abort(404)
      
      question.delete()
      return jsonify({
        "success": True,
      })
    
    except:
      print(sys.exc_info())
      abort(422)



  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  @app.route('/questions', methods=['POST'])
  def create_question():
    try:
      body = request.get_json()
      question = body.get('question').strip()
      answer = body.get('answer').strip()
      difficulty = body.get('difficulty')
      category = body.get('category')
      
      questionObj = Question(question, answer, category, difficulty)
      questionObj.insert()
      return jsonify({
        "success": True
      })
    except:
      print(sys.exc_info())
      abort(400, "bad request, the body is either missing arguments or the arguments were not properly formed")

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/search', methods=['POST'])
  def get_questions_from_search():
    
    body = request.get_json()
    search_term = body.get('searchTerm').strip().lower()

    if (not(search_term)):
      abort(400, "no search term provided")

    searchFilterText = "%" + search_term + "%"

    data = []
    filtered_questions = Question.query.filter(func.lower(Question.question).like(searchFilterText)).all()
    
    for question in filtered_questions:
      data.append(question)

    current_questions = paginate_questions(request, data)
    return jsonify({
      "questions": current_questions,
      "total_questions": len(current_questions),
      "current_category": None
    })

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

  @app.route('/categories/<int:categoryId>/questions')
  def get_questions_by_category(categoryId):
    try:
      questions = Question.query.filter_by(category = categoryId).order_by(Question.id).all()
      
      if not questions:
        abort(404, "no questions found for category " + categoryId)
      else:
        current_questions = paginate_questions(request, questions)
        total_questions = len(current_questions)
        
        category = Category.query.get(categoryId).format()

        return jsonify({
          "questions": current_questions,
          "total_questions": total_questions,
          "current_category": category['type']
        })

    except:
      print(sys.exc_info())
      abort(404)


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
  def get_quiz_questions_for_category():
    
    try:

      data = request.get_json()
      previous_questions = data.get('previous_questions')
      category = data.get('quiz_category', None)

      question_ids = []

      if (category is None):
        question_ids = [Question.id for Question in Question.query.all()]
      else:
        all_questions_for_category = Question.query.filter_by(category = category['id']).all()
        
        if (len(all_questions_for_category) == 0):
          abort(404, "no questions found for quiz category " + category['type'])
        
        for question in all_questions_for_category:
          question_ids.append(question.id)

      filtered_question_ids = [x for x in question_ids if x not in previous_questions]
      
      random_question = None
      if (len(filtered_question_ids)):
        random_question = Question.query.get(random.choice(filtered_question_ids)).format()

      #if (random_question is None):
       # abort(404, "no more questions left for quiz category " + category['type'])

      return jsonify({
        "question": random_question
      })
    
    except:
      print(sys.exc_info())
      abort(404)

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": 404,
      "message": error.description
      }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "unprocessable"
      }), 422
  
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": error.description
      }), 400

  return app

app = create_app()

    
