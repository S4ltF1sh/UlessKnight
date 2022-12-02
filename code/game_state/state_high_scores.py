import pygame.key

from code.game_state import title_font, body_font
from code.game_state.state_base import BaseState
from code.util import read_from_file


class HighScoresState(BaseState):
    __TITLE_POS = (100, 100)
    __HIGH_SCORES_POS = (100, 200)
    events = {"BACK": "BACK"}

    def __init__(self, on_select):
        super(HighScoresState, self).__init__(on_select)
        self.high_score_title = title_font.render('High Scores', True, (255, 255, 255))
        self.high_scores = [body_font.render(f'{s}', True, (255, 255, 255))
                            for s in read_from_file('../high_scores.txt')]
        self.on_option_selected = on_select

    def draw(self, screen):
        screen.blit(self.high_score_title, self.__TITLE_POS)
        for i, score in enumerate(self.high_scores):
            screen.blit(score, (self.__HIGH_SCORES_POS[0], self.__HIGH_SCORES_POS[1] + i * 50))

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.on_option_selected(self.events["BACK"])
