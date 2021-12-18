import platform
import pygame

import lib.font
import lib.scene.title
import lib.sound
import lib.globals

from .title import background

fontNormalRenderer = lib.font.FontRenderer(lib.font.FONT_NORMAL, (255, 255, 255))

with open('build-info.txt', 'r', encoding='utf-8') as f:
    BUILD_INFO = f.read().splitlines()

manualShade = pygame.Surface((1050, 700), pygame.SRCALPHA)
pygame.draw.rect(manualShade, (0, 0, 0, 192), manualShade.get_rect(), 0, 8)
# 一行42个全角字符，一页最多17行，用----------------分页
manualPages = tuple(fontNormalRenderer.render(x.strip()) for x in f'''
# 基本的介绍

这是一个简单（？）的弹幕射击游戏，目的是回避弹幕并击破敌机，在每一关的最后有一个比较
强的ＢＯＳＳ，击破后就算是过关了。一共四关，最后一关是比较长的ＢＯＳＳ战，没有二周目
或者隐藏ＢＯＳＳ之类的设定，也没有什么剧情，音乐和图片用的都是免费素材而已。

难度不是很高，虽然一开始的目标是控制到东方Ｐｒｏｊｅｃｔ系列的Ｅａｓｙ到Ｎｏｒｍａｌ
难度之间，不过平衡性和游戏性还是可能会很糟。因为是做着玩的所以还是不要在意这些了，我
也不是专业做游戏的嘛（逃

# 操作方法

方向键　　　　　移动自机
ＬＳｈｉｆｔ键　使用低速移动
Ｚ键　　　　　　射击，按住不放就可以连射
Ｘ键　　　　　　开启火力强化模式（后述）
Ｐ键　　　　　　暂停游戏，再按一下就会恢复
Ｅｓｃ键　　　　返回标题画面
----------------
# 分数系统和奖励

射击分：自机的发射的子弹命中敌机，即可得到和造成伤害相同的分数。
击破分：击破各种敌机后，可以得到固定的分数。
擦弹分：近距离擦过一个敌弹，可以得到＜同屏敌弹量／５＞的分数。
火力强化时的消弹分：在火力强化模式下击毁一个敌弹，可以得到＜５＋同屏敌弹量／２０＞的
分数。
击破ＢＯＳＳ的奖励：击破ＢＯＳＳ的一个阶段就会触发一次全屏消弹，同时可以得到＜同屏敌
弹量＊（５０＋擦弹数／３）＞的分数。

分数达到２０００００、５０００００和１００００００各可以获得一个残机。击破特定的敌人
也可以获得火力强化或残机作为奖励。
----------------
# 火力强化模式

模仿了《怒首领蜂大复活》的Ｈｙｐｅｒ系统，因为没有做Ｂｏｍｂ系统所以用这个系统作为替
代。但是因为没有做《大复活》的连击系统，所以Ｈｙｐｅｒ的获得方式还是和Ｂｏｍｂ一样每
个残机自带３个。

在发动火力强化的一段时间内，自机发射子弹的速度和威力都会提升，并且子弹还有消弹功能，
碰到敌弹可以将其击毁。只有刚发动火力强化的一小段时间内是无敌的，不过这样也不用怕被最
致命的那个敌弹击中了。

注意：如果在用完火力强化前就中弹的话，没有使用的火力强化的机会就被浪费了，这里可没有
决死的设定啊！
----------------
# 一些小提示

＊活用火力强化的话，一个残机的生存时间就可以增加至少３倍，因此不想避弹／躲不过去的话
　就果断地按下Ｘ吧，资源应该是足够的。
＊敌机的大部分弹幕都是对着自机发射的，朝一个方向微移就没有什么威胁。如果快要被逼进死
　角，可以试试用大幅度的移动拉出一条缝隙，然后就可以穿过缝隙继续向反方向微移了。
＊不需要刻意擦弹刷分（除非你知道你在做什么），正常进行游戏的话分数是足够拿到三个奖残
　的，一不小心ＭＩＳＳ的话就得不偿失了。
＊弹幕密集的时候还是专注于避弹比较好，即使漏了几个杂鱼也没关系。
＊如果损失了所有的残机（满身疮痍），仍然可以通过不限次数的续关继续体验后面的关卡。但
　是，续关之后就不会再记录分数，而是以记录续关次数作为替代，当然也不能继续获得分数奖
　残。另外也有不能续关的时候……所以还是把不续关通关作为目标吧！
＊某个ＢＯＳＳ在进行某次攻击时会跑到屏幕正下方，虽然血条很短但是攻击似乎并没有效果。
　实际上这个“血条”是作为以秒为单位的计时器存在的，只要避弹到时间耗尽就可以了。
＊有些游戏机制和ＢＯＳＳ的弹幕是从东方Ｐｒｏｊｅｃｔ系列借鉴的，有没有哪些“符卡”看
　上去有点眼熟呢？
----------------
# 借物表

＊魔王魂｜無料で使える森田交一の音楽
　https://maou.audio/
＊Pixabay Royalty Free Sound Effects
　https://pixabay.com/sound-effects/
＊Source Han Serif
　https://source.typekit.com/source-han-serif/
＊Avería – The Average Font
　http://iotic.com/averia/
＊Arcade game "1943 - The Battle of Midway" sprite sheet ripped by "AFruitaday!"
　https://www.spriters-resource.com/arcade/1943thebattleofmidway/
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

currentPage = 0

def update():
    global currentPage
    if lib.globals.keys[pygame.K_LEFT] and not lib.globals.keysLastFrame[pygame.K_LEFT]:
        currentPage -= 1
        lib.sound.sfx['PAGE'].play()
    if lib.globals.keys[pygame.K_RIGHT] and not lib.globals.keysLastFrame[pygame.K_RIGHT]:
        currentPage += 1
        lib.sound.sfx['PAGE'].play()
    if lib.globals.keys[pygame.K_x] and not lib.globals.keysLastFrame[pygame.K_x]:
        lib.globals.nextScene = lib.scene.title
        lib.sound.sfx['PAGE'].play()

def draw(surface: pygame.Surface):
    surface.blit(background, (0, 0))
    surface.blit(manualShade, (115, 130))
    surface.blit(manualPages[currentPage % len(manualPages)], (135, 144))
