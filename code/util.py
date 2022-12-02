from os import walk
import pygame


def import_folder(path):
    surface_list = []

    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list


def import_surface(path: str) -> pygame.Surface:
    return pygame.image.load(path).convert_alpha()


def gradient(window, left_colour, right_colour, target_rect):
    """ Draw a horizontal-gradient filled rectangle covering <target_rect> """
    colour_rect = pygame.Surface((2, 2))  # tiny! 2x2 bitmap
    pygame.draw.line(colour_rect, left_colour, (0, 0), (0, 1))  # left colour line
    pygame.draw.line(colour_rect, right_colour, (1, 0), (1, 1))  # right colour line
    colour_rect = pygame.transform.smoothscale(colour_rect, (target_rect.width, target_rect.height))  # stretch!
    window.blit(colour_rect, target_rect)  # paint it


def write_to_file(file_name: str, data: [str]):
    with open(file_name, 'w') as file:
        for line in data:
            file.write(line + '\n')


def read_from_file(file_name: str) -> [str]:
    lines = []
    with open(file_name, 'r') as file:
        for line in file:
            lines.append(line.strip())
    return lines
