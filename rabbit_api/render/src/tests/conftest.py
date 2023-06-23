from http import HTTPStatus
from unittest.mock import patch, Mock

import pytest

from src.services.extraction import UserDataExtractor
from src.services.message_handler import EmailMessageHandler
from src.services.rendering import JanjaTemplateRender
from src.services.url_shortener import BitlyURLShortener
from src.tests.messages import bitly_response, auth_response


@pytest.fixture()
def email_message_handler():
    return EmailMessageHandler(
        UserDataExtractor('test', 'test'),
        JanjaTemplateRender(),
        BitlyURLShortener('test', 'test')
    )


@pytest.fixture()
def mock_url_shortener_post():
    with patch('render.src.services.url_shortener.requests.post') as post:
        json = bitly_response
        post.return_value = Mock(status_code=HTTPStatus.OK, json=lambda: json)
        yield post


@pytest.fixture()
def mock_bad_url_shortener_post():
    with patch('render.src.services.url_shortener.requests.post') as post:
        json = bitly_response
        post.return_value = Mock(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, json=lambda: json)
        yield post


@pytest.fixture()
def mock_auth_service():
    with patch('render.src.services.extraction.requests.get') as get:
        json = auth_response
        get.return_value = Mock(status_code=HTTPStatus.OK, json=lambda: json)
        yield get