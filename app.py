from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///employees.db" #Tells flask to create a database employees.db
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False #Tells flask not to track modifications of objects and emit signals

app.secret_key = "Secret Key"

db = SQLAlchemy(app)

class Employee(db.Model): #Inherits the properties of db.model class
    id = db.Column(db.Integer, primary_key=True, nullable=False) #Auto-Incrementing primary key
    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), nullable = False, unique = True)

    def __repr__(self):
        return f"Employee Name: {self.name}, Email: {self.email}"

@app.route("/")
def home():
    all_data = Employee.query.all()
    return render_template("index.html", employees = all_data)


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        data = Employee(name = name, email = email)
        db.session.add(data)
        db.session.commit()

        flash("Employee Inserted Successfully", "success")

        return redirect(url_for('home'))

@app.route('/update/<id>', methods=['POST'])
def update(id):
    if request.method == 'POST':
        data = Employee.query.get(id)
        data.name = request.form['name']
        data.email = request.form['email']

        db.session.commit()

        flash("Employee Updated Successfully", "success")

        return redirect(url_for('home'))
    
@app.route('/delete/<id>', methods=['GET','POST'])
def delete(id):
    data = Employee.query.get(id)
    db.session.delete(data)
    db.session.commit()

    flash("Employee Deleted Successfully", "danger")

    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)


"""app.app_context() # Specifes that database employees is needed to created from the employees file of this app.py file
db.create_all() # Creates database employees in your directory or in instance folder.

Implementation in terminal: 
python -c "from app import app, db; app.app_context(); db.create_all"""