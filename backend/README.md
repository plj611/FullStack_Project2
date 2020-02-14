i# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## API endpoints

#### Getting Started

- Base URL: The backend app is hosted at `http://127.0.0.1:5000/` which is set as a proxy for the frontend app.
- Authentication: This application does not require authentication or API keys.

#### Error Handling

Errors are returned as JSON object as in the following format:

```
{
  "error": 404,
  "message": "not found",
  "success": false
}

```

This app will return 5 error types when request failed:

- 400: bad request
- 404: not found
- 405 method not allow
- 422: unprocessable entity
- 500: internal server error

#### Endpoints

<u>GET /categories</u>

- Description:

  - Return a list of questions categories 

- Sample call: 

  - `curl -X GET http://127.0.0.1:5000/categories`

  ```
  {
    "categories": [
      "science",
      "art",
      "geography",
      "history",
      "entertainment",
      "sports"
    ],
    "success": true
  }
  ```

<u>GET /questions?page=<int: page id>&category=<int: category id>&searchterm=<str: search str></u>

- Description:

  - Return a list of questions based on either category or search term, the result also has the total questions, current category and categories.

  - The possible values of category are:

    | id   | type          |
    | ---- | ------------- |
    | 1    | science       |
    | 2    | art           |
    | 3    | geography     |
    | 4    | history       |
    | 5    | entertainment |
    | 6    | sports        |

  - The results are paginated in groups of 10 

- Sample call:

  - `curl -X GET "http://127.0.0.1:5000/questions?page=1&category=1"`

  ```
  {
    "categories": [
      "science",
      "art",
      "geography",
      "history",
      "entertainment",
      "sports"
    ],
    "current_category": 1,
    "questions": [
      {
        "answer": "The Liver",
        "category": 1,
        "difficulty": 4,
        "id": 20,
        "question": "What is the heaviest organ in the human body?"
      },
      {
        "answer": "Alexander Fleming",
        "category": 1,
        "difficulty": 3,
        "id": 21,
        "question": "Who discovered penicillin?"
      },
      {
        "answer": "Blood",
        "category": 1,
        "difficulty": 4,
        "id": 22,
        "question": "Hematology is a branch of medicine involving the study of wha                                                                    t?"
      }
    ],
    "searchTerm": "null",
    "success": true,
    "total_questions": 3
  }
  ```

  - `curl -X GET "http://127.0.0.1:5000/questions?searchTerm=What"`

  ```
  {
    "categories": [
      "science",
      "art",
      "geography",
      "history",
      "entertainment",
      "sports"
    ],
    "current_category": 0,
    "questions": [
      {
        "answer": "Muhammad Ali",
        "category": 4,
        "difficulty": 1,
        "id": 9,
        "question": "What boxer's original name is Cassius Clay?"
      },
      {
        "answer": "Apollo 13",
        "category": 5,
        "difficulty": 4,
        "id": 2,
        "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
      },
      {
        "answer": "Tom Cruise",
        "category": 5,
        "difficulty": 4,
        "id": 4,
        "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
      },
      {
        "answer": "Edward Scissorhands",
        "category": 5,
        "difficulty": 3,
        "id": 6,
        "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
      },
      {
        "answer": "Lake Victoria",
        "category": 3,
        "difficulty": 2,
        "id": 13,
        "question": "What is the largest lake in Africa?"
      },
      {
        "answer": "Mona Lisa",
        "category": 2,
        "difficulty": 3,
        "id": 17,
        "question": "La Giaconda is better known as what?"
      },
      {
        "answer": "The Liver",
        "category": 1,
        "difficulty": 4,
        "id": 20,
        "question": "What is the heaviest organ in the human body?"
      },
      {
        "answer": "Blood",
        "category": 1,
        "difficulty": 4,
        "id": 22,
        "question": "Hematology is a branch of medicine involving the study of what?"
      },
      {
        "answer": "10",
        "category": 2,
        "difficulty": 1,
        "id": 32,
        "question": "what is the size of a atom"
      }
    ],
    "searchTerm": "What",
    "success": true,
    "total_questions": 9
  }
  
  ```

