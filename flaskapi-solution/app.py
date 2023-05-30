# ! /usr/bin/env python
from main import app, api

from settings import settings
from flask import request, jsonify
import requests

from views.v1.admin import (check_role, create_role, get_roles, get_user_roles, delete_role,  # noqa: F401
                            change_role, grant_role, revoke_role)

from views.v1.auth import (login_user, logout_user, user_sessions, reg_user, update_user,  # noqa: F401
                           check_email, refresh_token)

from helios import initialize

initialize(
    api_token=settings.helios_api_token,
    service_name="FlaskAuth_API",
    enabled=settings.helios_enabled,
    environment="MyEnv",    # Defaults to os.environ.get('DEPLOYMENT_ENV') if omitted.
    commit_hash="",    # Defaults to os.environ.get('COMMIT_HASH') if omitted.
)


@app.before_request
def block_bots():
    if request.method == 'POST' and settings.recapcha_enabled:
        # Check if the request is coming from a bot
        response = requests.post('https://www.google.com/recaptcha/api/siteverify',
                                 data={'secret': settings.recapcha_api_key,
                                       'response': request.form.get('g-recaptcha-response')})
        if not response.json().get('success'):
            return jsonify({'error': 'Please complete the CAPTCHA.'}), 403


api.register(app)

if __name__ == "__main__":
    app.run(port=8001, debug=True)
