import os
import json
import sys
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)
else:
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

import pygame
import pygame.locals
pygame.init()

import lib.constants
import lib.sound
import lib.utils
import lib.globals
import lib.debug
import lib.scene.title

if __name__ == '__main__':
    # Hide cursor
    pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
    lib.sound.playBgm('TITLE')

    lib.globals.nextScene = lib.scene.title
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
            lib.globals.currentScene = lib.globals.nextScene
            lib.globals.currentScene.update()
            lib.globals.currentScene.draw(lib.globals.screen)

            if lib.globals.config['inputDisplay']:
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
                        (1140 + pos[0], 895 + pos[1], pos[2], pos[3])
                    )

            pygame.display.flip()
            pygame.display.set_caption(f'{lib.constants.TITLE} (FPS: {lib.globals.clock.get_fps():.02f})')

        lib.globals.clock.tick(60)

    # Write config before quit
    with open(f'{lib.constants.DATA_DIR}/config.json', 'w', encoding='utf-8') as f:
        json.dump(lib.globals.config, f, separators=(',', ':'))

    pygame.quit()
