import enum
import pygame

class Scene(enum.IntEnum):
    TITLE = enum.auto()
    STG = enum.auto()
    RESULT = enum.auto()

BACKGROUND_TITLE = pygame.image.load('assets/ui-title-background.png').convert(24, pygame.HWACCEL)
BACKGROUND_STG = pygame.image.load('assets/ui-stg-background.png').convert(24, pygame.HWACCEL)
BACKGROUND_RESULT = pygame.image.load('assets/ui-result-background.png').convert(24, pygame.HWACCEL)