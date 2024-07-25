# Geowebapp-flask
Burundi Market Analytics is a project from the Geowebapp wourse at Geoversity (ITC). We'll change the architecture and do the backend with flask, a python framework.

# Basics commands
```
python -V
python -m venv venv
pip install -r requirements.txt
pip freeze > requirements.txt
```

# Run your wsgi server
```
run_flask.bat
sh run_flask.sh
```

waitress-serve --listen=127.0.0.1:8000 app:app
