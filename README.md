# project-striker

[![build](https://github.com/TransparentLC/project-striker/actions/workflows/build.yml/badge.svg)](https://github.com/TransparentLC/project-striker/actions/workflows/build.yml)
![size](https://img.shields.io/github/repo-size/TransparentLC/project-striker)
![lines](https://img.shields.io/tokei/lines/github/TransparentLC/project-striker)

一个弹幕射击游戏。

![](https://dd-static.jd.com/ddimg/jfs/t1/161575/12/27237/268036/61bc8bceE310fa3d6/92e0be2447ea02eb.png)

## 基本介绍

这是一个使用 [pygame](https://www.pygame.org/) 制作的简单（？）弹幕射击游戏，目的是回避弹幕并击破敌机，在每一关的最后有一个比较强的 BOSS，击破后就算是过关了。

一共有 3 种机体和 4 个关卡，通关流程大概为 20 分钟。[（通关演示/云玩家通道）
](https://hlsplayer.stream/video/stream.html?url=https://ae01.alicdn.com/kf/Hec9064265cd24f74b6206280a4d91437D.jpg)

音乐和图片用的都是免费素材，具体请参见后面的[借物表](#借物表)。没有剧情之类的设定。另外这个游戏里有不少借鉴东方 Project 的地方……

因为我之前几乎没有制作游戏的经验，所以代码可能十分混乱，某些设计可能也不是最佳实践，肥肠抱歉 ( >﹏<。)

（更详细的介绍请参见游戏内的说明）

## 如何运行

最简单的方式是直接下载使用 GitHub Actions 自动打包的，可以在 Windows/Linux x64 下运行的单个[可执行文件](https://github.com/TransparentLC/project-striker/actions/workflows/build.yml)。打包使用 PyInstaller 完成。

未登录 GitHub 的话，可以在这里下载：

* [Windows 版](https://nightly.link/TransparentLC/project-striker/workflows/build/master/striker-Windows)
* [Linux 版](https://nightly.link/TransparentLC/project-striker/workflows/build/master/striker-Linux)

和系统相关的说明：

* Windows 版可能会被 Windows Defender 或其它杀毒软件报毒，属于误报。
* Linux 版打包和测试是在 Ubuntu 20.04 上进行的，并没有测试在其他 Linux 发行版上是否可以运行。
* 虽然 GitHub Actions 也可以选择使用 macOS 的镜像，但是由于我没有环境测试且对 macOS 软件生态不了解，因此并没有添加相关的打包支持。

也可以使用 `pip install -r requirements.txt` 安装依赖，并参见[这里](https://github.com/TransparentLC/project-striker/blob/master/font/README.md)下载字体后，直接从 `main.py` 以源代码形式运行（需要 Python 3.9 或以上版本，之前的版本或许也可以但我没有测试过）。

配置数据存储在用户目录下，删除即可完全初始化：

* Windows：`%HOMEPATH%/.striker`
* Linux：`~/.striker`

## 操作方法

* <kbd>↑</kbd> <kbd>↓</kbd> <kbd>←</kbd> <kbd>→</kbd> 移动自机、在标题画面的菜单项中选择
* <kbd>LShift</kbd> 使用低速移动
* <kbd>Z</kbd> 射击（按住不放就可以连射）、确认
* <kbd>X</kbd> 开启火力强化模式（参见游戏内的说明）、取消
* <kbd>P</kbd> 暂停游戏，再按一下就会恢复
* <kbd>Esc</kbd> 在游戏过程中返回标题画面

（想要改键或使用手柄？试试 [PowerToys](https://github.com/microsoft/PowerToys)、[JoyToKey](https://joytokey.net/)之类的有按键映射功能的工具吧）

## “太难了，根本不能通关” >_<

**可以的。**

所有的前半/后半道中，以及 BOSS 的每个攻击阶段（或者叫“身”）我都单独测试过了，在不丢失残机不使用火力强化的情况下都能通过，也就是说**没有无解的弹幕设计**。

实在不能通关的话，损失所有残机~~满身疮痍~~之后还可以续关（最终 BOSS 战中除外），并且没有次数限制。不过续关之后：

* 不再记录分数，以记录续关次数作为替代。
* 不能见到最终 BOSS。

所以还是以不续关通关为目标努力吧！

## 借物表

* [魔王魂｜無料で使える森田交一の音楽](https://maou.audio/) 所有的背景音乐和大部分的音效
* [Pixabay Royalty Free Sound Effects](https://pixabay.com/sound-effects/) 另一部分使用的音效
* [Source Han Serif](https://source.typekit.com/source-han-serif/) 使用的字体
* [Avería – The Average Font](http://iotic.com/averia/) 使用的字体
* [Arcade game "1943 - The Battle of Midway" sprite sheet ripped by "AFruitaday!"](https://www.spriters-resource.com/arcade/1943thebattleofmidway/) 几乎所有的精灵图
* [Unsplash](https://unsplash.com/) 部分背景图片素材

## 可以改进的部分

~~做了当然会更好，虽然列在这里之后大概率就会一直摸了~~

* 自机判定点的显示（其实是因为没找到合适的图片素材）
* 完整的背景卷轴设计（也是因为素材不够）
* 键位修改（暂时可以用改键工具替代）
* macOS 打包支持（对这方面完全哇嘎奶 QwQ）
* ……