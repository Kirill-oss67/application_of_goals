from pytest_factoryboy import register

from tests.factories import UserFactory, BoardFactory, BoardParticipantFactory, GoalCategoryFactory, GoalCommentFactory, \
    GoalFactory

register(UserFactory)
register(BoardFactory)
register(BoardParticipantFactory)
register(GoalCategoryFactory)
register(GoalCommentFactory)
register(GoalFactory)

pytest_plugins = 'tests.fixtures'
