import os
import pygame

import lib.constants
import lib.debug
import lib.font
import lib.globals
import lib.replay
import lib.scene.replay
import lib.scene.result
import lib.scene.title
import lib.scroll_map
import lib.sound
import lib.stg_overlay
import lib.sprite.player
import lib.utils

background = pygame.image.load(lib.utils.getResourceHandler('assets/ui-stg-background.webp')).convert()
enemyMarker = pygame.image.load(lib.utils.getResourceHandler('assets/enemy-marker.webp')).convert_alpha()
replayPlayingHint = lib.font.FONT_LARGE.render('REPLAY播放中', True, (255, 255, 255))

def update():
    player: lib.sprite.player.Player = lib.globals.groupPlayer.sprite

    if not lib.globals.continueRemain:
        if lib.globals.replayRecording:
            lib.globals.replayKeyStream.write(bytes([lib.replay.readKeys()]))
        else:
            lib.replay.setKeys(lib.globals.replayKeyStream.read(1)[0] or 0)
        lib.globals.scoreLastFrame = lib.globals.score

        lib.globals.stageEngine.update()
        lib.globals.backgroundScrollOffset += lib.globals.backgroundScrollSpeed

        if os.environ.get('STRIKER_DEBUG_PLAYER_INVINCIBLE'):
            player.invincibleRemain = player.frameCounter

        for g in lib.globals.stgGroups:
            g.update()

        if lib.globals.groupBoss.sprite:
            lib.globals.maxGetPoint = max(10000, lib.globals.maxGetPoint - 2)
        lib.globals.phaseBonus = max(0, lib.globals.phaseBonus - lib.globals.phaseBonusDrop)

        scoreDiff = lib.globals.score - lib.globals.scoreDisplay
        lib.globals.scoreDisplay += scoreDiff if scoreDiff < 128 else max(128, scoreDiff // 8)

        if not lib.globals.continueCount:
            if lib.globals.replayRecording and lib.globals.savedata[lib.globals.optionType]['highScore'] < lib.globals.score:
                lib.globals.savedata[lib.globals.optionType]['highScore'] = lib.globals.score

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
        if lib.globals.replayRecording and lib.globals.continueEnabled:
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
                    lib.replay.stopRecording()
                    lib.globals.nextScene = lib.scene.result
        else:
            lib.sound.sfx['HYPER_END'].play()
            if lib.globals.replayRecording:
                pygame.mixer.music.stop()
                lib.replay.stopRecording()
                lib.globals.nextScene = lib.scene.result
            else:
                lib.sound.playBgm('TITLE')
                lib.globals.nextScene = lib.scene.replay

    if lib.globals.keys[pygame.K_ESCAPE]:
        lib.sound.playBgm('TITLE')
        lib.replay.stopRecording()
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
        (str(
            lib.globals.savedata[lib.globals.optionType]['highScore']
            if lib.globals.savedata[lib.globals.optionType]['highScore'] != lib.globals.score else
            lib.globals.scoreDisplay
        ), (1248, 76)),
        (f'Continue×{lib.globals.continueCount}' if lib.globals.continueCount else str(lib.globals.scoreDisplay), (1248, 136)),
        (str(lib.globals.maxGetPoint), (1248, 376)),
        (str(lib.globals.grazeCount), (1248, 436)),
        (str(len(lib.globals.groupEnemyBullet)), (1248, 526)),
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
            (1248, 642)
        ),
    ):
        renderedSurface = lib.font.FONT_LARGE.render(text, True, (255, 255, 255))
        surface.blit(renderedSurface, (posX - renderedSurface.get_width(), posY - renderedSurface.get_height() // 2))
    for text, (posX, posY) in (
        ('★' * lib.globals.lifeNum, (1000, 226)),
        (
            (
                lib.utils.frameToSeconds(lib.globals.groupPlayer.sprite.hyperRemain)
                if lib.globals.groupPlayer.sprite.hyperRemain
                else '★' * lib.globals.hyperNum
            ),
            (1000, 286)
        ),
    ):
        renderedSurface = lib.font.FONT_LARGE.render(text, True, (255, 255, 255))
        surface.blit(renderedSurface, (posX, posY - renderedSurface.get_height() // 2))
    pygame.draw.rect(
        surface,
        (255, 255, 255),
        (836, 564, lib.utils.clamp(len(lib.globals.groupEnemyBullet), 0, 256) / 256 * 408, 24),
    )
    if lib.globals.groupBoss.sprite:
        pygame.draw.rect(
            surface,
            (255, 255, 255),
            (
                836, 680,
                lib.utils.clamp(
                    lib.globals.groupBoss.sprite.hitpoint - lib.globals.bossHitpointRangeMin,
                    0, lib.globals.bossHitpointRangeMax - lib.globals.bossHitpointRangeMin
                ) / (lib.globals.bossHitpointRangeMax - lib.globals.bossHitpointRangeMin) * 408,
                24
            ),
        )
        surface.blit(
            enemyMarker,
            (round(lib.globals.groupBoss.sprite.position.x * 2 - enemyMarker.get_width() / 2) + 32, 932)
        )
    if not lib.globals.replayRecording:
        surface.blit(replayPlayingHint, (1040 - replayPlayingHint.get_width() // 2, 820 - replayPlayingHint.get_height() // 2))
