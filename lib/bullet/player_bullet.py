import enum
import pygame
import random

import lib.bullet
import lib.bullet.enemy_bullet
import lib.constants
import lib.globals
import lib.sprite.enemy
import lib.sprite.explosion
import lib.sprite.item
import lib.sound
import lib.utils

class PlayerBulletFlags(enum.IntFlag):
    HOMING = enum.auto()
    LOCKING = enum.auto()
    BULLET_CANCELLING = enum.auto()

bulletTexture1Way = pygame.image.load(lib.utils.getResourceHandler('assets/player-bullet-a.webp')).convert_alpha()
bulletTexture2Way = pygame.image.load(lib.utils.getResourceHandler('assets/player-bullet-b.webp')).convert_alpha()
bulletTexture4Way = pygame.image.load(lib.utils.getResourceHandler('assets/player-bullet-c.webp')).convert_alpha()
bulletTexture1WayHyper = pygame.image.load(lib.utils.getResourceHandler('assets/player-bullet-a-hyper.webp')).convert_alpha()
bulletTexture2WayHyper = pygame.image.load(lib.utils.getResourceHandler('assets/player-bullet-b-hyper.webp')).convert_alpha()
bulletTexture4WayHyper = pygame.image.load(lib.utils.getResourceHandler('assets/player-bullet-c-hyper.webp')).convert_alpha()
bulletTextureHoming = pygame.image.load(lib.utils.getResourceHandler('assets/player-bullet-d.webp')).convert_alpha()

bulletSize1Way = 4
bulletSize2Way = 8
bulletSize4Way = 10
bulletSizeHoming = 4

class PlayerBullet(lib.bullet.Bullet):
    def __init__(self, position: pygame.Vector2, texture: pygame.Surface, size: float, speed: float, angle: float, damage: int, flags: int = 0) -> None:
        super().__init__(lib.globals.groupPlayerBullet)
        self.position = pygame.Vector2(position)
        self.textures = (texture,)
        self.size = size
        self.speedRadius = speed
        self.angle = angle
        self.damage = damage
        self.bulletCancelRemain = lib.constants.BULLET_CANCELLING_INITIAL_REMAIN
        self.flags = flags

        if self.flags & PlayerBulletFlags.LOCKING:
            ne = self.nearestEnemy
            if ne:
                self.angle = -pygame.Vector2().angle_to(ne.position - self.position) - 90

    @property
    def nearestEnemy(self) -> 'lib.sprite.enemy.Enemy':
        if len(lib.globals.groupEnemy):
            return min(lib.globals.groupEnemy, key=lambda s: self.position.distance_squared_to(s.position))
        else:
            return None

    def update(self) -> None:
        super().update()

        if self.flags & PlayerBulletFlags.HOMING:
            ne = self.nearestEnemy
            if ne:
                self.angle = lib.utils.clamp(
                    -pygame.Vector2().angle_to(ne.position - self.position) - 90,
                    self.angle - lib.constants.HOMING_ANGLE_RANGE,
                    self.angle + lib.constants.HOMING_ANGLE_RANGE,
                )

        for s in lib.globals.groupEnemy:
            s: lib.sprite.enemy.Enemy
            for h in s.hitboxAbsolute:
                if (h.offset - self.position).length() < h.size + self.size:
                    if s.invincibleRemain:
                        self.damage = 1
                    else:
                        s.hitpoint -= self.damage
                    return self.explode()

        if self.flags & PlayerBulletFlags.BULLET_CANCELLING:
            for b in lib.globals.groupEnemyBullet:
                b: lib.bullet.enemy_bullet.EnemyBullet
                if self.position.distance_squared_to(b.position) < self.size ** 2:
                    lib.sprite.item.PointClear(pygame.Vector2(self.position))
                    lib.globals.maxGetPoint = max(10000, lib.globals.maxGetPoint - max(4, len(lib.globals.groupEnemyBullet) // 32))
                    self.bulletCancelRemain -= 1
                    b.explode()
                    if not self.bulletCancelRemain:
                        return self.explode()

    def explode(self) -> None:
        super().explode()
        lib.globals.score += self.damage * (8 + lib.globals.maxGetPoint % 16)
        lib.sound.sfx[random.choice(('PLAYER_SHOOT_HIT_A', 'PLAYER_SHOOT_HIT_B', 'PLAYER_SHOOT_HIT_C', 'PLAYER_SHOOT_HIT_D'))].play()
