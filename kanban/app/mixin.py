from flask import Response


class CORSPreflightMixin:

    status = 204
    allowed_headers = 'Content-Type, Authorization, X-Requested-With'
    allowed_methods = 'PUT, DELETE, POST, GET, OPTIONS'
    max_age = 120
    allowed_credentials = 'false'
    exposed_headers = '*'

    def options (self, **kwargs):
        headers = {
            'Access-Control-Allow-Headers' : self.allowed_headers,
            'Access-Control-Allow-Methods': self.allowed_methods,
            'Access-Control-Max-Age': self.max_age,
            'Access-Control-Allow-Credentials': self.allowed_credentials,
            'Access-Control-Expose-Headers': self.exposed_headers,
            'Vary': 'Origin'  # in case of server cache the response and the origin is not a wild card
        }
        return Response(status=self.status, headers=headers)
