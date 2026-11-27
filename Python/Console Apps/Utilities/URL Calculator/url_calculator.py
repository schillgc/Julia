import os

from flask import Flask
from flask import render_template

app = Flask(__name__)


#Default
@app.route('/')
@app.route('/<name>')
def index(name='URL Calculator'):
    return render_template("index.html", name = name)
    

# Adds
@app.route('/add/<int:num1>/<int:num2>')
@app.route('/add/<float:num1>/<float:num2>')
@app.route('/add/<float:num1>/<int:num2>')
@app.route('/add/<int:num1>/<float:num2>')
def add(num1, num2):
    context = { 'num1': num1, 'num2': num2 }
    return render_template("add.html", **context)


# Subtracts
@app.route('/subtract/<int:num1>/<int:num2>')
@app.route('/subtract/<float:num1>/<float:num2>')
@app.route('/subtract/<float:num1>/<int:num2>')
@app.route('/subtract/<int:num1>/<float:num2>')
def subtract(num1, num2):
    context = { 'num1': num1, 'num2': num2 }
    return render_template("subtract.html", **context)


# Multiplies
@app.route('/multiply/<int:num1>/<int:num2>')
@app.route('/multiply/<float:num1>/<float:num2>')
@app.route('/multiply/<float:num1>/<int:num2>')
@app.route('/multiply/<int:num1>/<float:num2>')
def multiply(num1, num2):
    context = { 'num1': num1, 'num2': num2 }
    return render_template("multiply.html", **context)


# Divides
@app.route('/divide/<int:num1>/<int:num2>')
@app.route('/divide/<float:num1>/<float:num2>')
@app.route('/divide/<float:num1>/<int:num2>')
@app.route('/divide/<int:num1>/<float:num2>')
def divide(num1, num2):
    context = { 'num1': num1, 'num2': num2 }
    return render_template("divide.html", **context)


def main():
    """Run the local development server with safe defaults."""
    host = os.environ.get("URL_CALCULATOR_HOST", "127.0.0.1").strip() or "127.0.0.1"
    port = int(os.environ.get("URL_CALCULATOR_PORT", "8000"))
    app.run(host=host, port=port, debug=False)


if __name__ == "__main__":
    main()
