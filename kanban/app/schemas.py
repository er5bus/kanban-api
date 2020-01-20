from . import ma
from .models import Task
from marshmallow.validate import Length


class TaskSchema(ma.Schema):
    _id = ma.Int(dump_only=True)
    title = ma.String(max_length=150, required=True, validate=Length(max=150, min=1))
    description = ma.String(max_length=500, required=True, validate=Length(max=500, min=1))
    status = ma.String(max_length=200, required=True, validate=Length(max=200, min=1))

    class Meta:
        Model = Task
