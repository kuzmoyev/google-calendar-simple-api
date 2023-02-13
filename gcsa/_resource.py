from abc import ABC, abstractmethod


class Resource(ABC):
    @property
    @abstractmethod
    def id(self):
        pass
