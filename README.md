**THIS README WAS REWRITTEN AS PART OF THE TRIVIA APP PROJECT ASSIGNMENT**

# Full Stack Trivia API

**Table of Contents**
* [Backend](#Backend)
    * [Overview of Key Dependencies](#Overview%20of%20Key%20Dependencies)
    * [Installing Dependencies for the Backend](#Installing%20Dependencies%20for%20the%20Backend)
    * [Configuring Environment Variables](#Configuring%20Environment%20Variables)
    * [Database Setup](#Database%20Setup)
    * [Running the Backend Server](#Running%20the%20Backend%20Server)
    * [Testing](#Testing)
* [Frontend](#Frontend)
    * [Overview of Key Dependencies](#Overview%20of%20Key%20Dependencies)
    * [Installing Dependencies for the Frontend](#Installing%20Dependencies%20for%20the%20Frontend)
    * [Running the Frontend Server](#Running%20the%20Frontend%20Server)
* [API Reference](#API%20Reference)
    * [Getting Started](#Getting%20Started)
    * [Error Handling](#Error%20Handling)
    * [Endpoints](#Endpoints)


## Backend

### Overview of Key Dependencies
Here we have a quick overview of the key dependencies used in the creation of the `backend` of this project.
* [Python](https://www.python.org/) is a programming language that lets you work quickly and integrate systems more effectively.

* [Flask](https://flask.palletsprojects.com/en/2.0.x/) is a lightweight backend microservices framework for Python. Flask is required to handle requests and responses.

* [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we use to handle connections to our database.

* [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we use to handle cross-origin requests from our frontend server.

### Installing Dependencies for the Backend
Before we can run our backend server, we need to ensure our environment is set up correctly.
1. **Python 3.7**<br>
Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python).

2. **Virtual Environment**<br>
We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/). [Conda](https://docs.conda.io/en/latest/) is another great alternative for managing virtual environments.

3. **Project Dependencies**<br>
Once you have your virtual environment setup and running, install the required dependencies by naviging to the `backend` directory and running:
    ```bash
    pip install -r requirements.txt;
    ```
    This will install all of the required packages within the [requirements.txt](./backend/requirements.txt) file including our key dependencies.


### Configuring Environment Variables
Once dependencies have been installed, we need to configure environment variables for our database credentials and Flask app.

* **Database**<br>
    Firstly, lets configure the environment variables for our database credentials. In the commands below, replace `YOUR_DB_USERNAME` and `YOUR_DB_PASSWORD` with the credentials for your database and run them.
    ```bash
    export DB_USERNAME="YOUR_DB_USERNAME";
    export DB_PASSWORD="YOUR_DB_PASSWORD";
    ```
    >*note:* If these are not set, it will default to `postgres` for both username and password.

* **App**<br>
    Next, we also need to configure environment variables for our Flask application. This can be done using the commands below:

    ```bash
    export FLASK_APP=flaskr;
    export FLASK_ENV=development;
    ```
    Through the `FLASK_APP` variable we are instructing `Flask` to start the app called [flaskr](./backend/flaskr), which in our case is a module initialised by [\_\_init\_\_.py](./backend/flaskr/__init__.py).

    Additionally we are setting the `FLASK_ENV` variable to indicate that the app should be started in development mode. More info on this can be found under [Environment and Debug Features](https://flask.palletsprojects.com/en/2.0.x/config/#environment-and-debug-features) in the Flask documentation.

### Database Setup
With Postgres running, restore a database using the [trivia.psql](./backend/trivia.psql) file provided.

Navigate to the `backend` directory and run:
```bash
psql trivia < trivia.psql;
```

### Running the Backend Server
To run the server, navigate to the `backend` directory and run:
```bash
flask run;
```
The backend will be available under [http://localhost:5000](http://localhost:5000) by default.
>*note:* Ensure the virtual environment you created earlier is currently active.

### Testing
First, lets configure the environment variables for our test database credentials. In the commands below, replace `YOUR_TEST_DB_USERNAME` and `YOUR_TEST_DB_PASSWORD` with the credentials for your database and run them.
```bash
export TEST_DB_USERNAME="YOUR_TEST_DB_USERNAME";
export TEST_DB_PASSWORD="YOUR_TEST_DB_PASSWORD";
```
>*note:* If these are not set, it will default to `postgres` for both username and password.

Next, to run the API tests, navigate to the `backend` directory and run:
```bash
dropdb trivia_test;
createdb trivia_test;
psql trivia_test < trivia.psql;
python test_flaskr.py;
```

## Frontend

### Overview of Key Dependencies
Here we have a quick overview of the key dependencies used in the creation of the `frontend` of this project.
   * [React](https://reactjs.org/) is JavaScript library for building UIs.
### Installing Dependencies for the Frontend

1. **Node and NPM**<br>
    This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

2. **Project Dependencies**<br>
    This project uses NPM to manage software dependencies. NPM Relies on the [package.json](./frontend/package.json) file located in the `frontend` directory of this repository. To install dependencies, navigate to the `frontend` directory and run::
    ```bash
    npm install;
    ```
    >_tip_: `npm i` is shorthand for `npm install`


### Running the Frontend Server

The frontend app was built using `create-react-app`. In order to run the app in development mode, navigate to the `frontend` directory and run:

```bash
npm start;
```
The frontend will be available under [http://localhost:3000](http://localhost:3000) in your browser and a new browser tab should be opened automatically.

## API Reference
### Getting Started
* All responses and request bodies from and to this API are using `JSON`.
* The API does not have a public base URI as it runs locally. By default this will be [http://localhost:3000](http://localhost:3000).

### Error Handling
Errors are returned as JSON objects in the following format:
```json
{
    "success": false,
    "error": 404,
    "message": "not found"
}
```

The following error codes are returned by this API:
* **400**: Bad Request - If the request body could not be parsed.
* **404**: Not Found - If the requested resource could not be found.
* **422**: Unprocessable - If the request body could be parsed, but its contents are semantically incorrect.

### Endpoints
#### **Quiz**
><span style="color:gold">**POST**</span> /quizzes

Gets a question for a specific or any category. If `previous_questions` is provided, then the returned question will not be one from the provided list of `previous_questions`.

* Request Body
    * quiz_category (dict): Dict of a category object.
    * previous_questions (list): List of ids of questions to exclude from the response.

* Example Request
    ```bash
    curl --request POST 'http://localhost:3000/quizzes' \
         --header "Content-Type: application/json" \
         --data '{"quiz_category": {"type": "Science", "id": 1}, "previous_questions": [12, 32]}' \
    ```

* Example Response
    ```json
    {
        "success": true,
        "question": {
            "answer": "Alexander Fleming",
            "category": 1,
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?"
        }
    }
    ```

#### **Categories**

><span style="color:darkseagreen">**GET**</span> /categories

Gets a list of all categories.

* Example Request
    ```bash
    curl --request GET 'http://localhost:3000/categories'
    ```

* Example Response
    ```json
    {
        "success": true,
        "categories": {
            "1": "Science",
            "2": "Art",
            "3": "Geography",
            "4": "History",
            "5": "Entertainment",
            "6": "Sports"
        }
    }
    ```

<br>

><span style="color:darkseagreen">**GET**</span> /categories/<category_id>/questions?page=\<page\>

Gets a list of all questions for a specified category.

* Request Parameters
    * category_id (int): Id of a category for which to retrieve questions.
    * page (int): Page number.


* Example Request
    ```bash
    curl --request GET 'http://localhost:3000/categories/3/questions'
    ```

* Example Response
    ```json
    {
        "success": true,
        "current_category": 3,
        "questions": [
            {
                "answer": "Lake Victoria",
                "category": 3,
                "difficulty": 2,
                "id": 13,
                "question": "What is the largest lake in Africa?"
            },
            {
                "answer": "The Palace of Versailles",
                "category": 3,
                "difficulty": 3,
                "id": 14,
                "question": "In which royal palace would you find the Hall of Mirrors?"
            },
            {
                "answer": "Agra",
                "category": 3,
                "difficulty": 2,
                "id": 15,
                "question": "The Taj Mahal is located in which Indian city?"
            }
        ],
        "total_questions": 3
    }
    ```

<br>

#### **Questions**
><span style="color:gold">**POST**</span> /questions/search

Gets a paginated list of all questions which contain the provided search term. Limited to 10 per page.

* Request Body
    * searchTerm (str): The term to search questions by.

* Example Request
    ```bash
    curl --request POST 'http://localhost:3000/questions/search' \
         --header 'Content-Type: application/json' \
         --data '{"searchTerm": "ab"}'
    ```

* Example Response
    ```json
    {
        "success": true,
        "total_questions": 2,
        "questions": [
            {
                "answer": "Edward Scissorhands",
                "category": 5,
                "difficulty": 3,
                "id": 6,
                "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
            },
            {
                "answer": "Jackson Pollock",
                "category": 2,
                "difficulty": 2,
                "id": 19,
                "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
            }
        ],
        "current_category": null
    }
    ```

<br>

><span style="color:darkseagreen">**GET**</span> /questions?page=\<page\>

Gets a paginated list of all questions. Limited to 10 per page.

* Request Parameters
    * page (int): Page number.

* Example Request
    ```bash
    curl --request GET 'http://localhost:3000/questions'
    ```

* Example Response
    ```json
    {
        "success": true,
        "categories": {
            "1": "Science",
            "2": "Art",
            "3": "Geography",
            "4": "History",
            "5": "Entertainment",
            "6": "Sports"
        },
        "current_category": null,
        "total_questions": 43,
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
                "answer": "Brazil",
                "category": 6,
                "difficulty": 3,
                "id": 10,
                "question": "Which is the only team to play in every soccer World Cup tournament?"
            },
            {
                "answer": "Uruguay",
                "category": 6,
                "difficulty": 4,
                "id": 11,
                "question": "Which country won the first ever soccer World Cup in 1930?"
            },
            {
                "answer": "George Washington Carver",
                "category": 4,
                "difficulty": 2,
                "id": 12,
                "question": "Who invented Peanut Butter?"
            },
            {
                "answer": "The Palace of Versailles",
                "category": 3,
                "difficulty": 3,
                "id": 14,
                "question": "In which royal palace would you find the Hall of Mirrors?"
            },
            {
                "answer": "Agra",
                "category": 3,
                "difficulty": 2,
                "id": 15,
                "question": "The Taj Mahal is located in which Indian city?"
            },
            {
                "answer": "Escher",
                "category": 2,
                "difficulty": 1,
                "id": 16,
                "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
            }
        ]
    }
    ```

<br>

><span style="color:gold">**POST**</span> /questions

Creates a new question.

* Request Body
    * question(str): The question.
    * answer(str): The answer to the question.
    * difficulty(int): The difficulty of the question between 1-5.
    * category(int): The category the question belongs to.

* Example Request
    ```bash
    curl --request POST 'http://localhost:3000/questions' \
         --header 'Content-Type: application/json' \
         --data '{"question": "Where is Batman based?", "answer": "Gotham City", "difficulty": 3, "category": 3}'
    ```

* Example Response
    ```json
    {
        "success": true,
        "created": 84
    }
    ```

<br>

><span style="color:lightcoral">**DELETE**</span> /questions/<question_id>

Delete the question with the specified id.

* Request Parameters
    * question_id (int): Id of the question to delete.

* Example Request
    ```bash
    curl --request DELETE 'http://localhost:3000/questions/13'
    ```

* Example Response
    ```json
    {
        "deleted": 13,
        "success": true
    }
    ```