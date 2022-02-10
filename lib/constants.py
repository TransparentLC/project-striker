import json
import os
import pathlib
import pygame

import lib.utils

if os.path.exists('build-info.txt'):
    with open('build-info.txt', 'r', encoding='utf-8') as f:
        BUILD_INFO = f.read().splitlines()
else:
    BUILD_INFO = None

with lib.utils.getResourceHandler('scriptfiles/phase-name.txt') as f:
    PHASE_NAME = f.read().decode('utf-8').splitlines()

TITLE = 'Striker'
DATA_DIR = f'{pathlib.Path.home()}/.striker'
PATH_CONFIG = f'{DATA_DIR}/config.json'
PATH_SAVEDATA = f'{DATA_DIR}/savedata.json'

SCHEMA_CONFIG = json.loads('''
    {
        "type": "object",
        "properties": {
            "windowed": {
                "type": "boolean",
                "default": false
            },
            "bgm": {
                "type": "boolean",
                "default": true
            },
            "scale2x": {
                "type": "boolean",
                "default": false
            },
            "inputDisplay": {
                "type": "boolean",
                "default": false
            }
        }
    }
''')
SCHEMA_SAVEDATA = json.loads('''
    {
        "type": "array",
        "default": null,
        "minItems": 3,
        "maxItems": 3,
        "items": {
            "type": "object",
            "properties": {
                "highScore": {
                    "type": "integer",
                    "default": "5000000",
                    "minimum": 0
                },
                "phaseHistory": {
                    "type": "array",
                    "minItems": null,
                    "maxItems": null,
                    "items": {
                        "type": "object",
                        "properties": {
                            "bonus": {
                                "type": "integer",
                                "default": "0",
                                "minimum": 0
                            },
                            "total": {
                                "type": "integer",
                                "default": "0",
                                "minimum": 0
                            }
                        }
                    }
                }
            }
        }
    }
''')
SCHEMA_SAVEDATA['items']['properties']['phaseHistory']['minItems'] = len(PHASE_NAME)
SCHEMA_SAVEDATA['items']['properties']['phaseHistory']['maxItems'] = len(PHASE_NAME)

DEFAULT_HIGHSCORE = 5000000

OPTION_TYPE_NAME = (
    'Type-A 诱导攻击型',
    'Type-B 广范围型',
    'Type-C 前方集中型',
)

DEBUG_INPUT_DISPLAY_PRESSED = pygame.Color(255, 255, 0)
DEBUG_INPUT_DISPLAY_NOTPRESSED = pygame.Color(127, 127, 127)
DEBUG_HITBOX = pygame.Color(255, 255, 0)

PLAYER_SPEED_NORMAL = 4
PLAYER_SPEED_SLOW = 1.8

HOMING_ANGLE_RANGE = 2
BULLET_CANCELLING_INITIAL_REMAIN = 2

ITEM_GAIN_RANGE = 5
ITEM_MAGNET_RANGE = 50
ITEM_GET_BORDER = 112
GRAZE_RANGE = 20
HYPER_TIME = 480
HYPER_INVINCIBLE_TIME = 180

INITIAL_LIFENUM = 2
INITIAL_HYPERNUM = 3
