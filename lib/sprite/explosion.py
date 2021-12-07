import pygame
import random

import lib.globals
import lib.sprite

class Explosion(lib.sprite.Sprite):
    def __init__(self, position: pygame.Vector2) -> None:
        super().__init__(lib.globals.groupParticle)
        self.position = position
        self.speed = pygame.Vector2()
        self.interval = 5

    def update(self) -> None:
        super().update()

        if self.frameCounter > len(self.textures) * self.interval:
            self.kill()

class ExplosionBullet(Explosion):
    def __init__(self, position: pygame.Vector2) -> None:
        super().__init__(position + pygame.Vector2(random.randint(-3, 3), random.randint(-3, 3)))
        self.textures = tuple(pygame.image.load(f'assets/explode-bullet-{i}.webp').convert_alpha() for i in range(3))
        self.interval = 3

class ExplosionPlaneSmallA(Explosion):
    def __init__(self, position: pygame.Vector2) -> None:
        super().__init__(position)
        self.textures = tuple(pygame.image.load(f'assets/explode-plane-a-{i}.webp').convert_alpha() for i in range(8))

class ExplosionPlaneSmallB(Explosion):
    def __init__(self, position: pygame.Vector2) -> None:
        super().__init__(position)
        self.textures = tuple(pygame.image.load(f'assets/explode-plane-b-{i}.webp').convert_alpha() for i in range(8))

class ExplosionPlaneMediumA(Explosion):
    def __init__(self, position: pygame.Vector2) -> None:
        super().__init__(position)
        self.textures = tuple(pygame.image.load(f'assets/explode-plane-c-{i}.webp').convert_alpha() for i in range(8))

class ExplosionPlaneMediumB(Explosion):
    def __init__(self, position: pygame.Vector2) -> None:
        super().__init__(position)
        self.textures = tuple(pygame.image.load(f'assets/explode-plane-d-{i}.webp').convert_alpha() for i in range(8))

class ExplosionPlaneLarge(Explosion):
    def __init__(self, position: pygame.Vector2) -> None:
        super().__init__(position)
        self.textures = tuple(pygame.image.load(f'assets/explode-plane-e-{i}.webp').convert_alpha() for i in range(8))

class ExplosionPlayer(Explosion):
    def __init__(self, position: pygame.Vector2) -> None:
        super().__init__(position)
        self.textures = tuple(pygame.image.load(f'assets/explode-player-{i}.webp').convert_alpha() for i in range(15))
