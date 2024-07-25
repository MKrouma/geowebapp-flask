@echo off
call venv\Scripts\activate
set FLASK_APP=app.py
set FLASK_DEBUG=1
flask run --port 10000