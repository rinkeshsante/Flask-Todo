from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200),nullable=False)
    completed = db.Column(db.Integer,default = 0)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

db.create_all()
db.session.commit()

@app.route('/',methods =["POST","GET"])
def index():
    if request.method == "POST":
        task_content  = request.form["content"]
        # print(task_content)
        if task_content == "":
            return redirect('/')

        new_task = Todo(content = task_content)
        
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return "Error occured" + str(e)
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html',tasks = tasks)

@app.route('/delete/<int:id>')
def deleteTask(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return str(e)


@app.route('/update/<int:id>',methods=['GET', 'POST'])
def updateTask(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form["content"]
        
        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return str(e)
    else:
        return render_template('update.html' , task = task)

if __name__ == "__main__":
    app.run(debug=True)