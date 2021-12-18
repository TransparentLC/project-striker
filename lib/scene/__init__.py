import pygame
import typing

class SceneProtrol(typing.Protocol):
    @staticmethod
    def update():
        pass

    @staticmethod
    def draw(surface: pygame.Surface):
        pass
