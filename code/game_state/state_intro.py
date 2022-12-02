import pygame

from code.game_state import title_font, body_font
from code.game_state.state_base import BaseState


class IntroState(BaseState):
    __SPACE_BETWEEN_OPTIONS = 50
    __MARGIN_START = 100
    __GAME_TITLE = "Uless Knight"
    __MENU_OPTIONS = [
        "New Game",
        "High Scores",
        "Exit",
    ]
    events = {
        "NEW_GAME": "NEW_GAME",
        "HIGH_SCORES": "HIGH_SCORES",
        "EXIT": "EXIT",
    }
    TITLE_POS = (100, 100)
    OPTIONS_POS = (100, 550)
    OPTIONS_BACKGROUND_PADDING = (12, 5)

    def __init__(self, on_select):
        super(IntroState, self).__init__(on_select)
        self.title_surface = title_font.render(self.__GAME_TITLE, False, (255, 255, 255))
        self.options_surfaces = [body_font.render(option, False, (255, 255, 255)) for option in self.__MENU_OPTIONS]
        self.options_selected_index = 0

        self.on_select = on_select

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.options_selected_index = (self.options_selected_index + 1) % len(self.__MENU_OPTIONS)
                elif event.key == pygame.K_UP:
                    self.options_selected_index = (self.options_selected_index - 1) % len(self.__MENU_OPTIONS)
                elif event.key == pygame.K_RETURN:
                    if self.options_selected_index == 0:
                        self.on_select(self.events["NEW_GAME"])
                    elif self.options_selected_index == 1:
                        self.on_select(self.events["HIGH_SCORES"])
                    elif self.options_selected_index == 2:
                        self.on_select(self.events["EXIT"])

    def draw(self, screen):
        # Draw title and options
        screen.blit(self.title_surface, self.TITLE_POS)

        # Generate a background for the selected option
        options_selected_background = pygame.Surface((self.options_surfaces[self.options_selected_index].get_width() +
                                                      self.OPTIONS_BACKGROUND_PADDING[0] * 2,
                                                      self.options_surfaces[self.options_selected_index].get_height() +
                                                      self.OPTIONS_BACKGROUND_PADDING[1] * 2))
        options_selected_background.fill((255, 255, 255))
        options_selected_background.set_alpha(64)
        options_selected_pos = (self.OPTIONS_POS[0] - self.OPTIONS_BACKGROUND_PADDING[0],
                                self.OPTIONS_POS[1] + self.options_selected_index * self.__SPACE_BETWEEN_OPTIONS)
        screen.blit(options_selected_background, options_selected_pos)

        # Draw options
        for i, surface in enumerate(self.options_surfaces):
            screen.blit(surface, (self.OPTIONS_POS[0], self.OPTIONS_POS[1] + i * self.__SPACE_BETWEEN_OPTIONS))
