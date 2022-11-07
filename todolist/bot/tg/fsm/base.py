from abc import ABC, abstractmethod
from enum import Enum


class Storage(ABC):
    @abstractmethod
    def get_state(self, chat_id: int) -> Enum | None:
        raise NotImplementedError

    @abstractmethod
    def get_data(self, chat_id: int) -> dict:
        raise NotImplementedError

    @abstractmethod
    def set_state(self, chat_id: int, state: Enum) -> None:
        raise NotImplementedError

    @abstractmethod
    def set_data(self, chat_id: int, data: dict) -> None:
        raise NotImplementedError

    @abstractmethod
    def reset_state(self, chat_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def reset_date(self, chat_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def reset(self, chat_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def update_date(self, chat_id: int, **kwargs) -> None:
        raise NotImplementedError
