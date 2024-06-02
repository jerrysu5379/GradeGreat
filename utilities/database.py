from abc import ABC, abstractmethod


class Database(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def create_user_table(self):
        pass

    @abstractmethod
    def register_user(self, username, password):
        pass

    @abstractmethod
    def authenticate_user(self, username, password):
        pass