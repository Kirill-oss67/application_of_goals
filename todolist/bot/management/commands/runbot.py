import logging
import os
from datetime import datetime
from enum import IntEnum, auto

from django.core.management import BaseCommand
from pydantic import BaseModel

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.fsm.memory_storage import MemoryStorage
from bot.tg.models import Message
from goals.models import Goal, GoalCategory, BoardParticipant
from todolist import settings

logger = logging.getLogger(__name__)


class NewGoal(BaseModel):
    cat_id: int | None = None
    goal_title: str | None = None

    @property
    def is_completed(self) -> bool:
        return None not in [self.cat_id, self.goal_title]


class StateEnum(IntEnum):
    CREATE_CATEGORY_SELECT = auto()
    CHOSEN_CATEGORY = auto()


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient(settings.BOT_TOKEN)
        self.storage = MemoryStorage()

    @staticmethod
    def _generate_verification_code() -> str:
        return os.urandom(12).hex()

    def handle_unverified_user(self, msg: Message, tg_user: TgUser):
        code: str = self._generate_verification_code()
        tg_user.verification_code = code
        tg_user.save(update_fields=('verification_code',))
        self.tg_client.send_message(
            chat_id=msg.chat.id,
            text=f'[verification_code] {tg_user.verification_code}'
        )

    def handle_goals_list(self, msg: Message, tg_user: TgUser):
        resp_goals: list[str] = [
            f'#{goal.id} {goal.title}'
            for goal in Goal.objects.filter(user_id=tg_user.user_id)]
        if resp_goals:
            self.tg_client.send_message(msg.chat.id, '\n'.join(resp_goals))
        else:
            self.tg_client.send_message(msg.chat.id, 'you have no goals')

    def handle_goal_categories_list(self, msg: Message, tg_user: TgUser):
        resp_categories: list[str] = [
            f'#{cat.id} {cat.title}'
            for cat in GoalCategory.objects.filter(
                board__participants__user_id=tg_user.user_id,
                is_deleted=False
            )
        ]
        if resp_categories:
            self.tg_client.send_message(msg.chat.id, 'Select category\n' + '\n'.join(resp_categories))
        else:
            self.tg_client.send_message(msg.chat.id, 'you have no categories')

    def handle_save_selected_category(self, msg: Message, tg_user: TgUser):
        if msg.text.isdigit():
            cat_id = int(msg.text)
            if GoalCategory.objects.filter(
                    board__participants__user_id=tg_user.user_id,
                    board__participants__role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
                    is_deleted=False,
                    id=cat_id
            ).exists():
                self.storage.update_date(chat_id=msg.chat.id, cat_id=cat_id)
                self.tg_client.send_message(msg.chat.id, '[set title]')
                self.storage.set_state(msg.chat.id, state=StateEnum.CHOSEN_CATEGORY)
            else:
                self.tg_client.send_message(msg.chat.id, '[category not found]')
        else:
            self.tg_client.send_message(msg.chat.id, '[invalid category id]')

    def handle_save_new_cat(self, msg: Message, tg_user: TgUser):
        goal = NewGoal(**self.storage.get_data(tg_user.chat_id))
        goal.goal_title = msg.text
        if goal.is_completed:
            Goal.objects.create(
                title=goal.goal_title,
                category_id=goal.cat_id,
                user_id=tg_user.user_id,
                due_date=datetime.now()
            )
            self.tg_client.send_message(msg.chat.id, '[New goal created]')
        else:
            self.tg_client.send_message(msg.chat.id, '[something went wrong]')
        self.storage.reset(tg_user.chat_id)

    def handle_verified_user(self, msg: Message, tg_user: TgUser):
        if msg.text == '/goals':
            self.handle_goals_list(msg, tg_user)
        elif msg.text == '/create':
            self.handle_goal_categories_list(msg, tg_user)
            self.storage.set_state(msg.chat.id, state=StateEnum.CREATE_CATEGORY_SELECT)
            self.storage.set_data(msg.chat.id, data=NewGoal().dict())

        elif msg.text == '/cancel' and self.storage.get_state(tg_user.chat_id):
            self.storage.reset(tg_user.chat_id)
            self.tg_client.send_message(msg.chat.id, '[canceled]')
        elif state := self.storage.get_state(tg_user.chat_id):
            match state:
                case StateEnum.CREATE_CATEGORY_SELECT:
                    self.handle_save_selected_category(msg, tg_user)
                case StateEnum.CHOSEN_CATEGORY:
                    self.handle_save_new_cat(msg, tg_user)
                case _:
                    logger.warning('Invalid state: %s', state)

        elif msg.text.startswith('/'):
            self.tg_client.send_message(msg.chat.id, '[unknown command]')

    def handle_message(self, msg: Message):
        tg_user, _ = TgUser.objects.select_related('user').get_or_create(
            chat_id=msg.chat.id,
            defaults={
                'username': msg.from_.username
            }
        )
        if tg_user.user:
            self.handle_verified_user(msg=msg, tg_user=tg_user)
        else:
            self.handle_unverified_user(msg=msg, tg_user=tg_user)

    def handle(self, *args, **options):
        offset = 0
        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                self.handle_message(msg=item.message)
