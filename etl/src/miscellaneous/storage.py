import abc
import json

import yaml


class BaseStorage:
    @abc.abstractmethod
    def save_state(self, state: dict) -> None:
        """Сохранить состояние в постоянное хранилище"""
        pass

    @abc.abstractmethod
    def retrieve_state(self) -> dict:
        """Загрузить состояние локально из постоянного хранилища"""
        pass


class JsonFileStorage(BaseStorage):
    def __init__(self, file_path: str):
        self.file_path: str = file_path

    def save_state(self, state: dict) -> None:
        with open(self.file_path, 'w') as file:
            file.write(json.dumps(state))

    def retrieve_state(self) -> dict:
        with open(self.file_path, 'r') as file:
            try:
                state: {} = json.loads(file.read())

            except json.decoder.JSONDecodeError:
                self.save_state({})
                state = {}

        return state


class YMLFileStorage(BaseStorage):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def save_state(self, state: dict) -> None:
        with open(self.file_path, 'w') as file:
            yaml.safe_dump(state, file)

    def retrieve_state(self) -> dict:
        try:
            with open(self.file_path, 'r') as file:
                state: {} = yaml.safe_load(file)

        except FileNotFoundError:
            state = None

        if state is None:
            self.save_state({})
            state = {}

        return state
