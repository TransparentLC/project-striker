import pygame
import random
import typing

import lib.bullet
import lib.globals
import lib.sprite.explosion
import lib.sprite.player
import lib.sound

class EnemyBullet(lib.bullet.Bullet):
    def __init__(
        self,
        position: pygame.Vector2,
        speed: float,
        angle: float,
        size: float,
        texture: pygame.Surface,
        update: typing.Callable[[lib.bullet.Bullet], None] = None
    ) -> None:
        super().__init__(lib.globals.groupEnemyBullet)
        self.position = pygame.Vector2(position)
        self.angle = angle
        self.speedRadius = speed
        self.size = size
        self.textures = (texture,)
        self.updateCustom = update
        self.grazed = False

    def update(self, *args, **kwargs) -> None:
        if self.updateCustom:
            self.updateCustom(self)
        super().update(*args, **kwargs)

        s: lib.sprite.player.Player = lib.globals.groupPlayer.sprite
        if not s.deathWait:
            for h in s.hitboxAbsolute:
                distance = (h.offset - self.position).length() - h.size - self.size
                if distance < 0:
                    if not s.invincibleRemain:
                        s.explode()
                    self.explode()
                    break
                elif distance < 10 and not self.grazed:
                    self.grazed = True
                    lib.globals.grazeCount += 1
                    lib.globals.score += len(lib.globals.groupEnemyBullet) // 5
                    lib.sound.sfx[random.choice(('GRAZE_A', 'GRAZE_B'))].play()
                    break
