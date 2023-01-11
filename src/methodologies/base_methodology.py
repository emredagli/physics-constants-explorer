from abc import ABC, abstractmethod
from collections import OrderedDict

from src.quantity import Quantity
from src.scope import Scope


class BaseMethodology(ABC):
    candidates: OrderedDict = None
    target: Quantity
    scope: Scope
    settings: dict

    def __init__(self, target, scope, settings):
        self.target = target
        self.scope = scope
        self.settings = settings

    @abstractmethod
    def find_matched(self):
        pass

