

# Trivia API

This api allows you to create/delete quiz questions for a variety of categories, search for
questions, and play a trivia game. The backend is integrated with a React Web App that calls the api.


## Getting Started

[Fork](https://help.github.com/en/articles/fork-a-repo) the [project repository]() and [Clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine.

## Setting up the Backend
1. Install python3 to your machine and create a virtual environment for it 
2. Navigate to your `\backend` directory and run `pip install -r requirements.txt`. This will install all of the packages contained in the requirements file.
3. Run `createdb Trivia` in your command prompt or terminal.
4. From the `\backend` directory run `psql trivia < trivia.psql` to seed your database with the required data. 
5. From the same directory run `flask run --reload`, which will start the backend server and automatically reload it when changes are made inside the directory. You can now send requests to the api endpoints!

## API Endpoints
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

##Setting up the Frontend
1. Install Node and NPM
2. Navigate to the `\frontend` directory and run `npm install` in a command prompt/terminal. This will install all of the frontend dependencies 
in the package-lock.json file
3. Run `npm start` in the same directory to start the React Web App on `http://localhost:3000`
