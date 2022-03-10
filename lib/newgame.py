import pygame

import lib.constants
import lib.globals
import lib.sprite.option
import lib.stg_overlay
import lib.utils
import lib.scene.stg
import lib.script_engine.stage

def init():
    lib.globals.stgRandom.seed(lib.globals.stgRandomSeed, version=2)

    lib.globals.groupPlayer.sprite.position.update(192, 400)
    lib.globals.groupPlayer.sprite.invincibleRemain = 0
    lib.globals.groupPlayer.sprite.hyperRemain = 0
    lib.globals.groupPlayer.sprite.shootWait = 0
    lib.globals.groupPlayer.sprite.deathWait = 0
    lib.globals.score = 0
    lib.globals.scoreLastFrame = 0
    lib.globals.grazeCount = 0
    lib.globals.maxGetPoint = 10000
    lib.globals.lifeNum = lib.constants.INITIAL_LIFENUM
    lib.globals.hyperNum = lib.constants.INITIAL_HYPERNUM
    lib.globals.missedCount = 0
    lib.globals.hyperUsedCount = 0
    lib.globals.phaseIndex = 0
    lib.globals.phaseBonusCount = 0
    lib.globals.continueCount = 0
    lib.globals.continueRemain = 0
    lib.globals.continueEnabled = True
    lib.globals.allCleared = False
    lib.globals.backgroundScrollOffset = 0
    lib.globals.backgroundMaskAlpha = 0
    lib.globals.backgroundMaskChangeSpeed = 0
    for i in range(len(lib.stg_overlay.overlayStatus)):
        lib.stg_overlay.overlayStatus[i] = 0
    for g in (
        lib.globals.groupPlayerOption,
        lib.globals.groupPlayerBullet,
        lib.globals.groupEnemy,
        lib.globals.groupEnemyBullet,
        lib.globals.groupBoss,
        lib.globals.groupParticle,
        lib.globals.groupItem,
    ):
        g.empty()

    if lib.globals.optionType == 0:
        lib.globals.groupPlayer.sprite.options = (
            lib.sprite.option.OptionTypeA(8, pygame.Vector2(-30, 5), pygame.Vector2(-20, -5), 20, 10),
            lib.sprite.option.OptionTypeA(8, pygame.Vector2(30, 5), pygame.Vector2(20, -5), -20, -10),
            lib.sprite.option.OptionTypeA(8, pygame.Vector2(-15, 20), pygame.Vector2(-8, -20), 10, 5),
            lib.sprite.option.OptionTypeA(8, pygame.Vector2(15, 20), pygame.Vector2(8, -20), -10, -5),
        )
    elif lib.globals.optionType == 1:
        lib.globals.groupPlayer.sprite.options = (
            lib.sprite.option.OptionTypeB1(8, pygame.Vector2(-15, 20), pygame.Vector2(-25, 0), 12, 0),
            lib.sprite.option.OptionTypeB0(8, pygame.Vector2(15, 20), pygame.Vector2(25, 0), -12, 0),
            lib.sprite.option.OptionTypeB0(8, pygame.Vector2(-30, 5), pygame.Vector2(-45, 0), 30, 0),
            lib.sprite.option.OptionTypeB1(8, pygame.Vector2(30, 5), pygame.Vector2(45, 0), -30, 0),
        )
    elif lib.globals.optionType == 2:
        lib.globals.groupPlayer.sprite.options = (
            lib.sprite.option.OptionTypeC(8, pygame.Vector2(-25, 0), pygame.Vector2(-10, -15), 0, 0),
            lib.sprite.option.OptionTypeC(8, pygame.Vector2(25, 0), pygame.Vector2(10, -15), 0, 0),
        )

    with lib.utils.getResourceHandler('scriptfiles/stage/stage1.txt') as f:
        lib.globals.stageEngine = lib.script_engine.stage.Engine(f.read().decode('utf-8'))
    lib.globals.nextScene = lib.scene.stg
