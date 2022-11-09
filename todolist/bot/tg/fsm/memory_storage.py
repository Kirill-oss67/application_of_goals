from enum import Enum

from pydantic import BaseModel

from bot.tg.fsm.base import Storage


class StorageData(BaseModel):
    state: Enum | None = None
    data: dict = {}


class MemoryStorage(Storage):
    def __init__(self):
        self.data: dict[int, StorageData] = {}

    def _resolve_chat(self, chat_id: int):
        if chat_id not in self.data:
            self.data[chat_id] = StorageData()
        return self.data[chat_id]

    def get_state(self, chat_id: int) -> StorageData | None:
        return self._resolve_chat(chat_id).state

    def get_data(self, chat_id: int) -> dict:
        return self._resolve_chat(chat_id).data

    def set_state(self, chat_id: int, state: Enum) -> None:
        self._resolve_chat(chat_id).state = state

    def set_data(self, chat_id: int, data: dict) -> None:
        self._resolve_chat(chat_id).data = data

    def reset_state(self, chat_id: int) -> None:
        self._resolve_chat(chat_id).state = None

    def reset_date(self, chat_id: int) -> None:
        self._resolve_chat(chat_id).data.clear()

    def reset(self, chat_id: int) -> bool:
        return bool(self.data.pop(chat_id, None))

    def update_date(self, chat_id: int, **kwargs) -> None:
        self._resolve_chat(chat_id).data.update(**kwargs)
