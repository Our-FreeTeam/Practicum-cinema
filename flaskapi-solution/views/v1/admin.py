import json
from functools import wraps

import messages
from flask import jsonify, request
from flask_pydantic_spec import Request, Response
from keycloak_conn import keycloak_admin
from main import api, app
from models.models import (BoolResponse, ErrorStr, Role, RoleCheck, RoleIds,
                           RoleList, UserRole, StrResponse, UserIdRole, UserId)
from redis_bucket_conn import rate_limiter
from settings import settings
from utils import check_session

from keycloak import KeycloakDeleteError, KeycloakPostError, KeycloakPutError


def prep_user_data(body):
    client_id = keycloak_admin.get_client_id(settings.client_id)
    user_id = keycloak_admin.get_user_id(body.get('user_name'))
    role_id = keycloak_admin.get_client_role(client_id=client_id, role_name=body['role_name'])

    return client_id, user_id, role_id


@check_session
def check_role_in(body: RoleCheck, token_info: dict):
    user_roles = token_info['resource_access'].get('theatre')
    if user_roles:
        user_roles = user_roles.get('roles')
    else:
        user_roles = set()
    if not set(user_roles) & set(body.roles):
        return messages.INSUFFICIENT_PRIVILEGES
    return BoolResponse(result=True)


def check_role_wrap(roles: list[str]):
    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            res_check = check_role_in(body=RoleCheck(roles=roles))
            # Check if the result is a BoolResponse instance and convert it to a JSON response
            if isinstance(res_check, BoolResponse):
                return func(*args, **kwargs)
            return res_check

        return inner

    return func_wrapper


@app.route('/v1/admin/check_role', methods=['POST'])
@rate_limiter(settings.rate_limit, settings.time_period)
@api.validate(
    body=Request(RoleCheck),
    resp=Response(HTTP_200=BoolResponse, HTTP_403=None, HTTP_429=ErrorStr), tags=['admin'])
def check_role():
    """ Проверка наличия роли у пользователя """
    body = request.json
    bool_response = check_role_in(RoleCheck(**body))
    if isinstance(bool_response, BoolResponse):
        return jsonify(bool_response.dict())
    else:
        return bool_response


@app.route('/v1/admin/user/<user_id>/check_authorization', methods=['GET'])
@check_session
@rate_limiter(settings.rate_limit, settings.time_period)
@api.validate(resp=Response(HTTP_200=BoolResponse, HTTP_403=None, HTTP_429=ErrorStr), tags=['admin'])
def check_authorization(user_id: str, token_info: dict):
    """ Проверка корректности токена пользователя (если роли не нужны) """

    if user_id == token_info['sub']:
        return jsonify({'result': True})
    user_roles = token_info['resource_access'].get('theatre')
    if user_roles:
        user_roles = user_roles.get('roles')
        if set(user_roles) & set(['theatre_admin']):
            return jsonify({'result': True})
    return messages.INSUFFICIENT_PRIVILEGES


@app.route('/v1/admin/get_user_id_by_token', methods=['GET'])
@check_session
@rate_limiter(settings.rate_limit, settings.time_period)
@api.validate(resp=Response(HTTP_200=UserId, HTTP_403=None, HTTP_429=ErrorStr), tags=['admin'])
def get_user_id_by_token(token_info: dict):
    """ Получение user_id по токену """

    return jsonify({'user_id': token_info['sub']})


@app.route('/v1/admin/roles/create', methods=['POST'])
@rate_limiter(settings.rate_limit, settings.time_period)
@api.validate(body=Request(Role),
              resp=Response(HTTP_200=BoolResponse, HTTP_400=None, HTTP_409=None,
                            HTTP_429=ErrorStr), tags=['admin'])
@check_role_wrap(['theatre_admin'])
def create_role():
    """ Создание роли """
    try:
        body = request.json

        client_id = keycloak_admin.get_client_id(settings.client_id)
        keycloak_admin.create_client_role(client_role_id=client_id,
                                          payload={'name': body['role_name'],
                                                   'clientRole': True})
        return jsonify({'result': True})
    except KeycloakPostError as e:
        return json.loads(e.response_body)['errorMessage'], e.response_code


@app.route('/v1/admin/roles', methods=['GET'])
@rate_limiter(settings.rate_limit, settings.time_period)
@api.validate(resp=Response(HTTP_200=RoleList), tags=['admin'])
@check_role_wrap(['theatre_admin'])
def get_roles():
    """ Получить все роли """
    client_id = keycloak_admin.get_client_id(settings.client_id)
    roles = keycloak_admin.get_client_roles(client_id)
    response = [{'id': role['id'], 'role_name': role['name']} for role in roles]

    return jsonify({'roles': response})


@app.route('/v1/admin/user/<user_id>/roles', methods=['GET'])
@rate_limiter(settings.rate_limit, settings.time_period)
@api.validate(resp=Response(HTTP_200=RoleIds,
                            HTTP_429=ErrorStr), tags=['admin'])
@check_role_wrap(['theatre_admin'])
def get_user_roles(user_id: str):
    """ Получить все роли пользователя """
    client_id = keycloak_admin.get_client_id(settings.client_id)
    roles = keycloak_admin.get_client_roles_of_user(client_id=client_id, user_id=user_id)
    result_roles = []
    if roles:
        result_roles = [{'id': role['id'], 'role_name': role['name']} for role in roles]
    return jsonify({'result': result_roles})


