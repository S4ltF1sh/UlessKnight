import pygame.key

from code.button import Button
from code.game_state import body_font, title_font
from code.game_state.state_base import BaseState
from code.settings import screen_width, screen_height
from code.util import import_folder


class PauseState(BaseState):
    __PAUSE = "PAUSE"
    events = {"RESTART": "RESTART", "QUIT": "QUIT", "RESUME": "RESUME"}
    BUTTONS_SPACE_BETWEEN = 50
    BUTTONS_MARGIN_TOP = 50
    HELP_TEXT_MARGIN_TOP = 150

    def __init__(self, on_select):
        super(PauseState, self).__init__(on_select)
        self.current_option_index = 0
        self.pause_text_surface = title_font.render(self.__PAUSE, True, (255, 255, 255))
        self.__on_select = on_select

        self.selected_bt = []
        self.not_selected_bt = []
        self.__load_buttons()
        self.__reposition_buttons_row((screen_width, screen_height))

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
        self.__scale_buttons(0.25)

    def __reposition_buttons_row(self, pos):
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
        screen.blit(self.pause_text_surface, self.pause_text_surface.get_rect(center=screen.get_rect().center))
        for i in range(len(self.selected_bt)):
            if i == self.current_option_index:
                self.selected_bt[i].draw(screen)
            else:
                self.not_selected_bt[i].draw(screen)
        if self.current_option_index == 0:
            text = body_font.render("Quit", True, (255, 255, 255))
            text_pos = text.get_rect(center=screen.get_rect().center)
            text_pos.y += self.HELP_TEXT_MARGIN_TOP
            screen.blit(text, text_pos)
        elif self.current_option_index == 1:
            text = body_font.render("Restart", True, (255, 255, 255))
            text_pos = text.get_rect(center=screen.get_rect().center)
            text_pos.y += self.HELP_TEXT_MARGIN_TOP
            screen.blit(text, text_pos)

    def update_keyboard_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.__on_select(self.events["RESUME"])
                elif event.key == pygame.K_RETURN:
                    if self.current_option_index == 0:
                        self.__on_select(self.events["QUIT"])
                    elif self.current_option_index == 1:
                        self.__on_select(self.events["RESTART"])
                elif event.key == pygame.K_LEFT:
                    self.current_option_index = (self.current_option_index - 1) % 2
                elif event.key == pygame.K_RIGHT:
                    self.current_option_index = (self.current_option_index + 1) % 2

    def update(self, events):
        self.update_keyboard_events(events)
