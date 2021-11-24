import pygame

import lib.font
import lib.globals

fontRenderer = lib.font.FontRenderer(lib.font.FONT_LARGE, (255, 255, 255))

def draw(surface: pygame.Surface):
    if not lib.globals.messageQueue:
        return
    message = lib.globals.messageQueue[0]
    rendered = fontRenderer.render(message[0])
    surface.blit(rendered, ((surface.get_width() - rendered.get_width()) / 2, 64))
    message[1] -= 1
    if not message[1]:
        lib.globals.messageQueue.popleft()
