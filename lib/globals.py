import collections
import pygame
import pygame.locals
import typing

import lib.constants
import lib.script_engine.stage
import lib.scene

pygame.display.set_icon(pygame.image.load('assets/icon.png'))
pygame.display.set_caption(lib.constants.TITLE)
screen = pygame.display.set_mode((640, 480), pygame.locals.HWSURFACE | pygame.locals.DOUBLEBUF | pygame.locals.SCALED)
# screen = pygame.display.set_mode((640, 480), pygame.locals.HWSURFACE | pygame.locals.DOUBLEBUF)
clock = pygame.time.Clock()
keys: typing.Sequence[bool] = None
keysLastFrame: typing.Sequence[bool] = None
currentScene = lib.scene.Scene.TITLE

menuChoice = 0
menuSubChoice = 0

stgSurface = pygame.Surface((384, 448), pygame.locals.HWSURFACE)
stageEngine: lib.script_engine.stage.Engine = None

backgroundScrollSpeed = 1.5
backgroundScrollOffset = 0
# 只使用append和popleft作为队列使用
backgroundSurfaces: typing.Deque[pygame.Surface] = collections.deque()

score = 0
scoreLastFrame = 0
grazeCount = 0
lifeNum = 0
hyperNum = 0
optionType = 0
missedCount = 0
hyperUsedCount = 0
allCleared = False

messageQueue: typing.Deque[tuple[str, int]] = collections.deque()

bossRemain = 0
bossHitpointRangeMin = 0
bossHitpointRangeMax = 0

groupPlayer = pygame.sprite.GroupSingle()
groupPlayerOption = pygame.sprite.Group()
groupPlayerBullet = pygame.sprite.Group()
groupEnemy = pygame.sprite.Group()
groupEnemyBullet = pygame.sprite.Group()
groupBoss = pygame.sprite.GroupSingle()
groupParticle = pygame.sprite.Group()
