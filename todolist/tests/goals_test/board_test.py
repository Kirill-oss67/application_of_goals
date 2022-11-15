import pytest

from goals.serializers import BoardSerializer, BoardListSerializer
from tests.factories import BoardFactory, BoardParticipantFactory


@pytest.mark.django_db
def test_board_create(client, get_credentials, user):
    """Создание доски"""
    data = {
        'title': 'title',
        'user': user.id,
    }

    response = client.post(
        path='/goals/board/create',
        HTTP_AUTHORIZATION=get_credentials,
        data=data,
        content_type='application/json'
    )

    assert response.status_code == 201
    assert response.data['title'] == data['title']


@pytest.mark.django_db
def test_board_list(client, get_credentials, board_participant):
    """Список досок"""
    boards = [board_participant.board]
    boards.extend(BoardFactory.create_batch(10))
    for board in boards[1:]:
        BoardParticipantFactory.create(user=board_participant.user, board=board)

    response = client.get(
        path='/goals/board/list',
        HTTP_AUTHORIZATION=get_credentials
    )

    assert response.status_code == 200
    assert response.data == BoardListSerializer(boards, many=True).data


@pytest.mark.django_db
def test_board_retrieve(client, get_credentials, board, board_participant):
    """Просмотр доски"""
    response = client.get(
        path=f'/goals/board/{board.id}',
        HTTP_AUTHORIZATION=get_credentials
    )

    assert response.status_code == 200
    assert response.data == BoardSerializer(board).data


@pytest.mark.django_db
def test_board_update(client, get_credentials, board, board_participant):
    """Редактирование доски"""
    new_title = 'updated_title'

    response = client.patch(
        path=f'/goals/board/{board.id}',
        HTTP_AUTHORIZATION=get_credentials,
        data={'title': new_title},
        content_type='application/json'
    )

    assert response.status_code == 200
    assert response.data.get('title') == new_title


@pytest.mark.django_db
def test_board_delete(client, get_credentials, board, board_participant):
    """Удаление доски"""
    response = client.delete(
        path=f'/goals/board/{board.id}',
        HTTP_AUTHORIZATION=get_credentials,
    )

    assert response.status_code == 204
    assert response.data is None
