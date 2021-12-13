import os
import sys
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)
else:
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

import pygame
import pygame.locals
pygame.init()

import lib.constants
import lib.debug
import lib.font
import lib.globals
import lib.message
import lib.scene
import lib.sound
import lib.sprite
import lib.bullet.enemy_bullet
import lib.sprite.debris
import lib.sprite.enemy
import lib.sprite.explosion
import lib.sprite.player
import lib.script_engine.stage
import lib.scroll_map
import lib.title_screen
import lib.result_screen
import lib.utils

if __name__ == '__main__':
    lib.sound.playBgm('TITLE')

    player = lib.sprite.player.Player()
    loop = True
    freeze = False
    while loop:
        lib.globals.keysLastFrame = lib.globals.keys
        lib.globals.keys = pygame.key.get_pressed()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                loop = False

        if lib.globals.keys[pygame.K_p] and not lib.globals.keysLastFrame[pygame.K_p]:
            freeze = not freeze
            lib.sound.sfx['PAUSE'].play()
            if freeze:
                pygame.mixer.music.pause()
                pygame.display.set_caption(f'{lib.constants.TITLE} (Paused)')
            else:
                pygame.mixer.music.unpause()

        if not freeze:
            if lib.globals.currentScene == lib.scene.Scene.TITLE:
                lib.title_screen.update()
                lib.title_screen.draw(lib.globals.screen)
            elif lib.globals.currentScene == lib.scene.Scene.RESULT:
                lib.result_screen.update()
                lib.result_screen.draw(lib.globals.screen)
            elif lib.globals.currentScene == lib.scene.Scene.STG:
                lib.globals.screen.blit(lib.scene.BACKGROUND_STG, (0, 0))
                lib.scroll_map.blitBackground(lib.globals.stgSurface)
                # lib.globals.stgSurface.fill((255, 0, 255))
                lib.globals.scoreLastFrame = lib.globals.score

                lib.globals.stageEngine.update()
                lib.globals.backgroundScrollOffset += lib.globals.backgroundScrollSpeed

                if os.environ.get('STRIKER_DEBUG_PLAYER_INVINCIBLE'):
                    player.invincibleRemain = player.frameCounter

                for g in (
                    lib.globals.groupPlayer,
                    lib.globals.groupPlayerOption,
                    lib.globals.groupEnemy,
                    lib.globals.groupPlayerBullet,
                    lib.globals.groupEnemyBullet,
                    lib.globals.groupParticle,
                ):
                    g.update()
                    g.draw(lib.globals.stgSurface)

                for extendLimit in (
                    200000,
                    500000,
                    1000000,
                ):
                    if (
                        lib.globals.scoreLastFrame < extendLimit and
                        extendLimit <= lib.globals.score and
                        lib.globals.lifeNum < 8
                    ):
                        lib.globals.lifeNum += 1
                        lib.globals.messageQueue.append(['Life Extend!', 180])
                        lib.sound.sfx['EXTEND_LIFE'].play()

                if os.environ.get('STRIKER_DEBUG_HITBOX_DISPLAY'):
                    lib.debug.hitboxDisplay()

                if os.environ.get('STRIKER_STG_SCALE2X'):
                    pygame.transform.scale2x(lib.globals.stgSurface, lib.globals.stgSurface2x)
                else:
                    pygame.transform.scale(lib.globals.stgSurface, (768, 896), lib.globals.stgSurface2x)
                lib.message.draw(lib.globals.stgSurface2x)
                lib.globals.screen.blit(lib.globals.stgSurface2x, (32, 32))

                for text, (posX, posY) in (
                    (str(lib.globals.score), (1248, 76)),
                    (str(lib.globals.grazeCount), (1248, 309)),
                    (str(len(lib.globals.groupEnemyBullet)), (1248, 412)),
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
                        (1248, 528)
                    ),
                ):
                    renderedSurface = lib.font.FONT_LARGE.render(text, True, (255, 255, 255))
                    lib.globals.screen.blit(renderedSurface, (posX - renderedSurface.get_width(), posY - renderedSurface.get_height() // 2))
                for text, (posX, posY) in (
                    ('★' * lib.globals.lifeNum, (1000, 188)),
                    (
                        (
                            lib.utils.frameToSeconds(lib.globals.groupPlayer.sprite.hyperRemain)
                            if lib.globals.groupPlayer.sprite.hyperRemain
                            else '★' * lib.globals.hyperNum
                        ),
                        (1000, 248)
                    ),
                ):
                    renderedSurface = lib.font.FONT_LARGE.render(text, True, (255, 255, 255))
                    lib.globals.screen.blit(renderedSurface, (posX, posY - renderedSurface.get_height() // 2))
                pygame.draw.rect(
                    lib.globals.screen,
                    (255, 255, 255),
                    (836, 450, lib.utils.clamp(len(lib.globals.groupEnemyBullet), 0, 256) / 256 * 408, 24),
                )
                if lib.globals.groupBoss.sprite:
                    pygame.draw.rect(
                        lib.globals.screen,
                        (255, 255, 255),
                        (
                            836, 566,
                            lib.utils.clamp(
                                lib.globals.groupBoss.sprite.hitpoint - lib.globals.bossHitpointRangeMin,
                                0, lib.globals.bossHitpointRangeMax - lib.globals.bossHitpointRangeMin
                            ) / (lib.globals.bossHitpointRangeMax - lib.globals.bossHitpointRangeMin) * 408,
                            24
                        ),
                    )

                if lib.globals.keys[pygame.K_ESCAPE]:
                    lib.sound.playBgm('TITLE')
                    lib.globals.currentScene = lib.scene.Scene.TITLE

            if os.environ.get('STRIKER_DEBUG_INPUT_DISPLAY'):
                lib.debug.inputDisplay()

            pygame.display.flip()
            pygame.display.set_caption(f'{lib.constants.TITLE} (FPS: {lib.globals.clock.get_fps():.02f})')

        lib.globals.clock.tick(60)
    pygame.quit()
