import collections
import os
import pygame
import pygame.locals
import typing

import lib.constants

pygame.display.set_icon(pygame.image.load('assets/icon.webp'))
pygame.display.set_caption(lib.constants.TITLE)
screen = pygame.display.set_mode(
    (1280, 960),
    (pygame.locals.SCALED if os.environ.get('STRIKER_WINDOWED') else pygame.locals.FULLSCREEN)
)
clock = pygame.time.Clock()
keys: typing.Sequence[bool] = None
keysLastFrame: typing.Sequence[bool] = None

currentScene = None
nextScene = None

menuChoice = 0
menuSubChoice = 0

stgSurface = pygame.Surface((384, 448))
stgSurface2x = pygame.Surface((768, 896))
stageEngine = None

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
continueCount = 0
continueRemain = 0
continueEnabled = True
allCleared = False

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
stgGroups = (
    groupPlayer,
    groupPlayerOption,
    groupEnemy,
    groupPlayerBullet,
    groupEnemyBullet,
    groupParticle,
)
