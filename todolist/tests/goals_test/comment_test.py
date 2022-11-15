import pytest

from goals.serializers import GoalCommentSerializer
from tests.factories import GoalCommentFactory


@pytest.mark.django_db
def test_comment_create(client, get_credentials, goal, board_participant):
    """Создание комментария"""
    data = {
        'text': 'text',
        'goal': goal.id,
    }

    response = client.post(
        path='/goals/goal_comment/create',
        HTTP_AUTHORIZATION=get_credentials,
        data=data,
        content_type='application/json'
    )

    assert response.status_code == 201
    assert response.data['text'] == data['text']
    assert response.data['goal'] == data['goal']


@pytest.mark.django_db
def test_comment_list(client, get_credentials, goal, board_participant):
    """Список комментариев"""
    comments = GoalCommentFactory.create_batch(10, user=goal.user, goal=goal)
    comments.sort(key=lambda x: x.id, reverse=True)

    response = client.get(
        path='/goals/goal_comment/list',
        HTTP_AUTHORIZATION=get_credentials
    )

    assert response.status_code == 200
    assert response.data == GoalCommentSerializer(comments, many=True).data


@pytest.mark.django_db
def test_comment_retrieve(client, get_credentials, goal_comment, board_participant):
    """Просмотр комментария"""
    response = client.get(
        path=f'/goals/goal_comment/{goal_comment.id}',
        HTTP_AUTHORIZATION=get_credentials
    )

    assert response.status_code == 200
    assert response.data == GoalCommentSerializer(goal_comment).data


@pytest.mark.django_db
def test_comment_update(client, get_credentials, goal_comment, board_participant):
    """Обновление комментария"""
    new_text = 'updated_text'

    response = client.patch(
        path=f'/goals/goal_comment/{goal_comment.id}',
        HTTP_AUTHORIZATION=get_credentials,
        data={'text': new_text},
        content_type='application/json'
    )

    assert response.status_code == 200
    assert response.data.get('text') == new_text


@pytest.mark.django_db
def test_comment_delete(client, get_credentials, goal_comment, board_participant):
    """Удаление комментария"""
    response = client.delete(
        path=f'/goals/goal_comment/{goal_comment.id}',
        HTTP_AUTHORIZATION=get_credentials,
    )

    assert response.status_code == 204
    assert response.data is None
