from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mypass@127.0.0.1:3306/taskDB'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taskDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ToDo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route('/', methods=['GET', 'POST'])
def homePage():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = ToDo(title = title, description = desc)
        db.session.add(todo)
        db.session.commit()
    allTodo = ToDo.query.all()
    print(allTodo)
    return render_template('index.html', allTodo=allTodo)

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = ToDo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')

    todo = ToDo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = ToDo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route('/about')
def aboutPage():
    return None

@app.route('/contact')
def contactPage():
    return render_template('contact.html')

if __name__ == "__main__":
    app.run(debug=True, port=8000)