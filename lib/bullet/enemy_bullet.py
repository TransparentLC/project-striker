import pygame
import random

import lib.bullet
import lib.constants
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
        texture: pygame.Surface
        # update: typing.Callable[[lib.bullet.Bullet], None] = None
    ) -> None:
        super().__init__(lib.globals.groupEnemyBullet)
        self.position = pygame.Vector2(position)
        self.angle = angle
        self.speedRadius = speed
        self.size = size
        # self.textures = (texture,)
        self.texturesRotated = (pygame.transform.rotate(texture, angle),)
        # self.updateCustom = update
        self.grazed = False

    def update(self, *args, **kwargs) -> None:
        # if self.updateCustom:
        #     self.updateCustom(self)
        super().update(*args, **kwargs)

        s: lib.sprite.player.Player = lib.globals.groupPlayer.sprite
        if not s.deathWait:
            for h in s.hitbox:
                p = h.offset + s.position
                rSum = h.size + self.size
                # rCheck = rSum + lib.constants.GRAZE_RANGE
                d = p - self.position
                # if rCheck < d.y or d.y < -rCheck or rCheck < d.x or d.x < -rCheck:
                #     continue
                distance = d.length() - rSum
                if distance < 0:
                    if not s.invincibleRemain:
                        s.explode()
                    self.explode()
                    break
                elif distance < lib.constants.GRAZE_RANGE and not self.grazed and not s.invincibleRemain and not s.hyperRemain:
                    self.grazed = True
                    lib.globals.grazeCount += 1
                    lib.sound.sfx[random.choice(('GRAZE_A', 'GRAZE_B'))].play()
                    lib.globals.score += len(lib.globals.groupEnemyBullet)
                    if not lib.globals.groupBoss.sprite:
                        lib.globals.maxGetPoint += len(lib.globals.groupEnemyBullet)
                    break
