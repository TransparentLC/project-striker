import pygame
import random

from . import Sprite
from . import Hitbox
from . import explosion
from .. import constants
from .. import globals
from .. import scene
from .. import sound
from .. import utils

from ..bullet import player_bullet

r = globals.stgSurface.get_rect()
playerBoundary = pygame.Rect(13, 8, r.width - 2 * 13, r.height - 2 * 8)
playerInitialPosition = pygame.Vector2(192, 400)

class Player(Sprite):
    texturesIdle = tuple(pygame.image.load(f'assets/player-idle-{i}.png').convert_alpha() for i in range(2))
    texturesTurnL0 = tuple(pygame.image.load(f'assets/player-turn-l-0-{i}.png').convert_alpha() for i in range(2))
    texturesTurnL1 = tuple(pygame.image.load(f'assets/player-turn-l-1-{i}.png').convert_alpha() for i in range(2))
    texturesTurnR0 = tuple(pygame.image.load(f'assets/player-turn-r-0-{i}.png').convert_alpha() for i in range(2))
    texturesTurnR1 = tuple(pygame.image.load(f'assets/player-turn-r-1-{i}.png').convert_alpha() for i in range(2))

    turnCounter = 0
    invincibleRemain = 0
    hyperRemain = 0
    shootWait = 0
    deathWait = 0

    def __init__(self) -> None:
        super().__init__(globals.groupPlayer)
        self.speed = pygame.Vector2(0, 0)
        self.boundary = playerBoundary
        self.position = pygame.Vector2(playerInitialPosition)
        self.hitbox = (
            Hitbox(pygame.Vector2(0, 0), 3),
        )
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
            player_bullet.PlayerBullet(
                self.position,
                player_bullet.bulletTexture4WayHyper,
                size=player_bullet.bulletSize4Way, speed=16, angle=self.angle, damage=25,
                flags=player_bullet.PlayerBulletFlags.BULLET_CANCELLING
            )
            self.shootWait = 6
        else:
            player_bullet.PlayerBullet(
                self.position,
                player_bullet.bulletTexture4Way,
                size=player_bullet.bulletSize4Way, speed=12, angle=self.angle, damage=20
            )
            self.shootWait = 8
        sound.sfx[random.choice(('PLAYER_SHOOT_A', 'PLAYER_SHOOT_B'))].play()

    def update(self) -> None:
        self.speed.update(0, 0)

        if self.deathWait:
            self.deathWait -= 1
            if not self.deathWait:
                if globals.lifeNum:
                    globals.lifeNum -= 1
                    globals.hyperNum = constants.INITIAL_HYPERNUM
                    self.invincibleRemain = 150
                    self.position.update(playerInitialPosition)
                else:
                    pygame.mixer.music.stop()
                    globals.currentScene = scene.Scene.RESULT
                    self.deathWait = 1

        if self.invincibleRemain:
            self.invincibleRemain -= 1

        if self.hyperRemain:
            self.hyperRemain -= 1
            if not self.hyperRemain:
                sound.sfx['HYPER_END'].play()
        elif globals.keys[pygame.K_x] and globals.hyperNum and not self.deathWait:
            globals.hyperNum -= 1
            globals.hyperUsedCount += 1
            self.hyperRemain = constants.HYPER_TIME
            self.invincibleRemain = constants.HYPER_INVINCIBLE_TIME
            sound.sfx['HYPER_ACTIVATE'].play()

        if not self.deathWait:
            speed = constants.PLAYER_SPEED_SLOW if globals.keys[pygame.K_LSHIFT] else constants.PLAYER_SPEED_NORMAL
            if globals.keys[pygame.K_LEFT] and not globals.keys[pygame.K_RIGHT]:
                self.speed -= pygame.Vector2(speed, 0)
                self.turnCounter = max(-10 if globals.keys[pygame.K_LSHIFT] else -20, min(self.turnCounter, 0) - 1)
            elif globals.keys[pygame.K_RIGHT] and not globals.keys[pygame.K_LEFT]:
                self.speed += pygame.Vector2(speed, 0)
                self.turnCounter = min(10 if globals.keys[pygame.K_LSHIFT] else 20, max(self.turnCounter, 0) + 1)
            else:
                if self.turnCounter > 0:
                    self.turnCounter -= 1
                elif self.turnCounter < 0:
                    self.turnCounter += 1
            if globals.keys[pygame.K_UP] and not globals.keys[pygame.K_DOWN]:
                self.speed -= pygame.Vector2(0, speed)
            elif globals.keys[pygame.K_DOWN] and not globals.keys[pygame.K_UP]:
                self.speed += pygame.Vector2(0, speed)
            if self.speed.x and self.speed.y:
                self.speed /= 2 ** .5

            if self.shootWait:
                self.shootWait -= 1
            if globals.keys[pygame.K_z] and not self.shootWait:
                self.shoot()

        super().update()

        if self.invincibleRemain & 4:
            self.image.set_alpha(128)

        if self.deathWait:
            self.image.set_alpha(0)

        self.rect.centerx = self.position.x = utils.clamp(self.position.x, self.boundary.left, self.boundary.right)
        self.rect.centery = self.position.y = utils.clamp(self.position.y, self.boundary.top, self.boundary.bottom)

    def explode(self):
        if self.deathWait:
            return
        sound.sfx['EXPLODE_PLAYER'].play()
        explosion.ExplosionPlayer(self.position)
        self.deathWait = 180
        self.hyperRemain = 0
        globals.missedCount += 1
