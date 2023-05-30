import json
from functools import wraps

from flask import request
from keycloak import KeycloakPostError

import messages
from keycloak_conn import keycloak_conn


def check_session(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            token_info = keycloak_conn.introspect(request.headers.get('access_token'))
            is_active = token_info.get('active')
            if is_active:
                return func(*args, token_info=token_info, **kwargs)
            return messages.INCORRECT_TOKEN
        except KeycloakPostError as e:
            return json.loads(e.response_body)['error_description'], e.response_code

    return inner
