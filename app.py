from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# For mySql database
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost/flask"
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost/flask"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable = False)
    description = db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    status = db.Column(db.String(500), nullable = False)

    def __repr__(self)-> str:
        return f"{self.sno} - {self.title}"
@app.route('/', methods=['GET', 'POST'])
def hello_world():
    todo = Todo()
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        todo = Todo(title=title, description=description, status="Pending")
        db.session.add(todo)
        db.session.commit()
    alltodo = todo.query.all()
    return render_template('index.html', alltodo = alltodo)

@app.route('/about')
def about():
    return 'This is about page.'

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect ('/')

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.description = description
        db.session.add(todo)
        db.session.commit()
        return redirect ('/')
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo = todo)

@app.route('/complete/<int:sno>', methods=['GET', 'POST'])
def completed(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    todo.status = 'Completed'
    db.session.add(todo)
    db.session.commit()
    return redirect ('/')
@app.route('/uncomplete/<int:sno>', methods=['GET', 'POST'])
def incomplete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    todo.status = 'Pending'
    db.session.add(todo)
    db.session.commit()
    return redirect ('/')


@app.route('/updatedata/<int:sno>', methods=['GET', 'POST'])
def updatedata(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    title = todo.title
    desc = todo.description
    data = {'title': title,
            'desc': desc}
    print(data)

    return data

if __name__ == "__main__":
    app.run(debug=True)