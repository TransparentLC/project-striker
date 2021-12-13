import platform
import pygame

import lib.constants
import lib.globals
import lib.font
import lib.scene
import lib.script_engine.stage
import lib.sound
import lib.sprite.option

MENU = pygame.image.load('assets/ui-title-menu.webp').convert_alpha()
MENU_ITEMS = tuple(
    (
        MENU.subsurface((0, x * 64, 256, 64)),
        MENU.subsurface((256, x * 64, 256, 64)),
    )
    for x in range(3)
)

OPTION = pygame.image.load('assets/ui-title-select.webp').convert_alpha()
OPTION_ITEMS = tuple(OPTION.subsurface((0, x * 256, 768, 256)) for x in range(3))

with open('build-info.txt', 'r', encoding='utf-8') as f:
    BUILD_INFO = f.read().splitlines()

fontNormalRenderer = lib.font.FontRenderer(lib.font.FONT_NORMAL, (255, 255, 255))
fontSmallRenderer = lib.font.FontRenderer(lib.font.FONT_SMALL, (255, 255, 255))
versionText = fontSmallRenderer.render('\n'.join((
    f'Built at {BUILD_INFO[1]} (Commit {BUILD_INFO[0][:7]})',
    f'with Python {platform.python_version()} Pygame {pygame.version.ver}',
    '© 2021 TransparentLC https://akarin.dev',
)))

