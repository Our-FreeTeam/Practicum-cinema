import json
from datetime import datetime

import messages
from flask import jsonify, make_response, request
from flask_pydantic_spec import Request, Response
from keycloak_conn import keycloak_admin, keycloak_conn
from main import api, app
from models.models import (BoolResponse, ErrorStr, Login, OnlyLogin, RegInfo,
                           SessionList, TokensResp)
from redis_bucket_conn import rate_limiter
from settings import settings
from utils import check_session

import keycloak
from keycloak import KeycloakAuthenticationError, KeycloakPostError


@app.route('/v1/auth/login', methods=['POST'])
@rate_limiter(settings.rate_limit, settings.time_period)
@api.validate(
    body=Request(Login),
    resp=Response(HTTP_200=BoolResponse, HTTP_400=None, HTTP_401=None,
                  HTTP_429=ErrorStr), tags=['auth'])
def login_user():
    """
        Выполнить авторизацию по логину и паролю
    """
    body = request.json
    try:
        try:
            token = keycloak_conn.token(body['user'], body['password'])
            response = make_response(dict(BoolResponse(result=True)))
            response.headers.set('access_token', token['access_token'])
            response.headers.set('refresh_token', token['refresh_token'])

        except keycloak.KeycloakPostError as e:
            return e.error_message.decode("utf-8"), str(e.response_code)

        return response
    except KeycloakAuthenticationError:
        return messages.INCORRECT_CREDENTIALS


@app.route('/v1/auth/logout', methods=['POST'])
@rate_limiter(settings.rate_limit, settings.time_period)
@check_session
@api.validate(body=Request(OnlyLogin), resp=Response(HTTP_200=None, HTTP_400=None, HTTP_409=None,
                                                     HTTP_429=ErrorStr),
              tags=['auth'])
def logout_user(token_info=None):
    """
        Выйти из учетной записи
    """

    if keycloak_conn.logout(request.headers.get('refresh_token')) == {}:
        return messages.LOGOUT_SUCCES


@app.route('/v1/auth/user_sessions', methods=['POST'])
@rate_limiter(settings.rate_limit, settings.time_period)
@check_session
@api.validate(resp=Response(HTTP_200=SessionList, HTTP_400=None, HTTP_409=None,
                            HTTP_429=ErrorStr), tags=['auth'])
def user_sessions(token_info: dict):
    """
        Получить активные сессии пользователя
    """
    try:
        id_user = keycloak_admin.get_user_id(token_info.get('username'))
        sessions = keycloak_admin.get_sessions(id_user)

        response = [{'id': session['id'],
                     'ip_address': session['ipAddress'],
                     'time_start': datetime.utcfromtimestamp(session['start'] / 1000).isoformat()}
                    for session in sessions]

        return jsonify({'sessions': response})
    except keycloak.KeycloakPostError as e:
        return e.error_message.decode("utf-8"), str(e.response_code)


@app.route('/v1/auth/session_history', methods=['POST'])
@rate_limiter(settings.rate_limit, settings.time_period)
@check_session
@api.validate(resp=Response(HTTP_200=SessionList, HTTP_400=None, HTTP_409=None,
                            HTTP_429=ErrorStr), tags=['auth'])
def user_history(token_info: dict):
    """
        Получить историю сессий пользователя
    """
    try:
        id_user = keycloak_admin.get_user_id(token_info.get('username'))

        URL_ADMIN_EVENTS = "admin/realms/{realm-name}/events"
        params_path = {
            "realm-name": "cinema",
            "id": id_user
        }

        data_raw = keycloak_admin.connection.raw_get(
            URL_ADMIN_EVENTS.format(**params_path), data=None, query=None)

        response = []
        for session in data_raw.json():
            if session.get('userId') == id_user and session.get('sessionId') is not None:
                response.append(
                    {'id': session['sessionId'],
                     'ip_address': session['ipAddress'],
                     'time_start': datetime.utcfromtimestamp(session['time'] / 1000).isoformat()}
                )

        return jsonify({'sessions': response})
    except keycloak.KeycloakPostError as e:
        return e.error_message.decode("utf-8"), str(e.response_code)


@app.route('/v1/auth/user_create', methods=['POST'])
@rate_limiter(settings.rate_limit, settings.time_period)
@api.validate(body=Request(RegInfo), resp=Response(HTTP_201=None, HTTP_400=None, HTTP_409=None,
                                                   HTTP_429=ErrorStr), tags=['auth'])
def reg_user():
    """
        Регистрация пользователя
    """
    body = request.json
    if not keycloak_admin.get_user_id(username=body['user']):
        try:
            keycloak_admin.create_user({"email": body['email'],
                                        "username": body['user'],
                                        "enabled": True,
                                        "credentials": [
                                            {"value": body['password'], "type": "password", }]})
            return messages.USER_CREATED
        except keycloak.KeycloakPostError as e:
            return e.error_message.decode("utf-8"), str(e.response_code)

    return messages.USER_EXIST


@app.route('/v1/auth/user_update', methods=['POST'])
@rate_limiter(settings.rate_limit, settings.time_period)
@check_session
@api.validate(body=Request(RegInfo), resp=Response(HTTP_202=None, HTTP_400=None, HTTP_409=None,
                                                   HTTP_429=ErrorStr),
              tags=['auth'])
def update_user(token_info=None):
    """
        Обновление данных пользователя
    """
    body = request.json
    try:

        userinfo = keycloak_conn.userinfo(request.headers.get('access_token'))
        if userinfo['preferred_username'] != body['user']:
            return messages.INCORRECT_CREDENTIALS

        user_id = keycloak_admin.get_user_id(username=body['user'])
        keycloak_admin.update_user(
            user_id,
            {"email": body['email'],
             "enabled": True,
             "credentials": [
                 {"value": body['password'], "type": "password", }]})

    except (keycloak.KeycloakPostError, keycloak.KeycloakGetError) as e:
        return e.error_message.decode("utf-8"), str(e.response_code)

    return messages.USER_UPDATED


@app.route('/v1/auth/check_email', methods=['POST'])
@rate_limiter(settings.rate_limit, settings.time_period)
@check_session
@api.validate(resp=Response(HTTP_202=None, HTTP_400=None, HTTP_409=None,
                            HTTP_429=ErrorStr), tags=['auth'])
def check_email():
    """
        Проверка email
    """
    try:
        userinfo = keycloak_conn.userinfo(request.headers.get('access_token'))

        user_id = keycloak_admin.get_user_id(username=userinfo['preferred_username'])
        keycloak_admin.send_verify_email(user_id=user_id)

        return messages.MAIL_SEND

    except keycloak.KeycloakPutError as e:
        return e.error_message.decode("utf-8"), str(e.response_code)


@app.route('/v1/auth/refresh_token', methods=['POST'])
@rate_limiter(settings.rate_limit, settings.time_period)
@api.validate(resp=Response(HTTP_202=TokensResp, HTTP_409=None,
                            HTTP_429=ErrorStr), tags=['auth'])
def refresh_token():
    """
        Обновление refresh токена
    """
    try:
        new_token = keycloak_conn.refresh_token(request.headers.get('refresh_token'))
        response = make_response(jsonify({'result': True}))
        response.headers.set("access_token", new_token['access_token'])
        return response
    except KeycloakPostError as e:
        return json.loads(e.response_body)['error_description'], e.response_code
