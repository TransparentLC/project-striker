import pygame

import lib.globals
import lib.utils

pygame.mixer.set_num_channels(64)

sfx: dict[str, pygame.mixer.Sound] = {
    'EXTEND_HYPER': pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/extend-hyper.ogg')),
    'EXTEND_LIFE': pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/extend-life.ogg')),
    'HYPER_ACTIVATE': pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/hyper-activate.ogg')),
    'HYPER_END': pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/hyper-end.ogg')),
    'BOSS_ALERT': pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/boss-alert.ogg')),
    'PHASE_START': pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/phase-start.ogg')),
    'BONUS': pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/bonus.ogg')),
    'PAUSE': pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/pause.ogg')),
    'PAGE': pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/page.ogg')),
    'MENU': pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/menu.ogg')),
    'COUNTDOWN': pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/countdown.ogg')),
    'GET_POINT': pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/get-point.ogg')),
    'GRAZE_A': pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/graze-a.ogg')),
    'GRAZE_B': pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/graze-b.ogg')),
    'EXPLODE_PLAYER': pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/explode-player.ogg')),
    'EXPLODE_ENEMY_A': pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/explode-enemy-a.ogg')),
    'EXPLODE_ENEMY_B': pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/explode-enemy-b.ogg')),
    'EXPLODE_ENEMY_C': pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/explode-enemy-c.ogg')),
    'EXPLODE_ENEMY_D': pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/explode-enemy-d.ogg')),
    'PLAYER_SHOOT_A': pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/player-shoot-a.ogg')),
    'PLAYER_SHOOT_B': pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/player-shoot-b.ogg')),
    'PLAYER_SHOOT_HIT_A': pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/player-shoot-hit-a.ogg')),
    'PLAYER_SHOOT_HIT_B': pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/player-shoot-hit-b.ogg')),
    'PLAYER_SHOOT_HIT_C': pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/player-shoot-hit-c.ogg')),
    'PLAYER_SHOOT_HIT_D': pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/player-shoot-hit-d.ogg')),
    'ENEMY_SHOOT_A': pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/enemy-shoot-a.ogg')),
    'ENEMY_SHOOT_B': pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/enemy-shoot-b.ogg')),
    'ENEMY_SHOOT_C': pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/enemy-shoot-c.ogg')),
    'ENEMY_SHOOT_D': pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/enemy-shoot-d.ogg')),
    'ENEMY_SHOOT_E': pygame.mixer.Sound(lib.utils.getResourceHandler('sound/sfx/enemy-shoot-e.ogg')),
}

for value in sfx.values():
    value.set_volume(.2)

sfx['COUNTDOWN'].set_volume(.5)
sfx['GET_POINT'].set_volume(.4)
sfx['PLAYER_SHOOT_A'].set_volume(.01)
sfx['PLAYER_SHOOT_B'].set_volume(.01)
sfx['PLAYER_SHOOT_HIT_A'].set_volume(.02)
sfx['PLAYER_SHOOT_HIT_B'].set_volume(.02)
sfx['PLAYER_SHOOT_HIT_C'].set_volume(.02)
sfx['PLAYER_SHOOT_HIT_D'].set_volume(.02)
sfx['EXPLODE_PLAYER'].set_volume(.8)
sfx['EXPLODE_ENEMY_A'].set_volume(.3)
sfx['EXPLODE_ENEMY_B'].set_volume(.4)
sfx['EXPLODE_ENEMY_C'].set_volume(.5)
sfx['EXPLODE_ENEMY_D'].set_volume(.5)
sfx['HYPER_ACTIVATE'].set_volume(.5)
sfx['HYPER_END'].set_volume(.5)
sfx['EXTEND_HYPER'].set_volume(.8)
sfx['EXTEND_LIFE'].set_volume(.8)
sfx['BOSS_ALERT'].set_volume(.6)

bgm: dict[str, tuple[str, str]] = {
    'TITLE': ('sound/bgm/title-a.ogg', 'sound/bgm/title-b.ogg'),
    'STAGE1': ('sound/bgm/stage1-a.ogg', 'sound/bgm/stage1-b.ogg'),
    'STAGE2': ('sound/bgm/stage2-a.ogg', 'sound/bgm/stage2-b.ogg'),
    'STAGE3': ('sound/bgm/stage3-a.ogg', 'sound/bgm/stage3-b.ogg'),
    'STAGE4': ('sound/bgm/stage4-a.ogg', 'sound/bgm/stage4-b.ogg'),
    'BOSS1': ('sound/bgm/boss1-a.ogg', 'sound/bgm/boss1-b.ogg'),
    'BOSS2': ('sound/bgm/boss2-a.ogg', 'sound/bgm/boss2-b.ogg'),
    'BOSS3': ('sound/bgm/boss3-a.ogg', 'sound/bgm/boss3-b.ogg'),
}

def playBgm(bgmName: str):
    if not lib.globals.config['bgm']:
        return
    bgmHeader, bgmLoop = bgm[bgmName]
    pygame.mixer.music.stop()
    pygame.mixer.music.load(lib.utils.getResourceHandler(bgmHeader))
    pygame.mixer.music.play()
    pygame.mixer.music.queue(lib.utils.getResourceHandler(bgmLoop), loops=-1)
