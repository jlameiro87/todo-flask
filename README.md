# Final CS50 Project

# ToDo App, tracking todo items per registered user
# Options:
## Register a new account
## Login in the system
## Logout from the system
## Manage ToDos
### List Your ToDos
### Add a new ToDo
### Update an existing ToDo
### Delete an existing ToDo
### User has a notification indicator of pending ToDos

# Structure
## templates folder: html files with users views
## application.py, main file
## models.py, includes application models
## requirements.txt, includes all required python dependencies
## todos.db, application database

## Make sure have all the dependencies installed
Run `pip3 install -r requirements.txt` in your terminal window to make sure that all of the necessary Python packages (Flask, Flask-SQLAlchemy and flask_cors, for instance) are installed.

## This is a simple TODO app
### Used flask with SQLite to create an API Rest in the backend
### And in the front using React JS.

## To run the project simple execute:
`cd server`
`flask run`

## Author:
### Jorge L. Lameiro

## Set configuration variables
`set FLASK_APP=application.py`
`set DATABASE_URL=sqlite:///todos.db`