<u>DELETE /questions/<int: question id></u>

- Description:

  - Delete a question with ID, return success in state or error otherwise.

- Sample call:

  - `curl -X DELETE "http://127.0.0.1:5000/questions/32"`

  ```
  {
    "success": true
  }
  ```

<u>POST /questions?searchTerm=null</u>

- Description:
  - Add a question to the trivia, the post request must contain the question, answer, difficulty and category. The category must be in one of the category id that describe above.
  
  - The operation will return success if the question is added or error otherwise.
  
  - The values pass in the post body are:
  
    | name       | type and value                                               |
    | ---------- | ------------------------------------------------------------ |
    | question   | str                                                          |
    | answer     | str                                                          |
    | difficulty | int (value 1 to 5)                                           |
    | category   | int (1: science, 2: art, 3: geography, 4: history, 5: entertainment, 6: sports) |
  
- Sample call:
  
  - `curl -X POST "http://127.0.0.1:5000/questions?searchTerm=null" -H "Content-Type: application/json" -d '{"question": "What is the time for earth to rotate 360 degree?", "answer": "23Hr 56mins", "difficulty": 2, "category": 1}'`
  
  ```
  {
    "success": true
  }
  ```

<u>POST /questions</u>

- Description:

  - Search the trivia by any phrase. The questions list will return to include only questions which has that string within their question. The post request must contain searchTerm to search the trivia database.

  - The operation will return the list of questions upon success or error otherwise.

  - The value pass in the post body is:

    | name       | value |
    | ---------- | ----- |
    | searchTerm | str   |

- Sample call:

  - `curl -X POST "http://127.0.0.1:5000/questions" -H "Content-Type: application/json" -d '{"searchTerm": "earth"}'`

  ```
  {
    "current_category": 0,
    "questions": [
      {
        "answer": "23Hr 56mins",
        "category": 1,
        "difficulty": 2,
        "id": 61,
        "question": "What is the time for earth to rotate 360 degree?"
      }
    ],
    "searchTerm": "earth",
    "success": true,
    "total_questions": 1
  }
  ```


<u>GET /categories/<int: category id>/questions</u>

- Description:

  - Get questions based on category. The category is listed above.
  - It returns the list of questions in that particular category or returns error otherwise.

- Sample call:

  - `curl -X GET "http://127.0.0.1:5000/categories/1/questions"`

  ```
  {
    "current_category": 1,
    "questions": [
      {
        "answer": "The Liver",
        "category": 1,
        "difficulty": 4,
        "id": 20,
        "question": "What is the heaviest organ in the human body?"
      },
      {
        "answer": "Alexander Fleming",
        "category": 1,
        "difficulty": 3,
        "id": 21,
        "question": "Who discovered penicillin?"
      },
      {
        "answer": "Blood",
        "category": 1,
        "difficulty": 4,
        "id": 22,
        "question": "Hematology is a branch of medicine involving the study of what?"
      }
    ],
    "success": true,
    "total_questions": 3
  }
  ```

<u>POST /quizzes</u>

- Description:

  - Return a random question to play in quiz with particular category. The post request must consist the list of ids of previous questions and quiz category in the post body. The random question return is not in the previous questions list. It will return error if otherwise.

  - The values pass in the post body are :

    | name               | type and value                                               |
    | ------------------ | ------------------------------------------------------------ |
    | previous_questions | List [value1, value2, ....]                                  |
    | quiz_category      | Dict {"type": "science\|art\|geography\|history\|entertainment\|sports", "id": 0\|1\|2\|3\|4\|5} where 0: science, 1: art..... |

- Sample call:

  -  `curl -X POST "http://127.0.0.1:5000/quizzes" -H "Content-Type: application/json" -d '{"previous_questions": [2], "quiz_category": {"type": "science", "id": 0}}'`

  ```
  {
    "previousQuestions": [
      2
    ],
    "question": {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    "success": true
  }
  ```



## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
