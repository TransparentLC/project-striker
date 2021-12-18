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

            if os.environ.get('STRIKER_DEBUG_INPUT_DISPLAY'):
                lib.debug.inputDisplay()

            pygame.display.flip()
            pygame.display.set_caption(f'{lib.constants.TITLE} (FPS: {lib.globals.clock.get_fps():.02f})')


        lib.globals.clock.tick(60)
    pygame.quit()
