from . import ma
from .models import Task, Analytics
from marshmallow.validate import Length


class TaskSchema(ma.ModelSchema):
    _id = ma.Int(data_key="id", dump_only=True)
    title = ma.String(max_length=150, required=True, validate=Length(max=150, min=1))
    description = ma.String(max_length=500, required=True, validate=Length(max=500, min=1))
    status = ma.String(max_length=200, required=True, validate=Length(max=200, min=1))

    class Meta:
        Model = Task


class AnalyticsSchema(ma.ModelSchema):

    _id = ma.Int(data_key="id", dump_only=True)
    event = ma.String(max_length=1000, required=False, validate=Length(max=1000))
    data = ma.Dict(keys=ma.Str(), values=ma.Str())

    class Meta:
        Model = Analytics
