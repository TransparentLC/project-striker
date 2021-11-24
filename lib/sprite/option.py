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
    texturesIdle = tuple(pygame.image.load(f'assets/player-option-idle-{i}.png').convert_alpha() for i in range(2))
    texturesTurnL0 = tuple(pygame.image.load(f'assets/player-option-turn-l-0-{i}.png').convert_alpha() for i in range(2))
    texturesTurnL1 = tuple(pygame.image.load(f'assets/player-option-turn-l-1-{i}.png').convert_alpha() for i in range(2))
    texturesTurnR0 = tuple(pygame.image.load(f'assets/player-option-turn-r-0-{i}.png').convert_alpha() for i in range(2))
    texturesTurnR1 = tuple(pygame.image.load(f'assets/player-option-turn-r-1-{i}.png').convert_alpha() for i in range(2))

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

class OptionTypeA(PlayerOption):
    def shoot(self) -> None:
        if lib.globals.groupPlayer.sprite.hyperRemain:
            lib.bullet.player_bullet.PlayerBullet(
                self.position,
                lib.bullet.player_bullet.bulletTextureHoming,
                size=lib.bullet.player_bullet.bulletSizeHoming, speed=4, angle=self.angle, damage=9,
                flags=lib.bullet.player_bullet.PlayerBulletFlags.HOMING
            )
            lib.bullet.player_bullet.PlayerBullet(
                self.position,
                lib.bullet.player_bullet.bulletTexture1WayHyper,
                size=lib.bullet.player_bullet.bulletSize1Way, speed=12, angle=self.angle, damage=5,
                flags=lib.bullet.player_bullet.PlayerBulletFlags.BULLET_CANCELLING
            )
            self.shootWait = 15
        else:
            lib.bullet.player_bullet.PlayerBullet(
                self.position,
                lib.bullet.player_bullet.bulletTextureHoming,
                size=lib.bullet.player_bullet.bulletSizeHoming, speed=4, angle=self.angle, damage=9,
                flags=lib.bullet.player_bullet.PlayerBulletFlags.HOMING
            )
            self.shootWait = 25
        lib.sound.sfx[random.choice(('PLAYER_SHOOT_A', 'PLAYER_SHOOT_B'))].play()

class OptionTypeB0(PlayerOption):
    def shoot(self) -> None:
        if lib.globals.groupPlayer.sprite.hyperRemain:
            lib.bullet.player_bullet.PlayerBullet(
                self.position,
                lib.bullet.player_bullet.bulletTexture2WayHyper,
                size=lib.bullet.player_bullet.bulletSize2Way, speed=10, angle=self.angle, damage=7,
                flags=lib.bullet.player_bullet.PlayerBulletFlags.BULLET_CANCELLING
            )
            if not self.slow:
                lib.bullet.player_bullet.PlayerBullet(
                    self.position,
                    lib.bullet.player_bullet.bulletTexture1WayHyper,
                    size=lib.bullet.player_bullet.bulletSize1Way, speed=12, angle=self.angle - 7, damage=3,
                    flags=lib.bullet.player_bullet.PlayerBulletFlags.BULLET_CANCELLING
                )
            self.shootWait = 6
        else:
            lib.bullet.player_bullet.PlayerBullet(
                self.position,
                lib.bullet.player_bullet.bulletTexture2Way,
                size=lib.bullet.player_bullet.bulletSize2Way, speed=8, angle=self.angle, damage=5
            )
            if not self.slow:
                lib.bullet.player_bullet.PlayerBullet(
                    self.position,
                    lib.bullet.player_bullet.bulletTexture1Way,
                    size=lib.bullet.player_bullet.bulletSize1Way, speed=10, angle=self.angle - 7, damage=3
                )
            self.shootWait = 10 if self.slow else 15
        lib.sound.sfx[random.choice(('PLAYER_SHOOT_A', 'PLAYER_SHOOT_B'))].play()

class OptionTypeB1(PlayerOption):
    def shoot(self) -> None:
        if lib.globals.groupPlayer.sprite.hyperRemain:
            lib.bullet.player_bullet.PlayerBullet(
                self.position,
                lib.bullet.player_bullet.bulletTexture2WayHyper,
                size=lib.bullet.player_bullet.bulletSize2Way, speed=10, angle=self.angle, damage=5
            )
            if not self.slow:
                lib.bullet.player_bullet.PlayerBullet(
                    self.position,
                    lib.bullet.player_bullet.bulletTexture1WayHyper,
                    size=lib.bullet.player_bullet.bulletSize1Way, speed=12, angle=self.angle + 7, damage=3
                )
            self.shootWait = 6
        else:
            lib.bullet.player_bullet.PlayerBullet(
                self.position,
                lib.bullet.player_bullet.bulletTexture2Way,
                size=lib.bullet.player_bullet.bulletSize2Way, speed=8, angle=self.angle, damage=7
            )
            if not self.slow:
                lib.bullet.player_bullet.PlayerBullet(
                    self.position,
                    lib.bullet.player_bullet.bulletTexture1Way,
                    size=lib.bullet.player_bullet.bulletSize1Way, speed=10, angle=self.angle + 7, damage=3
                )
            self.shootWait = 10 if self.slow else 15
        lib.sound.sfx[random.choice(('PLAYER_SHOOT_A', 'PLAYER_SHOOT_B'))].play()
