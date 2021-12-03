import pygame

import lib.bullet
import lib.constants
import lib.globals
import lib.sprite.enemy
import lib.sprite.player

def inputDisplay():
    for key, pos in (
        (pygame.K_LSHIFT, (10, 10, 45, 20)),
        (pygame.K_z, (10, 35, 20, 20)),
        (pygame.K_x, (35, 35, 20, 20)),
        (pygame.K_LEFT, (60, 35, 20, 20)),
        (pygame.K_DOWN, (85, 35, 20, 20)),
        (pygame.K_UP, (85, 10, 20, 20)),
        (pygame.K_RIGHT, (110, 35, 20, 20)),
    ):
        pygame.draw.rect(
            lib.globals.screen,
            lib.constants.DEBUG_INPUT_DISPLAY_PRESSED if lib.globals.keys[key] else lib.constants.DEBUG_INPUT_DISPLAY_NOTPRESSED,
            (500 + pos[0], 415 + pos[1], pos[2], pos[3])
        )

def hitboxDisplay():
    for g in (
        lib.globals.groupPlayerBullet,
        lib.globals.groupEnemyBullet,
    ):
        for s in g:
            s: lib.bullet.Bullet
            pygame.draw.circle(
                lib.globals.stgSurface,
                lib.constants.DEBUG_HITBOX,
                s.position,
                s.size,
                1
            )

    s: lib.sprite.player.Player = lib.globals.groupPlayer.sprite
    for h in s.hitboxAbsolute:
        pygame.draw.circle(
            lib.globals.stgSurface,
            lib.constants.DEBUG_HITBOX,
            h.offset,
            h.size,
            1
        )
        pygame.draw.circle(
            lib.globals.stgSurface,
            lib.constants.DEBUG_HITBOX,
            h.offset,
            h.size + lib.constants.GRAZE_RANGE,
            1
        )

    for s in lib.globals.groupEnemy:
        s: lib.sprite.enemy.Enemy
        for h in s.hitboxAbsolute:
            pygame.draw.circle(
                lib.globals.stgSurface,
                lib.constants.DEBUG_HITBOX,
                h.offset,
                h.size,
                1
            )
