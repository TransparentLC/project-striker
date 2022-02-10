import pygame
import random

from . import Sprite
from . import Hitbox
from . import explosion

import lib.constants
import lib.globals
import lib.sound
import lib.utils
import lib.bullet.player_bullet

playerBoundary = pygame.Rect(13, 8, 384 - 2 * 13, 448 - 2 * 8)
playerInitialPosition = pygame.Vector2(192, 400)

class Player(Sprite):
    texturesIdle = tuple(pygame.image.load(lib.utils.getResourceHandler(f'assets/player-idle-{i}.webp')).convert_alpha() for i in range(2))
    texturesTurnL0 = tuple(pygame.image.load(lib.utils.getResourceHandler(f'assets/player-turn-l-0-{i}.webp')).convert_alpha() for i in range(2))
    texturesTurnL1 = tuple(pygame.image.load(lib.utils.getResourceHandler(f'assets/player-turn-l-1-{i}.webp')).convert_alpha() for i in range(2))
    texturesTurnR0 = tuple(pygame.image.load(lib.utils.getResourceHandler(f'assets/player-turn-r-0-{i}.webp')).convert_alpha() for i in range(2))
    texturesTurnR1 = tuple(pygame.image.load(lib.utils.getResourceHandler(f'assets/player-turn-r-1-{i}.webp')).convert_alpha() for i in range(2))

    turnCounter = 0
    invincibleRemain = 0
    hyperRemain = 0
    shootWait = 0
    deathWait = 0

    def __init__(self) -> None:
        super().__init__(lib.globals.groupPlayer)
        self.speed = pygame.Vector2(0, 0)
        self.boundary = playerBoundary
        self.position = pygame.Vector2(playerInitialPosition)
        self.hitbox = (Hitbox(pygame.Vector2(0, -3), 2),)
        self.options = []
        self.interval = 5

    @property
    def textures(self) -> tuple[pygame.Surface]:
        if self.turnCounter == 0:
            return self.texturesIdle
        elif self.turnCounter < -10:
            return self.texturesTurnL1
        elif self.turnCounter < 0:
            return self.texturesTurnL0
        elif self.turnCounter > 10:
            return self.texturesTurnR1
        elif self.turnCounter > 0:
            return self.texturesTurnR0

    def shoot(self) -> None:
        if self.hyperRemain:
            lib.bullet.player_bullet.PlayerBullet(
                self.position,
                lib.bullet.player_bullet.bulletTexture4WayHyper,
                size=lib.bullet.player_bullet.bulletSize4Way * 2, speed=16, angle=self.angle, damage=25,
                flags=lib.bullet.player_bullet.PlayerBulletFlags.BULLET_CANCELLING
            )
            self.shootWait = 6
        else:
            lib.bullet.player_bullet.PlayerBullet(
                self.position,
                lib.bullet.player_bullet.bulletTexture4Way,
                size=lib.bullet.player_bullet.bulletSize4Way, speed=12, angle=self.angle, damage=20
            )
            self.shootWait = 8
        lib.sound.sfx[random.choice(('PLAYER_SHOOT_A', 'PLAYER_SHOOT_B'))].play()

    def update(self) -> None:
        self.speed.update(0, 0)

        if self.deathWait:
            self.deathWait -= 1
            if not self.deathWait:
                if lib.globals.lifeNum:
                    lib.globals.lifeNum -= 1
                    lib.globals.hyperNum = lib.constants.INITIAL_HYPERNUM
                    lib.globals.maxGetPoint = max(10000, lib.globals.maxGetPoint * 4 // 5)
                    self.invincibleRemain = 150
                    self.position.update(playerInitialPosition)
                else:
                    if lib.globals.continueEnabled:
                        lib.sound.sfx['COUNTDOWN'].play()
                    lib.globals.continueRemain = 659
                    self.deathWait = 1

        if self.invincibleRemain:
            self.invincibleRemain -= 1

        if self.hyperRemain:
            self.hyperRemain -= 1
            lib.globals.phaseBonus = 0
            if not self.hyperRemain:
                lib.sound.sfx['HYPER_END'].play()
        if lib.globals.keys[pygame.K_x] and not lib.globals.keysLastFrame[pygame.K_x]:
            if self.hyperRemain:
                self.hyperRemain = 0
                self.invincibleRemain = 0
                lib.sound.sfx['HYPER_END'].play()
            elif lib.globals.hyperNum and not self.deathWait:
                lib.globals.hyperNum -= 1
                lib.globals.hyperUsedCount += 1
                self.hyperRemain = lib.constants.HYPER_TIME
                self.invincibleRemain = lib.constants.HYPER_INVINCIBLE_TIME
                for item in lib.globals.groupItem:
                    item.magnetNear = True
                lib.sound.sfx['HYPER_ACTIVATE'].play()

        if not self.deathWait:
            speed = lib.constants.PLAYER_SPEED_SLOW if lib.globals.keys[pygame.K_LSHIFT] else lib.constants.PLAYER_SPEED_NORMAL
            if lib.globals.keys[pygame.K_LEFT] and not lib.globals.keys[pygame.K_RIGHT]:
                self.speed -= pygame.Vector2(speed, 0)
                self.turnCounter = max(-10 if lib.globals.keys[pygame.K_LSHIFT] else -20, min(self.turnCounter, 0) - 1)
            elif lib.globals.keys[pygame.K_RIGHT] and not lib.globals.keys[pygame.K_LEFT]:
                self.speed += pygame.Vector2(speed, 0)
                self.turnCounter = min(10 if lib.globals.keys[pygame.K_LSHIFT] else 20, max(self.turnCounter, 0) + 1)
            else:
                if self.turnCounter > 0:
                    self.turnCounter -= 1
                elif self.turnCounter < 0:
                    self.turnCounter += 1
            if lib.globals.keys[pygame.K_UP] and not lib.globals.keys[pygame.K_DOWN]:
                self.speed -= pygame.Vector2(0, speed)
            elif lib.globals.keys[pygame.K_DOWN] and not lib.globals.keys[pygame.K_UP]:
                self.speed += pygame.Vector2(0, speed)
            if self.speed.x and self.speed.y:
                self.speed /= 2 ** .5

            if self.shootWait:
                self.shootWait -= 1
            if lib.globals.keys[pygame.K_z] and not self.shootWait:
                self.shoot()

        super().update()

        if self.invincibleRemain & 4:
            self.image.set_alpha(128)

        if self.deathWait:
            self.image.set_alpha(0)

        self.rect.centerx = self.position.x = lib.utils.clamp(self.position.x, self.boundary.left, self.boundary.right)
        self.rect.centery = self.position.y = lib.utils.clamp(self.position.y, self.boundary.top, self.boundary.bottom)

    def explode(self):
        if self.deathWait:
            return
        lib.sound.sfx['EXPLODE_PLAYER'].play()
        explosion.ExplosionPlayer(self.position)
        self.deathWait = 120
        self.hyperRemain = 0
        lib.globals.phaseBonus = 0
        lib.globals.missedCount += 1

Player()
