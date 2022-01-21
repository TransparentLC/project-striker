import os
import pygame

import lib.constants
import lib.debug
import lib.font
import lib.globals
import lib.scene.result
import lib.scene.title
import lib.scroll_map
import lib.sound
import lib.stg_overlay
import lib.sprite.player
import lib.utils

background = pygame.image.load(lib.utils.getResourceHandler('assets/ui-stg-background.webp')).convert()

def update():
    player: lib.sprite.player.Player = lib.globals.groupPlayer.sprite

    if not lib.globals.continueRemain:
        lib.globals.scoreLastFrame = lib.globals.score

        lib.globals.stageEngine.update()
        lib.globals.backgroundScrollOffset += lib.globals.backgroundScrollSpeed

        if os.environ.get('STRIKER_DEBUG_PLAYER_INVINCIBLE'):
            player.invincibleRemain = player.frameCounter

        for g in lib.globals.stgGroups:
            g.update()

        if lib.globals.groupBoss.sprite:
            lib.globals.maxGetPoint = max(10000, lib.globals.maxGetPoint - 2)

        if not lib.globals.continueCount:
            for extendLimit in (
                5000000,
                15000000,
                30000000,
                50000000,
            ):
                if (
                    lib.globals.scoreLastFrame < extendLimit and
                    extendLimit <= lib.globals.score and
                    lib.globals.lifeNum < 8
                ):
                    lib.globals.lifeNum += 1
                    lib.stg_overlay.overlayStatus[lib.stg_overlay.OverLayStatusIndex.LIFE_REMAIN] = 240
                    lib.sound.sfx['EXTEND_LIFE'].play()

    if lib.globals.continueRemain:
        if lib.globals.continueEnabled:
            if lib.globals.keys[pygame.K_z] and not lib.globals.keysLastFrame[pygame.K_z]:
                lib.sound.sfx['HYPER_ACTIVATE'].play()
                lib.globals.continueCount += 1
                lib.globals.continueRemain = 0
                lib.globals.lifeNum = lib.constants.INITIAL_LIFENUM + 1
            else:
                if lib.globals.continueRemain % 60 == 0:
                    lib.sound.sfx['COUNTDOWN'].play()
                if lib.globals.keys[pygame.K_x] and not lib.globals.keysLastFrame[pygame.K_x]:
                    lib.globals.continueRemain -= 60
                    if lib.globals.continueRemain < 0:
                        lib.globals.continueRemain = 0
                    lib.sound.sfx['COUNTDOWN'].play()
                else:
                    lib.globals.continueRemain -= 1
                if not lib.globals.continueRemain:
                    lib.sound.sfx['HYPER_END'].play()
                    pygame.mixer.music.stop()
                    lib.globals.nextScene = lib.scene.result
        else:
            lib.sound.sfx['HYPER_END'].play()
            pygame.mixer.music.stop()
            lib.globals.nextScene = lib.scene.result

    if lib.globals.keys[pygame.K_ESCAPE]:
        lib.sound.playBgm('TITLE')
        lib.globals.nextScene = lib.scene.title

def draw(surface: pygame.Surface):
    surface.blit(background, (0, 0))
    lib.scroll_map.blitBackground(lib.globals.stgSurface)
    # lib.globals.stgSurface.fill((255, 0, 255))

    for g in lib.globals.stgGroups:
        g.draw(lib.globals.stgSurface)

    if os.environ.get('STRIKER_DEBUG_HITBOX_DISPLAY'):
        lib.debug.hitboxDisplay()

    if lib.globals.config['scale2x']:
        pygame.transform.scale2x(lib.globals.stgSurface, lib.globals.stgSurface2x)
    else:
        pygame.transform.scale(lib.globals.stgSurface, (768, 896), lib.globals.stgSurface2x)

    lib.stg_overlay.update()
    lib.stg_overlay.draw(lib.globals.stgSurface2x)

    surface.blit(lib.globals.stgSurface2x, (32, 32))

    for text, (posX, posY) in (
        (f'Continue×{lib.globals.continueCount}' if lib.globals.continueCount else str(lib.globals.score), (1248, 76)),
        (str(lib.globals.maxGetPoint), (1248, 316)),
        (str(lib.globals.grazeCount), (1248, 376)),
        (str(len(lib.globals.groupEnemyBullet)), (1248, 466)),
        (
            '★{0}  {1}/{2}'.format(
                lib.globals.bossRemain,
                lib.utils.clamp(
                    lib.globals.groupBoss.sprite.hitpoint - lib.globals.bossHitpointRangeMin,
                    0,
                    lib.globals.bossHitpointRangeMax - lib.globals.bossHitpointRangeMin
                ),
                lib.globals.bossHitpointRangeMax - lib.globals.bossHitpointRangeMin
            )
            if lib.globals.groupBoss.sprite else '???',
            (1248, 582)
        ),
    ):
        renderedSurface = lib.font.FONT_LARGE.render(text, True, (255, 255, 255))
        surface.blit(renderedSurface, (posX - renderedSurface.get_width(), posY - renderedSurface.get_height() // 2))
    for text, (posX, posY) in (
        ('★' * lib.globals.lifeNum, (1000, 166)),
        (
            (
                lib.utils.frameToSeconds(lib.globals.groupPlayer.sprite.hyperRemain)
                if lib.globals.groupPlayer.sprite.hyperRemain
                else '★' * lib.globals.hyperNum
            ),
            (1000, 226)
        ),
    ):
        renderedSurface = lib.font.FONT_LARGE.render(text, True, (255, 255, 255))
        surface.blit(renderedSurface, (posX, posY - renderedSurface.get_height() // 2))
    pygame.draw.rect(
        surface,
        (255, 255, 255),
        (836, 504, lib.utils.clamp(len(lib.globals.groupEnemyBullet), 0, 256) / 256 * 408, 24),
    )
    if lib.globals.groupBoss.sprite:
        pygame.draw.rect(
            surface,
            (255, 255, 255),
            (
                836, 620,
                lib.utils.clamp(
                    lib.globals.groupBoss.sprite.hitpoint - lib.globals.bossHitpointRangeMin,
                    0, lib.globals.bossHitpointRangeMax - lib.globals.bossHitpointRangeMin
                ) / (lib.globals.bossHitpointRangeMax - lib.globals.bossHitpointRangeMin) * 408,
                24
            ),
        )
