#!/usr/bin/env python
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default= datetime.utcnow)
    comment = db.Column(db.String(200), nullable = False)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content = task_content, comment = 'None')
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue with your task"
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks = tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "We have mutual problem with deleting the task"



@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "You have major problem with updating your task"
    else:
        return render_template('update.html', task = task)

@app.route('/comment/<int:id>', methods = ['GET', 'POST'])
def comment(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.comment = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "You have major problem with commenting your task"
    else:
        return render_template('comment.html', task = task)

if __name__ == "__main__":
    app.run(debug=True)
