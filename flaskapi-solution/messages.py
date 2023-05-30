from http import HTTPStatus

INCORRECT_CREDENTIALS = 'Incorrect login/password', HTTPStatus.UNAUTHORIZED
INSUFFICIENT_PRIVILEGES = 'Insufficient privileges', HTTPStatus.FORBIDDEN
USER_EXIST = 'Error create user, login already exists', HTTPStatus.BAD_REQUEST
USER_CREATED = 'Success', HTTPStatus.CREATED
LOGOUT_SUCCES = 'Logout success', HTTPStatus.ACCEPTED
INCORRECT_TOKEN = 'Incorrect token', HTTPStatus.UNAUTHORIZED
ROLE_NOT_FOUND = 'Role with such name does not exist', HTTPStatus.NOT_FOUND
USER_UPDATED = 'User email or/and password updated', HTTPStatus.ACCEPTED
MAIL_SEND = 'Verify email sent', HTTPStatus.ACCEPTED
NOT_ACCEPTABLE = 'Not Acceptable', HTTPStatus.NOT_ACCEPTABLE
