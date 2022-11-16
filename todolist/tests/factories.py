import factory

from core.models import User
from goals.models import Goal, GoalCategory, Board, BoardParticipant, GoalComment


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('name')
    first_name = 'First name'
    last_name = 'Last name'
    email = 'email@mail.ru'
    password = 'Password8956'


class BoardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Board

    title = factory.Faker('name')
    is_deleted = False


class BoardParticipantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BoardParticipant

    board = factory.SubFactory(BoardFactory)
    user = factory.SubFactory(UserFactory)
    role = 1


class GoalCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoalCategory

    title = 'Test category'
    is_deleted = False
    user = factory.SubFactory(UserFactory)
    board = factory.SubFactory(BoardFactory)


class GoalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Goal

    title = 'Test goal'
    description = 'Test description'
    user = factory.SubFactory(UserFactory)
    category = factory.SubFactory(GoalCategoryFactory)

    status = 1
    priority = 2
    due_date = '2022-11-14'


class GoalCommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoalComment

    text = 'Test text'
    goal = factory.SubFactory(GoalFactory)
    user = factory.SubFactory(UserFactory)
