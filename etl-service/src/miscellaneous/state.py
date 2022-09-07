from typing import Any

from .storage import BaseStorage


class State:
    def __init__(self, storage: BaseStorage):
        self.storage: BaseStorage = storage
        self.kv_storage = self.storage.retrieve_state()

    def set_state(self, key: str, value: Any) -> None:
        self.kv_storage[key] = value
        self.storage.save_state(self.kv_storage)

    def get_state(self, key: str) -> Any:
        return self.kv_storage[key] if key in self.kv_storage else None
