import base64
import pytest


@pytest.fixture
@pytest.mark.django_db
def get_credentials(client, user):
    """Получение токена для аутентификации пользователя"""
    password = user.password

    user.set_password(password)
    user.save()

    token = base64.b64encode(f'{user.username}:{password}'.encode()).decode()

    return 'Basic ' + token
