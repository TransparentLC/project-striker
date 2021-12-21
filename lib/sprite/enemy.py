import random
import pygame
import typing

import lib.globals
import lib.script_engine.enemy
import lib.sprite
import lib.sprite.debris
import lib.sprite.explosion
import lib.sprite.player
import lib.sprite.item
import lib.utils

r = lib.globals.stgSurface.get_rect()
enemyBoundary = pygame.Rect(-30, -80, r.width + 60, r.height + 110)

class Enemy(lib.sprite.Sprite):
    hitpoint: int
    maxGetPointAdd: int
    invincibleRemain: int
    explosion: typing.Callable[[pygame.Vector2], lib.sprite.explosion.Explosion]
    debris: list[
        tuple[
            typing.Callable[[pygame.Vector2, float, float], lib.sprite.debris.Debris],
            pygame.Vector2,
            float, float, float, float,
        ]
    ]
    scriptEngine: lib.script_engine.enemy.Engine
    explodeSfx: pygame.mixer.Sound
    starNum: int

    def __init__(self) -> None:
        super().__init__(lib.globals.groupEnemy)
        self.interval = 5
        self.hitpoint = 1
        self.maxGetPointAdd = 0
        self.position = pygame.Vector2()
        self.speed = pygame.Vector2()
        self.boundary = enemyBoundary
        self.explosion = None
        self.hitbox = []
        self.debris = []
        self.invincibleRemain = 0
        self.scriptEngine = None
        self.explodeSfx = None
        self.pointItemNum = 0

    def setScript(self, script: str) -> None:
        self.scriptEngine = lib.script_engine.enemy.Engine(self, script)

    def update(self) -> None:
        if self.invincibleRemain:
            self.invincibleRemain -= 1
        if self.hitpoint <= 0:
            if self.explosion:
                self.explosion(self.position)
            for d in self.debris:
                d[0](
                    self.position + d[1].rotate(-self.angle),
                    lib.utils.linearInterpolation(random.random(), d[2], d[3]),
                    lib.utils.linearInterpolation(random.random(), d[4], d[5]),
                )
            if self.scriptEngine and self.scriptEngine.pointerDeath:
                self.scriptEngine.pointer = self.scriptEngine.pointerDeath
                self.scriptEngine.wait = 0
                self.scriptEngine.update()
            if self.explodeSfx:
                self.explodeSfx.play()

            minwh = min(self.rect.width, self.rect.height)
            for i in range(self.pointItemNum):
                pos = pygame.Vector2(random.random() * minwh, 0)
                pos.rotate_ip(random.random() * 360)
                pos += self.position
                lib.sprite.item.Point(pos)
            lib.globals.maxGetPoint += self.maxGetPointAdd
            self.kill()
            return
        if self.outOfBoundary:
            self.kill()

        s: lib.sprite.player.Player = lib.globals.groupPlayer.sprite
        if not s.invincibleRemain:
            for h in self.hitboxAbsolute:
                for g in s.hitboxAbsolute:
                    if (h.offset - g.offset).length() < h.size + g.size:
                        s.explode()

        if self.scriptEngine:
            if self.scriptEngine.pointerRangeBreak and self.hitpoint < lib.globals.bossHitpointRangeMin:
                self.scriptEngine.pointer = self.scriptEngine.pointerRangeBreak
                self.scriptEngine.pointerRangeBreak = None
                self.scriptEngine.wait = 0
            self.scriptEngine.update()

        super().update()
