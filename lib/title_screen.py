import platform
import pygame

import lib.constants
import lib.globals
import lib.font
import lib.scene
import lib.script_engine.stage
import lib.sound
import lib.sprite.option

MENU = pygame.image.load('assets/ui-title-menu.png').convert_alpha()
MENU_ITEMS = tuple(
    (
        MENU.subsurface((0, x * 32, 128, 32)),
        MENU.subsurface((128, x * 32, 128, 32)),
    )
    for x in range(3)
)

OPTION = pygame.image.load('assets/ui-title-select.png').convert_alpha()
OPTION_ITEMS = tuple(OPTION.subsurface((0, x * 128, 384, 128)) for x in range(2))

with open('build-info.txt', 'r', encoding='utf-8') as f:
    BUILD_INFO = f.read().splitlines()

fontNormalRenderer = lib.font.FontRenderer(lib.font.FONT_NORMAL, (255, 255, 255))
fontSmallRenderer = lib.font.FontRenderer(lib.font.FONT_SMALL, (255, 255, 255))
versionText = fontSmallRenderer.render('\n'.join((
    f'Built at {BUILD_INFO[1]} (Commit {BUILD_INFO[0][:7]})',
    f'with Python {platform.python_version()} Pygame {pygame.version.ver}',
    '© 2021 TransparentLC https://akarin.dev',
)))

manualShade = pygame.Surface((400, 225), pygame.SRCALPHA)
pygame.draw.rect(manualShade, (0, 0, 0, 192), manualShade.get_rect(), 0, 8)
# 一行32个全角字符，一页最多12行，用----------------分页
manualPages = tuple(fontNormalRenderer.render(x.strip()) for x in f'''
# 基本的介绍

这是一个简单的弹幕射击游戏。目的是回避弹幕并击破敌机，在每一关的
最后有一个比较强的ＢＯＳＳ，击破后就算是过关了。

难度不是很高，可能是比东方Ｐｒｏｊｅｃｔ系列的Ｅａｓｙ难度还要简
单的程度，平衡性和游戏性也可能会很糟。不过因为是做着玩的所以还是
不要在意这些了，我也不是专业做游戏的嘛（逃

没有什么剧情，音乐和图片用的也都是免费素材而已。
----------------
# 操作方法

方向键　　　　　移动自机
ＬＳｈｉｆｔ键　使用低速移动
Ｚ键　　　　　　射击，按住不放就可以连射
Ｘ键　　　　　　开启火力强化模式（后述）
Ｐ键　　　　　　暂停游戏，再按一下就会恢复
Ｅｓｃ键　　　　返回标题画面
----------------
# 分数系统和奖励

射击分：自机的发射的子弹命中敌机，即可得到和造成的伤害相同的分数
击破分：击破各种敌机后，可以得到固定的分数
擦弹分：近距离擦过一个敌弹，可以得到＜同屏敌弹量／５＞的分数
火力强化时的消弹分：在火力强化模式下击毁一个敌弹，可以得到等同于
同屏敌弹量的分数
击破ＢＯＳＳ的奖励：击破ＢＯＳＳ的一个阶段就会触发一次全屏消弹，
可以得到＜同屏敌弹量＊（５０＋擦弹数／３）＞的分数

击破特定的敌人可以获得火力强化或残机作为奖励，最大可以累积８个，
满了的话就没有奖励了。
----------------
# 火力强化模式

因为没有做Ｂｏｍｂ系统，所以用这个系统作为替代。模仿的是《怒首领
蜂大复活》的Ｈｙｐｅｒ系统。但是，并不是像《大复活》那样通过连击
获得火力强化的机会……

在启动这个模式的一段时间内，自机发射子弹的速度和威力都会提升，并
且子弹还有消弹的功能，碰到敌弹可以将其击毁。虽然单个子弹的消弹次
数有限，但是飞到敌人面前还是足够的。除此之外，启动时还会给予短暂
的无敌时间，这样就不会被最致命的那个敌弹击中了。

注意：如果在用完火力强化前就中弹的话，那些强化的机会就被浪费了。
----------------
# 借物表

ＢＧＭ／ＳＥ：
＊魔王魂｜無料で使える森田交一の音楽
　https://maou.audio/
＊Pixabay
　https://pixabay.com/sound-effects/

图片素材：
＊AFruitaday!制作的1943 - The Battle of Midway精灵图
　https://www.spriters-resource.com/...
　.../arcade/1943thebattleofmidway/
----------------
# 关于

源代码以GNU AGPL 3.0许可证发布。
https://github.com/TransparentLC/project-striker

Commit: {BUILD_INFO[0]}
Build time: {BUILD_INFO[1]}

Built with:
　Python {platform.python_version()}
　Pygame {pygame.version.ver}
'''.split('----------------'))

