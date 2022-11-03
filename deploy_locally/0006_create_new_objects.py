from django.db import migrations, transaction
from django.utils import timezone


def create_objects(apps, schema_editor):
    # Для загрузки кода моделей используется специальный метод apps.get_model
    # Он позволяет загрузить ровно то состояние модели, которое было на момент применения этой миграции
    # Импортировать настоящие классы – плохая практика
    # так как в будущем вы можете удалить/переименовать эти модели, и тогда у вас будут ошибки импорта

    User = apps.get_model("core", "User")
    Board = apps.get_model("goals", "Board")
    BoardParticipant = apps.get_model("goals", "BoardParticipant")
    GoalCategory = apps.get_model("goals", "GoalCategory")

    with transaction.atomic():  # Применяем все изменения одной транзакцией
        for user in User.objects.all():  # Для каждого пользователя
            new_board = Board.objects.create(
                title="Мои цели",
                created=timezone.now(),  # Проставляем вручную по той же причине, что описана вверху
                updated=timezone.now()
            )
            BoardParticipant.objects.create(
                user=user,
                board=new_board,
                role=1,  # Владелец, проставляем числом, не импортируем код по той же причине
                created=timezone.now(),
                updated=timezone.now()
            )

            # проставляем всем категориям пользователя его доску
            GoalCategory.objects.filter(user=user).update(board=new_board)


class Migration(migrations.Migration):
    dependencies = [
        ('goals', '0005_board_goalcategory_board_boardparticipant'),
    ]

    operations = [
        migrations.RunPython(create_objects)
    ]