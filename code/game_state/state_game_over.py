import pygame.key

from code.button import Button
from code.game_state import title_font
from code.game_state.state_base import BaseState
from code.settings import screen_width, screen_height
from code.util import import_folder


class GameOverState(BaseState):
    events = {"RESTART": "RESTART", "QUIT": "QUIT"}
    BUTTONS_SPACE_BETWEEN = 50
    BUTTONS_MARGIN_TOP = 150

    def __init__(self, score_text, on_select):
        super().__init__(on_select)
        self.score_surface = title_font.render(score_text, True, (255, 255, 255))
        self.current_button = 0
        self.selected_bt = []
        self.not_selected_bt = []
        self.__load_buttons()
        self.__reposition_buttons((screen_width, screen_height))
        self.__on_select = on_select

    def __scale_buttons(self, scale):
        for button in self.selected_bt:
            button.scale(scale)
        for button in self.not_selected_bt:
            button.scale(scale)

    def __load_buttons(self):
        for surface in import_folder("../graphics/button/selected"):
            self.selected_bt += [Button(surface)]
        for surface in import_folder("../graphics/button/notselected"):
            self.not_selected_bt += [Button(surface)]
        self.__scale_buttons(0.4)

    def __reposition_buttons(self, pos):
        center_screen = (pos[0] / 2, pos[1] / 2)
        total_length = self.selected_bt[0].get_width() * len(self.selected_bt) + self.BUTTONS_SPACE_BETWEEN * (
                len(self.selected_bt) - 1)
        start_pos = (center_screen[0] - total_length / 2, center_screen[1])
        for i in range(len(self.selected_bt)):
            self.selected_bt[i].set_position((start_pos[0] + i * (
                    self.selected_bt[i].get_width() + self.BUTTONS_SPACE_BETWEEN),
                                              start_pos[1] + self.BUTTONS_MARGIN_TOP))
            self.not_selected_bt[i].set_position((start_pos[0] + i * (
                    self.not_selected_bt[i].get_width() + self.BUTTONS_SPACE_BETWEEN),
                                                  start_pos[1] + self.BUTTONS_MARGIN_TOP))

    def draw(self, screen):
        screen.blit(title_font.render("GAME OVER", True, (255, 255, 255)), (screen_width / 2 - 200, 50))
        screen.blit(self.score_surface,
                    (screen_width / 2 - self.score_surface.get_width() / 2, screen_height / 2 - 100))
        for i in range(len(self.selected_bt)):
            if i == self.current_button:
                self.selected_bt[i].draw(screen)
            else:
                self.not_selected_bt[i].draw(screen)

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.current_button = (self.current_button - 1) % len(self.selected_bt)
                elif event.key == pygame.K_RIGHT:
                    self.current_button = (self.current_button + 1) % len(self.selected_bt)
                elif event.key == pygame.K_RETURN:
                    if self.current_button == 0:
                        self.__on_select(self.events["QUIT"])
                    elif self.current_button == 1:
                        self.__on_select(self.events["RESTART"])
