from flask import request, current_app
from flask.views import MethodView
from ..mixin import CORSPreflightMixin
from ..models import Task, db
from ..schemas import TaskSchema
from . import api


class TaskAPI(MethodView, CORSPreflightMixin):

    def __init__(self):
        self.task_schema = TaskSchema()
        self.task_schemas = TaskSchema(many=True)

    def get(self, task_id=None):
        if task_id is None:
            page = request.args.get('page', type=int, default=1)
            item_per_page = request.args.get('item_per_page', type=int, default=10)
            paginator = Task.query.paginate(page, item_per_page, error_out=False)
            return dict(data=self.task_schemas.dump(paginator.items), has_more=paginator.has_next, code=200), 200
        else:
            task = Task.query.get_or_404(task_id)
            return dict(data=self.task_schema.dump(task), code=200), 200

    def post(self):
        try:
            data = self.task_schema.load(request.json)
        except ValidationError as err:
            abort(400, err.messages)
        else:
            task = Task(title=data['title'], description=data['description'], status=data['status'])
            db.session.add(task)
            db.session.commit()
            return dict(data=self.task_schema.dump(task), code=200), 200

    def delete(self, task_id):
        task = Task.query.get_or_404(task_id)
        db.session.remove(task)
        db.session.commit()

        return {}, 204

    def put(self, task_id):
        try:
            task = Task.query.get_or_404(task_id)
            data = self.task_schema.load(request.json, partial=True, unknown=True)
        except ValidationError as err:
            abort(400, err.messages)
        else:
            task.title = data.get('title', task.title)
            task.description = data.get('title', task.description)
            task.status = data.get('status', task.status)

            db.session.add(task)
            db.session.commit()

            return dict(data=self.task_schema.dump(task), code=200), 200


task_view = TaskAPI.as_view('task_api')
api.add_url_rule('/tasks/', view_func=task_view, methods=['GET', 'POST', 'OPTIONS'])
api.add_url_rule('/tasks/<string:task_id>', view_func=task_view, methods=['GET', 'PUT', 'DELETE', 'OPTIONS'])
