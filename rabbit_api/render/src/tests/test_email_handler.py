from render.src.tests.messages import incoming_message, outcoming_message, outcoming_message_bad_shortener


def test_email_handler(mock_url_shortener_post, mock_auth_service, email_message_handler):
    """Proccess incoming message."""
    result = email_message_handler.proccess_message(incoming_message.copy())
    messages = [message for message in result]
    assert len(incoming_message['users']) == len(messages)
    assert outcoming_message == messages[0].dict()


def test_email_handler_bad_shortener(mock_bad_url_shortener_post, mock_auth_service, email_message_handler):
    """Process incoming message when url shortener is not available."""
    result = email_message_handler.proccess_message(incoming_message.copy())
    messages = [message for message in result]
    assert len(incoming_message['users']) == len(messages)
    assert outcoming_message_bad_shortener == messages[0].dict()