manualShade = pygame.Surface((800, 450), pygame.SRCALPHA)
pygame.draw.rect(manualShade, (0, 0, 0, 192), manualShade.get_rect(), 0, 8)
# 一行32个全角字符，一页最多12行，用----------------分页
manualPages = tuple(fontNormalRenderer.render(x.strip()) for x in f'''
# 基本的介绍

这是一个简单（？）的弹幕射击游戏，目的是回避弹幕并击破敌机，在每
一关的最后有一个比较强的ＢＯＳＳ，击破后就算是过关了。一共四关，
最后一关是比较长的ＢＯＳＳ战，但是没有二周目或者隐藏ＢＯＳＳ之类
的设定，也没有什么剧情，音乐和图片用的都是免费素材而已。

难度不是很高，虽然目标是控制到东方Ｐｒｏｊｅｃｔ系列的Ｅａｓｙ到
Ｎｏｒｍａｌ难度之间，不过平衡性和游戏性还是可能会很糟。因为是做
着玩的所以还是不要在意这些了，我也不是专业做游戏的嘛（逃

（按右方向键查看下一页）
----------------
# 操作方法

方向键　　　　　移动自机
ＬＳｈｉｆｔ键　使用低速移动
Ｚ键　　　　　　射击，按住不放就可以连射
Ｘ键　　　　　　开启火力强化模式（后述）
Ｐ键　　　　　　暂停游戏，再按一下就会恢复
Ｅｓｃ键　　　　返回标题画面

在标题画面按左右方向键，可以选择自机或在说明书中翻页。
----------------
# 分数系统和奖励

射击分：自机的发射的子弹命中敌机，即可得到和造成伤害相同的分数。
击破分：击破各种敌机后，可以得到固定的分数。
擦弹分：近距离擦过一个敌弹，可以得到＜同屏敌弹量／５＞的分数。
火力强化时的消弹分：在火力强化模式下击毁一个敌弹，可以得到等同于
＜５＋同屏敌弹量／２０＞的分数。
击破ＢＯＳＳ的奖励：击破ＢＯＳＳ的一个阶段就会触发一次全屏消弹，
可以得到＜同屏敌弹量＊（５０＋擦弹数／３）＞的分数。

分数达到２０００００、５０００００和１００００００各可以获得一个
残机。击破特定的敌人也可以获得火力强化或残机作为奖励。
----------------
# 火力强化模式

因为没有做Ｂｏｍｂ系统，所以用这个系统作为替代。模仿的是《怒首领
蜂大复活》的Ｈｙｐｅｒ系统。但是因为没有做《大复活》的连击系统，
所以Ｈｙｐｅｒ的获得方式还是和Ｂｏｍｂ一样，每个残机自带３个。

在发动火力强化的一段时间内，自机发射子弹的速度和威力都会提升，并
且子弹还有消弹的功能，碰到敌弹可以将其击毁。只有刚发动火力强化的
一小段时间内是无敌的，不过这样也不用怕被最致命的那个敌弹击中了。

注意：如果在用完火力强化前就中弹的话，那些强化的机会就被浪费了，
这里可没有决死的设定啊！
----------------
# 一些小提示

＊活用火力强化的话，一个残机的生存时间就可以增加至少３倍，因此不
　想避弹／躲不过去的话就果断地按下Ｘ吧。资源应该是足够的。
＊敌机的大部分弹幕都是对着自机发射的，朝一个方向微移就没有什么威
　胁。如果快要被逼进死角，可以试试用大幅度的移动拉出一条缝隙，然
　后就可以穿过那里继续向反方向微移了。
＊奖残的分数是足够的，所以不需要刻意擦弹刷分（除非你知道你在做什
　么），一不小心ＭＩＳＳ的话就得不偿失了。
＊弹幕密集的时候还是专注于避弹比较好，即使漏了几个杂鱼也没关系。
＊有些ＢＯＳＳ的弹幕是从东方Ｐｒｏｊｅｃｔ系列里借鉴的，能看出被
　借鉴的符卡有哪些吗？
----------------
# 借物表

ＢＧＭ／ＳＥ：
＊魔王魂｜無料で使える森田交一の音楽
　https://maou.audio/
＊Pixabay
　https://pixabay.com/sound-effects/
----------------
# 借物表

图片素材：
＊AFruitaday!制作的1943 - The Battle of Midway精灵图
　https://www.spriters-resource.com/...
　.../arcade/1943thebattleofmidway/
＊Unsplash
　https://unsplash.com/
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
            lib.globals.missedCount = 0
            lib.globals.hyperUsedCount = 0
            lib.globals.allCleared = False
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
            lib.globals.menuSubChoice %= 3
            lib.globals.optionType = lib.globals.menuSubChoice
            #
            if lib.globals.menuSubChoice == 0:
                lib.globals.groupPlayer.sprite.options = [
                    lib.sprite.option.OptionTypeA(8, pygame.Vector2(-30, 5), pygame.Vector2(-20, -5), 20, 10),
                    lib.sprite.option.OptionTypeA(8, pygame.Vector2(30, 5), pygame.Vector2(20, -5), -20, -10),
                    lib.sprite.option.OptionTypeA(8, pygame.Vector2(-15, 20), pygame.Vector2(-8, -20), 10, 5),
                    lib.sprite.option.OptionTypeA(8, pygame.Vector2(15, 20), pygame.Vector2(8, -20), -10, -5),
                ]
            elif lib.globals.menuSubChoice == 1:
                lib.globals.groupPlayer.sprite.options = [
                    lib.sprite.option.OptionTypeB1(8, pygame.Vector2(-15, 20), pygame.Vector2(-25, 0), 12, 0),
                    lib.sprite.option.OptionTypeB0(8, pygame.Vector2(15, 20), pygame.Vector2(25, 0), -12, 0),
                    lib.sprite.option.OptionTypeB0(8, pygame.Vector2(-30, 5), pygame.Vector2(-45, 0), 30, 0),
                    lib.sprite.option.OptionTypeB1(8, pygame.Vector2(30, 5), pygame.Vector2(45, 0), -30, 0),
                ]
            elif lib.globals.menuSubChoice == 2:
                lib.globals.groupPlayer.sprite.options = [
                    lib.sprite.option.OptionTypeC(8, pygame.Vector2(-25, 0), pygame.Vector2(-10, -15), 0, 0),
                    lib.sprite.option.OptionTypeC(8, pygame.Vector2(25, 0), pygame.Vector2(10, -15), 0, 0),
                ]
            with open('scriptfiles/stage/stage1.txt', 'r', encoding='utf-8') as f:
                lib.globals.stageEngine = lib.script_engine.stage.Engine(f.read())
            lib.globals.currentScene = lib.scene.Scene.STG
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
        surface.blit(item[0 if lib.globals.menuChoice == index else 1], (64, 640 + index * 64))

    if lib.globals.menuChoice == 0:
        surface.blit(OPTION_ITEMS[lib.globals.menuSubChoice % 3], (400, 620))
    elif lib.globals.menuChoice == 1:
        surface.blit(manualShade, (400, 420))
        surface.blit(manualPages[lib.globals.menuSubChoice % len(manualPages)], (416, 428))

    surface.blit(versionText, (20, 870))
