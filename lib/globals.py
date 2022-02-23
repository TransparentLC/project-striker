import collections
import json
import os
import pygame
import typing

from jsonschema import Draft7Validator
from jsonschema import ValidationError
from jsonschema import validators

import lib.constants
import lib.utils

# https://python-jsonschema.readthedocs.io/en/stable/faq/#why-doesn-t-my-schema-s-default-property-set-the-default-on-my-instance
def extendValidatorWithDefault(validator_class: Draft7Validator) -> Draft7Validator:
    def setDefaults(validator, properties, instance, schema):
        for property, subschema in properties.items():
            if 'default' in subschema:
                instance.setdefault(property, subschema['default'])
        for error in validator_class.VALIDATORS['properties'](validator, properties, instance, schema):
            yield error
    return validators.extend(validator_class, {'properties': setDefaults})
Draft7ValidatorWithDefault = extendValidatorWithDefault(Draft7Validator)

if not os.path.exists(lib.constants.DATA_DIR):
    os.mkdir(lib.constants.DATA_DIR)
config: dict = None
if os.path.exists(lib.constants.PATH_CONFIG):
    with open(lib.constants.PATH_CONFIG, 'r', encoding='utf-8') as f:
        config = json.load(f)
try:
    Draft7ValidatorWithDefault(lib.constants.SCHEMA_CONFIG).validate(config)
except ValidationError:
    config = dict()
    Draft7ValidatorWithDefault(lib.constants.SCHEMA_CONFIG).validate(config)

savedata: tuple = None
if os.path.exists(lib.constants.PATH_SAVEDATA):
    with open(lib.constants.PATH_SAVEDATA, 'r', encoding='utf-8') as f:
        savedata = json.load(f)
try:
    Draft7ValidatorWithDefault(lib.constants.SCHEMA_SAVEDATA).validate(savedata)
except ValidationError:
    savedata = [
        {
            'highScore': lib.constants.DEFAULT_HIGHSCORE,
            'phaseHistory': [
                {
                    'bonus': 0,
                    'total': 0,
                } for y in range(len(lib.constants.PHASE_NAME))
            ],
        } for x in range(3)
    ]
    Draft7ValidatorWithDefault(lib.constants.SCHEMA_SAVEDATA).validate(savedata)

pygame.display.set_icon(pygame.image.load(lib.utils.getResourceHandler('assets/icon.webp')))
pygame.display.set_caption(lib.constants.TITLE)
screen = pygame.display.set_mode(
    (1280, 960),
    (pygame.SCALED if config['windowed'] else pygame.FULLSCREEN)
)
clock = pygame.time.Clock()
keys: typing.Sequence[bool] = None
keysLastFrame: typing.Sequence[bool] = None
currentScene = None
nextScene = None

stgSurface = pygame.Surface((384, 448))
stgSurface2x = pygame.Surface((768, 896))
stageEngine = None

backgroundScrollSpeed = 1.5
backgroundScrollOffset = 0
backgroundMaskAlpha = 0
backgroundMaskChangeSpeed = 0
# 只使用append和popleft作为队列使用
backgroundSurfaces: typing.Deque[pygame.Surface] = collections.deque()

score = 0
scoreLastFrame = 0
grazeCount = 0
maxGetPoint = 0
phaseIndex = 0
phaseBonus = 0
phaseBonusDrop = 0
phaseBonusCount = 0
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

groupItem = pygame.sprite.Group()
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
    groupItem,
    groupParticle,
)
