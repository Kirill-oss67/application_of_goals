import pytest


@pytest.mark.django_db
def test_user_login(client, user):
    """Тест авторизации пользователя"""
    password = user.password

    user.set_password(password)
    user.save()

    response = client.post(
        path='/core/login',
        data={
            'username': user.username,
            'password': password,
        },
        content_type='application/json'
    )

    expected_response = {
        'id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email
    }

    assert response.status_code == 200
    assert response.data == expected_response
