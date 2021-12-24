import typing
import pygame
import random

import lib.sprite
import lib.sprite.player
import lib.sound
import lib.globals
import lib.utils
import lib.bullet.player_bullet

class PlayerOption(lib.sprite.Sprite):
    texturesIdle = tuple(pygame.image.load(f'assets/player-option-idle-{i}.webp').convert_alpha() for i in range(2))
    texturesTurnL0 = tuple(pygame.image.load(f'assets/player-option-turn-l-0-{i}.webp').convert_alpha() for i in range(2))
    texturesTurnL1 = tuple(pygame.image.load(f'assets/player-option-turn-l-1-{i}.webp').convert_alpha() for i in range(2))
    texturesTurnR0 = tuple(pygame.image.load(f'assets/player-option-turn-r-0-{i}.webp').convert_alpha() for i in range(2))
    texturesTurnR1 = tuple(pygame.image.load(f'assets/player-option-turn-r-1-{i}.webp').convert_alpha() for i in range(2))

    offsetNormal: pygame.Vector2
    offsetSlow: pygame.Vector2
    angleNormal: float
    angleSlow: float
    shiftCounter: int
    shiftCounterLimit: int

    def __init__(
        self,
        shiftCounterLimit: int,
        offsetNormal: pygame.Vector2,
        offsetSlow: pygame.Vector2,
        angleNormal: float,
        angleSlow: float,
    ) -> None:
        super().__init__(lib.globals.groupPlayerOption)
        self.shiftCounter = 0
        self.speed = pygame.Vector2()
        self.interval = 5
        self.shiftCounterLimit = shiftCounterLimit
        self.offsetNormal = offsetNormal
        self.offsetSlow = offsetSlow
        self.angleNormal = angleNormal
        self.angleSlow = angleSlow
        self.shootWait = 0

    @property
    def textures(self) -> typing.Sequence[pygame.Surface]:
        s: lib.sprite.player.Player = lib.globals.groupPlayer.sprite
        if s.deathWait or s.textures == s.texturesIdle:
            return self.texturesIdle
        elif s.textures == s.texturesTurnL0:
            return self.texturesTurnL0
        elif s.textures == s.texturesTurnL1:
            return self.texturesTurnL1
        elif s.textures == s.texturesTurnR0:
            return self.texturesTurnR0
        elif s.textures == s.texturesTurnR1:
            return self.texturesTurnR1

    @property
    def angle(self) -> float:
        s: lib.sprite.player.Player = lib.globals.groupPlayer.sprite
        return s.angle + lib.utils.linearInterpolation(
            self.shiftCounter / self.shiftCounterLimit,
            self.angleNormal,
            self.angleSlow
        )

    @property
    def position(self) -> float:
        s: lib.sprite.player.Player = lib.globals.groupPlayer.sprite
        return s.position + lib.utils.linearInterpolation(
            self.shiftCounter / self.shiftCounterLimit,
            self.offsetNormal,
            self.offsetSlow
        ).rotate(-s.angle)

    @position.setter
    def position(self, value) -> None:
        # Computed property, shouldn't be assigned.
        pass

    @property
    def slow(self) -> bool:
        return lib.globals.keys[pygame.K_LSHIFT]

    def shoot(self) -> None:
        # Abstract
        pass

    def update(self) -> None:
        s: lib.sprite.player.Player = lib.globals.groupPlayer.sprite
        if not s.deathWait:
            if lib.globals.keys[pygame.K_LSHIFT]:
                self.shiftCounter = lib.utils.clamp(self.shiftCounter + 1, 0, self.shiftCounterLimit)
            else:
                self.shiftCounter = lib.utils.clamp(self.shiftCounter - 1, 0, self.shiftCounterLimit)

        if self.shootWait:
            self.shootWait -= 1
        if lib.globals.keys[pygame.K_z] and not self.shootWait and not s.deathWait:
            self.shoot()

        super().update()

