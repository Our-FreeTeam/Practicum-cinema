incoming_message = {
    "users": [
        "ec1691fa-965a-4295-9ad4-efbf5290140a",
        "d9fd04bc-3877-4209-80c6-373bb8c22a10",
    ],
    "template": "Hi, {{name}}! You watched {{watched_movies}}! Click the link {{redirect_url}}",
    "subject": "Special offer",
    "content_id": "5dc33ad2-2985-4557-9cae-4cfe9da592a7",
    "watched_movies": 10,
    "redirect_url": "https://dev.bitly.com/",
    "notification_id": "d0a310ec-6612-47f8-8a26-e385e33bdbd0"
}

auth_response = {
    'email': "ik-d@yandex.ru",
    "name": "Irina",
    "user_id": 'ec1691fa-965a-4295-9ad4-efbf5290140a',
}

bitly_response = {'link': 'http://short_url.ru'}

outcoming_message = {
    "letter": f"Hi, {auth_response['name']}! You watched 10! Click the link {bitly_response['link']}",
    "subject": "Special offer",
    "user_id": auth_response['user_id'],
    "content_id": "5dc33ad2-2985-4557-9cae-4cfe9da592a7",
    "notification_id": "d0a310ec-6612-47f8-8a26-e385e33bdbd0",
    "email": auth_response['email']
}

outcoming_message_bad_shortener = {
    "letter": f"Hi, {auth_response['name']}! You watched 10! Click the link {incoming_message['redirect_url']}",
    "subject": "Special offer",
    "user_id": auth_response['user_id'],
    "content_id": "5dc33ad2-2985-4557-9cae-4cfe9da592a7",
    "notification_id": "d0a310ec-6612-47f8-8a26-e385e33bdbd0",
    "email": auth_response['email']
}
