## Backend - Full Stack Trivia API 

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## ToDo Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 


## REVIEW_COMMENT
```

Endpoints
*GET* `/questions`
*GET* `/categories`
*POST* `/questions` 
*DELETE* `/questions/{id}`
*POST* `/questions/search`
*GET* `/categories/{id}/questions`
*POST* `/quizzes`

*GET* `/questions`
- Retrieves all trivia questions
- Request parameters/body: None
- Sample response body
```
{
  "questions": [
      {
          "id": 1,
          "question": "Who killed Abraham Lincoln?",
          "answer": "John Wilkes Booth",
          "difficulty": 1,
          "category": 4
      }
  ],
  "total_questions": 1,
  "categories": {
      1: "Science",
      2: "Art",
      3: "Geography",
      4: "History",
      5: "Entertainment",
      6: "Sports"
  },
  "current_category": None
}
```
*GET* `/categories`
- Retrieves all trivia categories
- Request parameters/body: None
- Sample response body
```
{
  "categories": {
      1: "Science",
      2: "Art",
      3: "Geography",
      4: "History",
      5: "Entertainment",
      6: "Sports"
  }
}
```
*POST* `/questions` 
- Create a trivia question in a specified category
- Sample request body
```
{
  "question": "Who founded Disney?",
  "answer": "Walt Disney",
  "difficulty": "1",
  "category": "5"
}
```
- Sample response body
```
{
    "success": True
}
```
*DELETE* `/questions/{id}`
- Delete a trivia question 
- Request parameters: question id (int)
- Sample response body
```
{
    "success": True
}
```
*POST* `/questions/search`
- Search for a question
- Sample request body
```
{
    "searchTerm": "name"
}
```
- Sample response body
```
{
    "questions": [
        {
            "id": 5,
            "question": "What's the name of the city of love?",
            "answer": "Paris",
            "difficulty": 1,
            "category": 3
        }
        
    ],
    "total_questions": 1,
    "current_category": None
}
```
*GET* `/categories/{id}/questions`
- Retrieve all trivia questions for a specified category
- Request parameters: category id (int)
- Sample response body 
```
{
    "questions": [
        {
            "id": 10,
            "question": "What sport is NFL?",
            "answer": "Football",
            "difficulty": 1,
            "category": 6
        }
        
    ],
    "total_questions": 1,
    "current_category": "Sports"
}
```
*POST* `/quizzes`
- Retrieve next quiz question
- Sample request body
```
{
    "previous_questions": [
        {
            "id": 10
        },
        {
            "id": 11
        },
        {
            "id": 12
        }
    ],
    "quiz_category": 6
}
```
- Sample response body
```
{
    "question": {
        "id": 17,
        "question": "What is the translation of Karate?",
        "answer": "Empty Hand",
        "difficulty": 1,
        "category": 6
    }
}
```
```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