def update():
    if lib.globals.keys[pygame.K_z] and not lib.globals.keysLastFrame[pygame.K_z]:
        if lib.globals.menuChoice == 0:
            lib.globals.groupPlayer.sprite.position.update(192, 400)
            lib.globals.groupPlayer.sprite.invincibleRemain = 0
            lib.globals.groupPlayer.sprite.hyperRemain = 0
            lib.globals.groupPlayer.sprite.invincibleRemain = 0
            lib.globals.groupPlayer.sprite.deathWait = 0
            lib.globals.score = 0
            lib.globals.scoreLastFrame = 0
            lib.globals.grazeCount = 0
            lib.globals.lifeNum = lib.constants.INITIAL_LIFENUM
            lib.globals.hyperNum = lib.constants.INITIAL_HYPERNUM
            lib.globals.messageQueue.clear()
            for g in (
                lib.globals.groupPlayerOption,
                lib.globals.groupPlayerBullet,
                lib.globals.groupEnemy,
                lib.globals.groupEnemyBullet,
                lib.globals.groupParticle,
            ):
                for s in g:
                    s.kill()
            lib.globals.menuSubChoice %= 2
            if lib.globals.menuSubChoice == 0:
                lib.globals.groupPlayer.options = [
                    lib.sprite.option.OptionTypeA(8, pygame.Vector2(-30, 5), pygame.Vector2(-20, -5), 20, 10),
                    lib.sprite.option.OptionTypeA(8, pygame.Vector2(30, 5), pygame.Vector2(20, -5), -20, -10),
                    lib.sprite.option.OptionTypeA(8, pygame.Vector2(-15, 20), pygame.Vector2(-8, -20), 10, 5),
                    lib.sprite.option.OptionTypeA(8, pygame.Vector2(15, 20), pygame.Vector2(8, -20), -10, -5),
                ]
            elif lib.globals.menuSubChoice == 1:
                lib.globals.groupPlayer.options = [
                    lib.sprite.option.OptionTypeB1(8, pygame.Vector2(-15, 20), pygame.Vector2(-25, 0), 12, 0),
                    lib.sprite.option.OptionTypeB0(8, pygame.Vector2(15, 20), pygame.Vector2(25, 0), -12, 0),
                    lib.sprite.option.OptionTypeB0(8, pygame.Vector2(-30, 5), pygame.Vector2(-45, 0), 30, 0),
                    lib.sprite.option.OptionTypeB1(8, pygame.Vector2(30, 5), pygame.Vector2(45, 0), -30, 0),
                ]
            with open('scriptfiles/stage/stage1.txt', 'r', encoding='utf-8') as f:
                lib.globals.stageEngine = lib.script_engine.stage.Engine(f.read())
            lib.globals.currentScene = lib.scene.Scene.STG_GAME
        elif lib.globals.menuChoice == 2:
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    if lib.globals.keys[pygame.K_UP] and not lib.globals.keysLastFrame[pygame.K_UP]:
        lib.globals.menuChoice = (lib.globals.menuChoice - 1) % len(MENU_ITEMS)
        lib.globals.menuSubChoice = 0
        lib.sound.sfx['MENU'].play()
    if lib.globals.keys[pygame.K_DOWN] and not lib.globals.keysLastFrame[pygame.K_DOWN]:
        lib.globals.menuChoice = (lib.globals.menuChoice + 1) % len(MENU_ITEMS)
        lib.globals.menuSubChoice = 0
        lib.sound.sfx['MENU'].play()
    if lib.globals.keys[pygame.K_LEFT] and not lib.globals.keysLastFrame[pygame.K_LEFT]:
        lib.globals.menuSubChoice -= 1
        lib.sound.sfx['PAGE'].play()
    if lib.globals.keys[pygame.K_RIGHT] and not lib.globals.keysLastFrame[pygame.K_RIGHT]:
        lib.globals.menuSubChoice += 1
        lib.sound.sfx['PAGE'].play()

def draw(surface: pygame.Surface):
    surface.blit(lib.scene.BACKGROUND_TITLE, (0, 0))
    for index, item in enumerate(MENU_ITEMS):
        surface.blit(item[0 if lib.globals.menuChoice == index else 1], (32, 320 + index * 32))

    if lib.globals.menuChoice == 0:
        surface.blit(OPTION_ITEMS[lib.globals.menuSubChoice % 2], (200, 310))
    elif lib.globals.menuChoice == 1:
        surface.blit(manualShade, (200, 210))
        surface.blit(manualPages[lib.globals.menuSubChoice % len(manualPages)], (208, 214))

    surface.blit(versionText, (10, 435))
