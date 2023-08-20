from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

app = Flask(__name__)

api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:root@localhost/TasksProject'
db = SQLAlchemy(app)


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    description = db.Column(db.Text)
    completed = db.Column(db.Boolean)
    sort_number = db.Column(db.Integer)
    due_date = db.Column(db.Date)
    user_id = db.Column(db.Integer)
    category_id = db.Column(db.Integer)


# get all tasks
class TasksController(Resource):
    # get all tasks by user_id
    def get(self):
        user_id = (request.get_json())['user_id']

        if user_id is None:
            return {"Message": "User id is required"}, 400
        else:
            tasks = Tasks.query \
                .filter_by(user_id=user_id) \
                .order_by(Tasks.due_date, Tasks.sort_number) \
                .all()
            task = [{'id': task.id,
                     'title': task.title,
                     'description': task.description,
                     'completed': task.completed,
                     'sort_number': task.sort_number,
                     'due_date': task.due_date,
                     'user_id': task.user_id,
                     'category_id': task.category_id
                     } for task in tasks
                    ]
            return jsonify(task)

    # add task
    def post(self):
        data = request.get_json()
        try:
            newTask = Tasks(
                title=data['title'],
                description=data['description'],
                completed=False,
                sort_number=0,
                due_date=data['due_date'],
                user_id=data['user_id'],
                category_id=data['category_id']
            )
            db.session.add(newTask)
            db.session.commit()
            return jsonify({"Message": "Task added successfully"})
        except:
            return {"Message": "Unable to add the task"}, 403


api.add_resource(TasksController, '/tasks')


class TaskController(Resource):
    # get task by id
    def get(self, task_id):
        try:
            task = Tasks.query.get(task_id)
            task = {'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'completed': task.completed,
                    'sort_number': task.sort_number,
                    'due_date': task.due_date,
                    'user_id': task.user_id,
                    'category_id': task.category_id
                    }
            return jsonify(task)
        except:
            return {"Message": "Task Not Found"}, 404

    # update task
    def put(self, task_id):
        try:
            task = Tasks.query.get(task_id)
            try:
                data = request.get_json()
                if data['title'] is not None:
                    task.title = data['title']
                if data['description'] is not None:
                    task.description = data['description']
                if data['due_date'] is not None:
                    task.due_date = data['due_date']
                if data['completed'] is not None:
                    task.completed = data['completed']
                db.session.commit()
                return {"Message": "Task Updated Successfully"}
            except:
                return {"Message": "Unable to update task"}, 400
        except:
            return {"Message": "Task Not Found"}, 404

    # delete task
    def delete(self, task_id):
        try:
            task = Tasks.query.get(task_id)
            db.session.delete(task)
            db.session.commit()
            return jsonify({'message': 'Task deleted successfully'})
        except:
            return {"Message": "Task Not Found"}, 404


api.add_resource(TaskController, '/task/<int:task_id>')


# get tasks by date
class TasksByDate(Resource):
    def get(self, date):
        tasks = Tasks.query.filter_by(due_date=date) \
            .order_by(Tasks.sort_number).all()
        task = [{'id': task.id,
                 'title': task.title,
                 'description': task.description,
                 'completed': task.completed,
                 'sort_number': task.sort_number,
                 'due_date': task.due_date,
                 'user_id': task.user_id,
                 'category_id': task.category_id
                 } for task in tasks
                ]
        return jsonify(task)


api.add_resource(TasksByDate, '/tasks/<string:date>')


# get tasks by category
class TasksByCategory(Resource):
    def get(self, category_id):
        tasks = Tasks.query.filter_by(category_id=category_id) \
            .order_by(Tasks.sort_number, Tasks.due_date).all()
        task = [{'id': task.id,
                 'title': task.title,
                 'description': task.description,
                 'completed': task.completed,
                 'sort_number': task.sort_number,
                 'due_date': task.due_date,
                 'user_id': task.user_id,
                 'category_id': task.category_id
                 } for task in tasks
                ]
        return jsonify(task)


api.add_resource(TasksByCategory, '/tasks/<int:category_id>')


# get completed tasks
class CompletedTasks(Resource):
    def get(self, user_id):
        completedTasks = db.session.query(func.count(Tasks.id)).filter_by(user_id=user_id,
                                                                          completed=True).scalar()
        tasks = db.session.query(func.count(Tasks.id)).filter_by(user_id=user_id).scalar()
        message = f"You completed {completedTasks}/{tasks}"
        return {"Message": message}


api.add_resource(CompletedTasks, '/tasks/count/<int:user_id>')


@app.route('/')
def hello_world():  # put application's code here
    return "Hello World"


if __name__ == '__main__':
    app.run(debug=True)