@app.route('/v1/admin/user/<user_id>/name', methods=['GET'])
@rate_limiter(settings.rate_limit, settings.time_period)
@api.validate(resp=Response(HTTP_200=StrResponse,
                            HTTP_429=ErrorStr), tags=['admin'])
@check_role_wrap(['theatre_admin'])
def get_user_name(user_id: str):
    """ Получить имя пользователя """
    user_data = keycloak_admin.get_user(user_id)
    user_name = ''
    if user_data:
        user_name = user_data['username']
    return jsonify({'result': user_name})


@app.route('/v1/admin/user/<email>', methods=['GET'])
@rate_limiter(settings.rate_limit, settings.time_period)
@api.validate(resp=Response(HTTP_200=StrResponse,
                            HTTP_429=ErrorStr), tags=['admin'])
@check_role_wrap(['theatre_admin'])
def get_user_id_by_email(email: str):
    """ Получить имя пользователя """
    user_data = keycloak_admin.get_users(query={'email': email})
    user_id = -1
    if user_data:
        user_id = user_data[0]['id']
    return jsonify({'result': user_id})


@app.route('/v1/admin/roles/<role_name>/delete', methods=['POST'])
@rate_limiter(settings.rate_limit, settings.time_period)
@api.validate(resp=Response(HTTP_200=BoolResponse, HTTP_400=None, HTTP_409=None, HTTP_404=None,
                            HTTP_429=ErrorStr), tags=['admin'])
@check_role_wrap(['theatre_admin'])
def delete_role(role_name: str):
    """ Удалить роль """
    try:
        client_id = keycloak_admin.get_client_id(settings.client_id)
        keycloak_admin.delete_client_role(client_role_id=client_id, role_name=role_name)
        return jsonify({'result': True})
    except KeycloakPostError as err:
        return json.loads(err.response_body)['errorMessage'], err.response_code
    except KeycloakDeleteError:
        return messages.ROLE_NOT_FOUND


@app.route('/v1/admin/roles/<role_name>/change', methods=['POST'])
@rate_limiter(settings.rate_limit, settings.time_period)
@api.validate(
    body=Request(Role),
    resp=Response(HTTP_200=BoolResponse, HTTP_400=None, HTTP_409=None, HTTP_429=ErrorStr), tags=['admin'])
@check_role_wrap(['theatre_admin'])
def change_role(role_name: str):
    """ Изменить роль """
    try:
        body = request.json
        client_id = keycloak_admin.get_client_id(settings.client_id)
        keycloak_admin.update_client_role(client_role_id=client_id, role_name=role_name,
                                          payload={'name': body['role_name'], 'clientRole': True})
        return jsonify({'result': True})
    except KeycloakPutError as e:
        return json.loads(e.response_body)['error'], e.response_code


@app.route('/v1/admin/grant_role', methods=['POST'])
@rate_limiter(settings.rate_limit, settings.time_period)
@api.validate(body=Request(UserRole),
              resp=Response(HTTP_200=BoolResponse, HTTP_400=None, HTTP_409=None,
                            HTTP_429=ErrorStr),
              tags=['admin'])
@check_role_wrap(['theatre_admin'])
def grant_role():
    """ Выдать роль пользователю """
    try:
        body = request.json
        client_id, user_id, role_id = prep_user_data(body)
        keycloak_admin.assign_client_role(client_id=client_id, user_id=user_id, roles=role_id)
        return jsonify({'result': True})
    except KeycloakPostError as e:
        return json.loads(e.response_body)['errorMessage'], e.response_code


@app.route('/v1/admin/grant_role_by_id', methods=['POST'])
@rate_limiter(settings.rate_limit, settings.time_period)
@api.validate(body=Request(UserIdRole),
              resp=Response(HTTP_200=BoolResponse, HTTP_400=None, HTTP_409=None,
                            HTTP_429=ErrorStr),
              tags=['admin'])
@check_role_wrap(['theatre_admin'])
def grant_role_by_id():
    """ Выдать роль пользователю """
    try:
        body = request.json
        client_id, _, role_id = prep_user_data(body)
        keycloak_admin.assign_client_role(client_id=client_id, user_id=body.get('user_id'), roles=role_id)
        return jsonify({'result': True})
    except KeycloakPostError as e:
        return json.loads(e.response_body)['errorMessage'], e.response_code


@app.route('/v1/admin/revoke_role', methods=['POST'])
@rate_limiter(settings.rate_limit, settings.time_period)
@api.validate(body=Request(UserRole),
              resp=Response(HTTP_200=BoolResponse, HTTP_400=None, HTTP_409=None,
                            HTTP_429=ErrorStr),
              tags=['admin'])
@check_role_wrap(['theatre_admin'])
def revoke_role():
    """ Забрать роль у пользователя """
    try:
        body = request.json
        client_id, user_id, role_id = prep_user_data(body)
        keycloak_admin.delete_client_roles_of_user(client_id=client_id, user_id=user_id,
                                                   roles=role_id)
        return jsonify({'result': True})
    except KeycloakPostError as e:
        return json.loads(e.response_body)['errorMessage'], e.response_code
