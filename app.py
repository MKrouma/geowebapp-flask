# geowebapp services app
from flask import Flask, render_template
from flask_bootstrap import Bootstrap5

# app initialization
app = Flask(__name__)
bootstrap = Bootstrap5(app)

@app.route('/')
def index() : 
    return render_template('index.html')

@app.route('/viewer')
def viewer() : 
    return render_template('viewer.html')


if __name__ == "__main__" : 
    app.run(debug=True)