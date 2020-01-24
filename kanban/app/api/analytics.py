from flask import request, abort
from flask.views import MethodView
from marshmallow.exceptions import ValidationError
from ..schemas import AnalyticsSchema
from ..models import Analytics, db
from ..mixin import CORSPreflightMixin


class AnalyticsAPI(MethodView, CORSPreflightMixin):
    def __init__(self):
        self.analytic_schema = AnalyticsSchema()
        self.analytic_schemas = AnalyticsSchema(many=True)

    def get (self, analytics_id=None):
        if analytics_id is None:
            page = request.args.get('page', type=int, default=1)
            item_per_page = request.args.get('item_per_page', type=int, default=10)
            paginator = Analytics.query.paginate(page, item_per_page, error_out=False)
            return dict(data=self.analytic_schemas.dump(paginator.items), has_more=paginator.has_next, code=200), 200
        else:
            analytic = Analytics.query.get_or_404(analytics_id)
            return dict(data=self.analytic_schema.dump(analytic), code=200), 200

    def post (self):
        try:
            data = self.analytic_schema.load(request.json)
        except ValidationError as err:
            abort(400, err.messages)
        else:
            analytic = Analytics(event=data['event'], data=data['data'])

            db.session.add(analytic)
            db.session.commit()

            return dict(data=self.analytic_schema.dump(analytic), code=201), 201

    def put (self, analytics_id):
        analytic = Analytics.query.get_or_404(analytics_id)
        try:
            data = self.analytic_schema.load(request.json ,partial=True)
        except ValidationError as err:
            abort(400, err.messages)
        else:
            analytic.event = data.get('event', analytic.event)
            analytic = data.get('data', analytic.data)

            db.session.add(analytic)
            db.session.commit()

            return dict(data=self.analytic_schema.dump(analytic), code=200), 200

    def delete (self, analytics_id):
        analytic = Analytics.query.get_or_404(analytics_id)

        db.session.remove(analytic)
        db.session.commit()

        return dict(data=self.analytic_schema.dump(analytic), code=204), 204


analytic_view = AnalyticsAPI.as_view('analytic_api')
api.add_url_rule('/analytics/', view_func=analytic_view, methods=['GET', 'POST', 'OPTIONS'])
api.add_url_rule('/analytics/<string:analytics_id>', view_func=analytic_view, methods=['GET', 'PUT', 'DELETE', 'OPTIONS'])
