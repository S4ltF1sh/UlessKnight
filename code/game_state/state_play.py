import pygame.key

from code.game import Game
from code.game_state.state_base import BaseState
from code.settings import level_map


class PlayState(BaseState):
    events = {'PAUSE': 'PAUSE', 'WIN': 'WIN'}

    def __init__(self, on_select, screen: pygame.surface.Surface):
        super().__init__(on_select)
        self.__on_select = on_select
        self.level = Game(level_map, screen, self.on_win)

    def on_win(self, point):
        self.__on_select(self.events['WIN'] + ':' + str(point))

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.__on_select(self.events['PAUSE'])

    def draw(self, screen):
        self.level.run()
