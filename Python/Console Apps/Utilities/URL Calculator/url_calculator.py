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


<<<<<<< HEAD
app.run(debug = True, port = 8000, host = '0.0.0.0')
=======
app.run(debug = False, port = 8000, host = '0.0.0.0')
>>>>>>> 94ae7c67ab8fb01bd690eed6e256c116e1516b50