# A机体：
# 高速      | 11x4     = 44/20f | 2.200/f | 1.000x | 4
# 高速Hyper | (11+5)x4 = 64/12f | 5.333/f | 2.424x | 4 12
# 低速和高速相同
class OptionTypeA(PlayerOption):
    def shoot(self) -> None:
        if lib.globals.groupPlayer.sprite.hyperRemain:
            lib.bullet.player_bullet.PlayerBullet(
                self.position,
                lib.bullet.player_bullet.bulletTextureHoming,
                size=lib.bullet.player_bullet.bulletSizeHoming, speed=4, angle=self.angle, damage=11,
                flags=lib.bullet.player_bullet.PlayerBulletFlags.HOMING
            )
            lib.bullet.player_bullet.PlayerBullet(
                self.position,
                lib.bullet.player_bullet.bulletTexture1WayHyper,
                size=lib.bullet.player_bullet.bulletSize1Way, speed=12, angle=self.angle, damage=5,
                flags=lib.bullet.player_bullet.PlayerBulletFlags.BULLET_CANCELLING
            )
            self.shootWait = 12
        else:
            lib.bullet.player_bullet.PlayerBullet(
                self.position,
                lib.bullet.player_bullet.bulletTextureHoming,
                size=lib.bullet.player_bullet.bulletSizeHoming, speed=4, angle=self.angle, damage=11,
                flags=lib.bullet.player_bullet.PlayerBulletFlags.HOMING
            )
            self.shootWait = 20
        lib.sound.sfx[random.choice(('PLAYER_SHOOT_A', 'PLAYER_SHOOT_B'))].play()

# B机体：
# 高速      | (5+6)x4 = 44/10f | 4.400/f | 1.000x | 8 10 10
# 高速Hyper | (7+6)x4 = 52/6f  | 8.667/f | 1.970x | 10 12 12
# 低速      | (5+3)x4 = 32/15f | 2.133/f | 1.000x | 8 10
# 低速Hyper | (7+3)x4 = 40/6f  | 6.667/f | 3.125x | 10 12
# 自机弹幕判定会稍微大一点
class OptionTypeB0(PlayerOption):
    def shoot(self) -> None:
        if lib.globals.groupPlayer.sprite.hyperRemain:
            lib.bullet.player_bullet.PlayerBullet(
                self.position,
                lib.bullet.player_bullet.bulletTexture2WayHyper,
                size=lib.bullet.player_bullet.bulletSize2Way * 3 // 2, speed=10, angle=self.angle, damage=7,
                flags=lib.bullet.player_bullet.PlayerBulletFlags.BULLET_CANCELLING
            )
            lib.bullet.player_bullet.PlayerBullet(
                self.position,
                lib.bullet.player_bullet.bulletTexture1WayHyper,
                size=lib.bullet.player_bullet.bulletSize1Way * 3 // 2, speed=12, angle=self.angle - 7, damage=3,
                flags=lib.bullet.player_bullet.PlayerBulletFlags.BULLET_CANCELLING
            )
            if not self.slow:
                lib.bullet.player_bullet.PlayerBullet(
                    self.position,
                    lib.bullet.player_bullet.bulletTexture1WayHyper,
                    size=lib.bullet.player_bullet.bulletSize1Way * 3 // 2, speed=12, angle=self.angle + 3, damage=3,
                    flags=lib.bullet.player_bullet.PlayerBulletFlags.BULLET_CANCELLING
                )
            self.shootWait = 6
        else:
            lib.bullet.player_bullet.PlayerBullet(
                self.position,
                lib.bullet.player_bullet.bulletTexture2Way,
                size=lib.bullet.player_bullet.bulletSize2Way * 3 // 2, speed=8, angle=self.angle, damage=5
            )
            lib.bullet.player_bullet.PlayerBullet(
                self.position,
                lib.bullet.player_bullet.bulletTexture1Way,
                size=lib.bullet.player_bullet.bulletSize1Way * 3 // 2, speed=10, angle=self.angle - 7, damage=3
            )
            if not self.slow:
                lib.bullet.player_bullet.PlayerBullet(
                    self.position,
                    lib.bullet.player_bullet.bulletTexture1Way,
                    size=lib.bullet.player_bullet.bulletSize1Way * 3 // 2, speed=10, angle=self.angle + 3, damage=3
                )
            self.shootWait = 10 if self.slow else 15
        lib.sound.sfx[random.choice(('PLAYER_SHOOT_A', 'PLAYER_SHOOT_B'))].play()

