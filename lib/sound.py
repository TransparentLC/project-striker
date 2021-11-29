import pygame

pygame.mixer.set_num_channels(64)

sfx: dict[str, pygame.mixer.Sound] = {
    'EXTEND_HYPER': pygame.mixer.Sound('sound/sfx/extend-hyper.ogg'),
    'EXTEND_LIFE': pygame.mixer.Sound('sound/sfx/extend-life.ogg'),
    'HYPER_ACTIVATE': pygame.mixer.Sound('sound/sfx/hyper-activate.ogg'),
    'HYPER_END': pygame.mixer.Sound('sound/sfx/hyper-end.ogg'),
    'BOSS_ALERT': pygame.mixer.Sound('sound/sfx/boss-alert.ogg'),
    'PAUSE': pygame.mixer.Sound('sound/sfx/pause.ogg'),
    'PAGE': pygame.mixer.Sound('sound/sfx/page.ogg'),
    'MENU': pygame.mixer.Sound('sound/sfx/menu.ogg'),
    'GRAZE_A': pygame.mixer.Sound('sound/sfx/graze-a.ogg'),
    'GRAZE_B': pygame.mixer.Sound('sound/sfx/graze-b.ogg'),
    'EXPLODE_PLAYER': pygame.mixer.Sound('sound/sfx/explode-player.ogg'),
    'EXPLODE_ENEMY_A': pygame.mixer.Sound('sound/sfx/explode-enemy-a.ogg'),
    'EXPLODE_ENEMY_B': pygame.mixer.Sound('sound/sfx/explode-enemy-b.ogg'),
    'EXPLODE_ENEMY_C': pygame.mixer.Sound('sound/sfx/explode-enemy-c.ogg'),
    'EXPLODE_ENEMY_D': pygame.mixer.Sound('sound/sfx/explode-enemy-d.ogg'),
    'PLAYER_SHOOT_A': pygame.mixer.Sound('sound/sfx/player-shoot-a.ogg'),
    'PLAYER_SHOOT_B': pygame.mixer.Sound('sound/sfx/player-shoot-b.ogg'),
    'PLAYER_SHOOT_HIT_A': pygame.mixer.Sound('sound/sfx/player-shoot-hit-a.ogg'),
    'PLAYER_SHOOT_HIT_B': pygame.mixer.Sound('sound/sfx/player-shoot-hit-b.ogg'),
    'PLAYER_SHOOT_HIT_C': pygame.mixer.Sound('sound/sfx/player-shoot-hit-c.ogg'),
    'PLAYER_SHOOT_HIT_D': pygame.mixer.Sound('sound/sfx/player-shoot-hit-d.ogg'),
    'ENEMY_SHOOT_A': pygame.mixer.Sound('sound/sfx/enemy-shoot-a.ogg'),
    'ENEMY_SHOOT_B': pygame.mixer.Sound('sound/sfx/enemy-shoot-b.ogg'),
    'ENEMY_SHOOT_C': pygame.mixer.Sound('sound/sfx/enemy-shoot-c.ogg'),
    'ENEMY_SHOOT_D': pygame.mixer.Sound('sound/sfx/enemy-shoot-d.ogg'),
    'ENEMY_SHOOT_E': pygame.mixer.Sound('sound/sfx/enemy-shoot-e.ogg'),
}

for value in sfx.values():
    value.set_volume(.2)

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
    'BOSS1': ('sound/bgm/boss1-a.ogg', 'sound/bgm/boss1-b.ogg'),
}

def playBgm(bgmName: str):
    bgmHeader, bgmLoop = bgm[bgmName]
    pygame.mixer.music.stop()
    pygame.mixer.music.load(bgmHeader)
    pygame.mixer.music.play()
    pygame.mixer.music.queue(bgmLoop, loops=-1)
