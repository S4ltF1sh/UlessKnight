from abc import abstractmethod
from typing import Callable, List

import pygame.event


class BaseState:
    def __init__(self, on_select: Callable[[str], None]):
        self.on_select = on_select
        pass

    @property
    @abstractmethod
    def events(self) -> map:
        pass

    @abstractmethod
    def draw(self, screen: pygame.surface.Surface):
        pass

    @abstractmethod
    def update(self, events: List[pygame.event.Event]):
        pass
