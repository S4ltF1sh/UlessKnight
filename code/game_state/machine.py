from typing import Callable

import pygame

from code.game_state.state_game_over import GameOverState
from code.game_state.state_high_scores import HighScoresState
from code.game_state.state_intro import IntroState
from code.game_state.state_pause import PauseState
from code.game_state.state_play import PlayState


class Machine:
    events = {'EXIT': 'EXIT'}

    def __init__(self, on_select: Callable[[str], None], screen: pygame.surface.Surface):
        self.state = IntroState(on_select=self.__on_intro_events)
        self.cache_state = None
        self.__on_select = on_select
        self.screen = screen

    def set_state(self, state):
        self.state = state

    def __update(self, events):
        self.state.update(events)

    def __draw(self, screen):
        self.state.draw(screen)

    def run(self, screen):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.__on_select(self.events["EXIT"])
                return
        self.__update(events)
        self.__draw(screen)

    def __on_intro_events(self, event_code: str):
        if event_code == IntroState.events["NEW_GAME"]:
            self.set_state(PlayState(on_select=self.__on_play_events, screen=self.screen))
        elif event_code == IntroState.events["HIGH_SCORES"]:
            self.set_state(HighScoresState(on_select=self.__on_high_scores_events))
        elif event_code == IntroState.events["EXIT"]:
            self.__on_select(self.events["EXIT"])

    def __on_play_events(self, event_code: str):
        if event_code == PlayState.events["PAUSE"]:
            self.cache_state = self.state
            self.set_state(PauseState(on_select=self.__on_pause_events))
        elif event_code == PlayState.events["GAME_OVER"]:
            # self.set_state(GameOverState(on_select=self.__on_game_over_events, score_text="100"))
            pass

    def __on_pause_events(self, event_code: str):
        if event_code == PauseState.events["RESUME"]:
            self.set_state(self.cache_state)
            self.cache_state = None
            pass
        elif event_code == PauseState.events["QUIT"]:
            self.set_state(IntroState(on_select=self.__on_intro_events))
        elif event_code == PauseState.events["RESTART"]:
            self.set_state(PlayState(on_select=self.__on_play_events, screen=self.screen))

    def __on_game_over_events(self, event_code: str):
        if event_code == GameOverState.events["RESTART"]:
            self.set_state(PlayState(on_select=self.__on_play_events, screen=self.screen))
        elif event_code == GameOverState.events["QUIT"]:
            self.set_state(IntroState(on_select=self.__on_intro_events))

    def __on_high_scores_events(self, event_code: str):
        if event_code == HighScoresState.events["BACK"]:
            self.set_state(IntroState(on_select=self.__on_intro_events))