class OptionTypeB1(PlayerOption):
    def shoot(self) -> None:
        if lib.globals.groupPlayer.sprite.hyperRemain:
            lib.bullet.player_bullet.PlayerBullet(
                self.position,
                lib.bullet.player_bullet.bulletTexture2WayHyper,
                size=lib.bullet.player_bullet.bulletSize2Way * 4 // 3, speed=10, angle=self.angle, damage=5
            )
            lib.bullet.player_bullet.PlayerBullet(
                self.position,
                lib.bullet.player_bullet.bulletTexture1WayHyper,
                size=lib.bullet.player_bullet.bulletSize1Way * 4 // 3, speed=12, angle=self.angle + 7, damage=3
            )
            if not self.slow:
                lib.bullet.player_bullet.PlayerBullet(
                    self.position,
                    lib.bullet.player_bullet.bulletTexture1WayHyper,
                    size=lib.bullet.player_bullet.bulletSize1Way * 4 // 3, speed=12, angle=self.angle - 3, damage=3
                )
            self.shootWait = 6
        else:
            lib.bullet.player_bullet.PlayerBullet(
                self.position,
                lib.bullet.player_bullet.bulletTexture2Way,
                size=lib.bullet.player_bullet.bulletSize2Way * 4 // 3, speed=8, angle=self.angle, damage=7
            )
            lib.bullet.player_bullet.PlayerBullet(
                self.position,
                lib.bullet.player_bullet.bulletTexture1Way,
                size=lib.bullet.player_bullet.bulletSize1Way * 4 // 3, speed=10, angle=self.angle + 7, damage=3
            )
            if not self.slow:
                lib.bullet.player_bullet.PlayerBullet(
                    self.position,
                    lib.bullet.player_bullet.bulletTexture1Way,
                    size=lib.bullet.player_bullet.bulletSize1Way * 4 // 3, speed=10, angle=self.angle - 3, damage=3
                )
            self.shootWait = 10 if self.slow else 15
        lib.sound.sfx[random.choice(('PLAYER_SHOOT_A', 'PLAYER_SHOOT_B'))].play()

# C机体：
# 高速      | (9+4)x2  = 26/8f | 3.250/f | 1.000x | 10 13
# 高速Hyper | (11+5)x2 = 32/5f | 6.400/f | 1.969x | 11 14
# 低速和高速相同
class OptionTypeC(PlayerOption):
    def shoot(self) -> None:
        if lib.globals.groupPlayer.sprite.hyperRemain:
            lib.bullet.player_bullet.PlayerBullet(
                self.position,
                lib.bullet.player_bullet.bulletTexture2WayHyper,
                size=lib.bullet.player_bullet.bulletSize2Way, speed=11, angle=self.angle, damage=11,
                flags=lib.bullet.player_bullet.PlayerBulletFlags.BULLET_CANCELLING
            )
            lib.bullet.player_bullet.PlayerBullet(
                self.position,
                lib.bullet.player_bullet.bulletTexture1WayHyper,
                size=lib.bullet.player_bullet.bulletSize1Way, speed=14, angle=self.angle, damage=5,
                flags=lib.bullet.player_bullet.PlayerBulletFlags.BULLET_CANCELLING
            )
            self.shootWait = 5
        else:
            lib.bullet.player_bullet.PlayerBullet(
                self.position,
                lib.bullet.player_bullet.bulletTexture2Way,
                size=lib.bullet.player_bullet.bulletSize2Way, speed=10, angle=self.angle, damage=9
            )
            lib.bullet.player_bullet.PlayerBullet(
                self.position,
                lib.bullet.player_bullet.bulletTexture1Way,
                size=lib.bullet.player_bullet.bulletSize1Way, speed=13, angle=self.angle, damage=4
            )
            self.shootWait = 8
        lib.sound.sfx[random.choice(('PLAYER_SHOOT_A', 'PLAYER_SHOOT_B'))].play()
