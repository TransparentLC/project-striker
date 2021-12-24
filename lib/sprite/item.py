import pygame

import lib.constants
import lib.globals
import lib.sound
import lib.sprite
import lib.sprite.player
import lib.stg_overlay
import lib.utils

itemSurface = pygame.image.load('assets/item.webp').convert_alpha()
itemNumber = tuple(itemSurface.subsurface((6 * x, 0, 6, 8)) for x in range(10))
itemNumberHighlight = tuple(itemSurface.subsurface((6 * x, 8, 6, 8)) for x in range(10))
itemImage = tuple(itemSurface.subsurface((16 * x, 16, 16, 16)) for x in range(5))
itemEffectLifeExtend = itemSurface.subsurface((64, 0, 16, 8))
itemEffectHyperExtend = itemSurface.subsurface((64, 8, 16, 8))
itemBoundary = pygame.Rect(-20, -20, 384 + 20, 448 + 20)

class ItemEffect(pygame.sprite.Sprite):
    def __init__(self, position: pygame.Vector2, image: pygame.Surface) -> None:
        super().__init__(lib.globals.groupParticle)
        self.image = image
        self.rect = image.get_rect()
        self.rect.center = position
        self.frameCounter = 0

    def update(self) -> None:
        self.frameCounter += 1
        self.rect.centery -= .025
        self.image.set_alpha((60 - self.frameCounter) / 60 * 255)
        if self.frameCounter > 60:
            self.kill()

class Item(lib.sprite.Sprite):
    def __init__(self, position: pygame.Vector2, texture: pygame.Surface) -> None:
        super().__init__(lib.globals.groupItem)
        self.position = pygame.Vector2(position)
        self.speed = pygame.Vector2(0, -.75)
        self.textures = (texture,)
        self.magnet = False
        self.image = lib.sprite.EmptyTexture
        self.rect = lib.sprite.EmptyTextureRect
        self.boundary = itemBoundary

    def gain(self):
        pass

    def update(self) -> None:
        super().update()

        if self.outOfBoundary:
            self.kill()

        s: lib.sprite.player.Player = lib.globals.groupPlayer.sprite
        if s.deathWait and self.magnet:
            self.magnet = False
            self.speed.update(0, 0)
        self.speed.y += .015
        if not s.deathWait:
            if s.position.y < lib.constants.ITEM_GET_BORDER:
                self.magnet = True

            distance = (s.position - self.position).length()
            if distance < lib.constants.ITEM_GAIN_RANGE:
                self.gain()
                self.kill()
                return
            elif distance < lib.constants.ITEM_MAGNET_RANGE:
                self.magnet = True

            if self.magnet:
                delta = s.position - self.position
                if delta.length_squared() >= 36:
                    delta.normalize_ip()
                    delta *= 6
                delta.y -= .02
                self.speed.update(delta)

class Point(Item):
    def __init__(self, position: pygame.Vector2) -> None:
        super().__init__(position, itemImage[4])

    def gain(self):
        # 25%-60% 100%
        if self.position.y < lib.constants.ITEM_GET_BORDER:
            point = lib.globals.maxGetPoint
            number = itemNumberHighlight
        else:
            point = int(lib.utils.linearInterpolation((self.position.y - lib.constants.ITEM_GET_BORDER) / (448 - lib.constants.ITEM_GET_BORDER), .6, .25) * lib.globals.maxGetPoint)
            number = itemNumber

        lib.globals.score += point
        ItemEffect(self.position, lib.utils.renderBitmapNumber(point, number))
        lib.sound.sfx['GET_POINT'].play()

class LifeExtend(Item):
    def __init__(self, position: pygame.Vector2) -> None:
        super().__init__(position, itemImage[2])

    def gain(self):
        if lib.globals.lifeNum < 8:
            lib.globals.lifeNum += 1
        lib.stg_overlay.overlayStatus[lib.stg_overlay.OverLayStatusIndex.LIFE_REMAIN] = 240
        ItemEffect(self.position, itemEffectLifeExtend)
        lib.sound.sfx['EXTEND_LIFE'].play()

class HyperExtend(Item):
    def __init__(self, position: pygame.Vector2) -> None:
        super().__init__(position, itemImage[3])

    def gain(self):
        if lib.globals.hyperNum < 8:
            lib.globals.hyperNum += 1
        lib.stg_overlay.overlayStatus[lib.stg_overlay.OverLayStatusIndex.HYPER_REMAIN] = 240
        ItemEffect(self.position, itemEffectHyperExtend)
        lib.sound.sfx['EXTEND_HYPER'].play()
