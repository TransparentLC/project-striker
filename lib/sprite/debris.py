import pygame
import random

import lib.globals
import lib.sprite

class Debris(lib.sprite.Sprite):
    def __init__(self, position: pygame.Vector2, spreadSpeed: float, rotateSpeed: float) -> None:
        super().__init__(lib.globals.groupParticle)
        self.position = position
        self.speed = pygame.Vector2()
        self.speed.from_polar((spreadSpeed, random.randint(0, 360)))
        self.rotateSpeed = rotateSpeed
        self.interval = 10

    def update(self) -> None:
        super().update()
        self.angle += self.rotateSpeed
        if self.frameCounter > len(self.textures) * self.interval:
            self.kill()

class DebrisA(Debris):
    def __init__(self, position: pygame.Vector2, spreadSpeed: float, rotateSpeed: float) -> None:
        super().__init__(
            position + pygame.Vector2(random.randint(-10, 10), random.randint(-10, 10)),
            spreadSpeed,
            rotateSpeed,
        )
        self.textures = tuple(pygame.image.load(f'assets/debris-a-{i}.png').convert_alpha() for i in range(8))

class DebrisB(Debris):
    def __init__(self, position: pygame.Vector2, spreadSpeed: float, rotateSpeed: float) -> None:
        super().__init__(
            position + pygame.Vector2(random.randint(-10, 10), random.randint(-10, 10)),
            spreadSpeed,
            rotateSpeed,
        )
        self.textures = tuple(pygame.image.load(f'assets/debris-b-{i}.png').convert_alpha() for i in range(8))
