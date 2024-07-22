# activate venv
.\venv\Scripts\activate

#this is our main entry
set FLASK_APP=app.py

#you can remove this in deployment server
#it's useful so we can see any change from our code directly when developing
set FLASK_DEBUG=1

#running the app
flask run