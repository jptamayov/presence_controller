import abc

class RepositoryABC(abc.ABC):

    @abc.abstractmethod
    def save(self, key: str, data: dict):
        pass

    @abc.abstractmethod
    def read(self, key: str) -> dict:
        pass


class DummyRepository(RepositoryABC):
    def read(self, key: str):
        return {}

    def save(self, key: str, data: dict):
        pass