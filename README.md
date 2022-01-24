# project-striker

[![build](https://github.com/TransparentLC/project-striker/actions/workflows/build.yml/badge.svg)](https://github.com/TransparentLC/project-striker/actions/workflows/build.yml)
![size](https://img.shields.io/github/repo-size/TransparentLC/project-striker)
![lines](https://img.shields.io/tokei/lines/github/TransparentLC/project-striker)

一个随便做做的弹幕射击游戏。

![](https://user-images.githubusercontent.com/47057319/147250475-e5aa18cd-5607-4901-a924-4879b264f492.png)

## 基本介绍

这是一个使用 [pygame](https://www.pygame.org/) 制作的简单（？）弹幕射击游戏，目的是回避弹幕并击破敌机，在每一关的最后有一个比较强的 BOSS，击破后就算是过关了。

一共有 3 种机体和 4 个关卡，通关流程大概为 20 分钟。[（通关演示/云玩家通道）
](https://hlsplayer.stream/video/stream.html?url=https://fs-im-kefu.7moor-fs2.com/im/2768a390-5474-11ea-afc9-7b323e3e16c0/C5KPb8eNLmwwSzIv.m3u8)

音乐和图片用的都是免费素材，具体请参见后面的[借物表](#借物表)。没有剧情之类的设定。另外这个游戏里有不少借鉴东方 Project 的地方……

因为我之前几乎没有制作游戏的经验，所以代码可能十分混乱，某些设计可能也不是最佳实践，肥肠抱歉 ( >﹏<。)

（更详细的介绍请参见游戏内的说明）

## 如何运行

最简单的方式是直接下载[使用 GitHub Actions 自动打包](https://github.com/TransparentLC/project-striker/actions/workflows/build.yml)的，可以在 Windows/Linux 下运行的单个可执行文件或 macOS 下的 bundle。打包使用 PyInstaller 完成。

未登录 GitHub 的话，可以在这里下载：

* [Windows 版](https://nightly.link/TransparentLC/project-striker/workflows/build/master/striker-Windows)
* [Linux 版](https://nightly.link/TransparentLC/project-striker/workflows/build/master/striker-Linux)
* [macOS 版](https://nightly.link/TransparentLC/project-striker/workflows/build/master/striker-macOS)

和系统相关的说明：

* Windows 版可能会被 Windows Defender 或其它杀毒软件报毒，属于误报。
* Linux 版打包和测试是在 Ubuntu 20.04 上进行的，并没有测试在其他 Linux 发行版上是否可以运行。可能需要使用 `LD_PRELOAD=/usr/lib64/libstdc++.so.6` 等方式强制使用系统库。
* macOS 版的 bundle 文件夹包含在一个 ZIP 文件内。
* 打包后的可执行文件为 x64 架构。

也可以从源代码运行，不过稍微有些麻烦：

<details>

* 需要 Python 3.9 或以上版本，使用之前的版本或许也可以运行，但我没有测试过。
* 使用 `pip install -r requirements.txt` 安装依赖。
* 参见[这里](https://github.com/TransparentLC/project-striker/blob/master/font/README.md)下载字体。
* 安装好 `gcc` 和 `g++` ，然后执行 `build-native.sh` 编译 C/C++ 的函数库。
    * 对于 Windows 用户，已经准备了编译好的 DLL。
    * 对于 macOS 用户，在编译前需要执行 `export libExtension=".dylib"`。
* 从 `main.py` 开始运行即可。

</details>

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

（想要改键或使用手柄？试试 [PowerToys](https://github.com/microsoft/PowerToys)、[JoyToKey](https://joytokey.net/) 之类的有按键映射功能的工具吧）

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
* [xBRZ: "Scale by rules" - high quality image upscaling filter by Zenju](https://sourceforge.net/projects/xbrz/files/xBRZ/) 像素画放大算法

## 可以改进的部分

~~做了当然会更好，虽然列在这里之后大概率就会一直摸了~~

* 更多的性能优化（人家的弹幕游戏引擎随随便便就[同屏几千甚至上万发](https://cowlevel.net/article/1882071)，你这一千发好意思吗）
* 完整的背景卷轴设计（素材不够）
* 键位修改（暂时可以用改键工具替代）
* ……

## 一些技术性较强的高级内容

### 对模组（MOD）的支持

<details>

通过加载自定义的模组文件，无需修改主程序代码即可实现替换图像、音频、关卡等功能。游戏会优先使用模组文件中相同路径的资源，如果无法找到则会继续使用自带的原版资源。

模组文件是包含以下目录的 tar 打包（请不要使用 gz、bz2、xz 等进行压缩），这些目录的具体用途可以参见[“目录结构”](#目录结构)部分：

* `assets`
* `scriptfiles`
* `sound`

在启动游戏时，可以使用环境变量 `STRIKER_MODDED_RESOURCE` 指定模组文件的路径。

</details>

### 关于判定和同屏弹幕量

<details>

自机、敌机及弹幕均使用圆形判定，对于 BOSS 之类的较大的敌机则会使用多个圆以尽可能地覆盖敌机图像。

BOSS 战中同屏弹幕量一般控制在 250 左右，但在保持 FPS 稳定在 60 左右（不出现处理落）的前提下，同屏弹幕的极限数量可以达到 1000 左右。

> 可以考证的其他一些弹幕射击游戏的同屏弹幕量：
>
> * 1998 年的长空超少年，同屏弹幕量一般不超过 300（STAGE 5B 的 BOSS 战，参见 PS4 版显示的计数）
> * 2003 年的绊地狱，同屏弹幕量一般不超过 150（里二周目 STAGE 5 光翼战，参见 PS4 版显示的计数，这两个的原作是街机游戏）
> * 2002 年的东方红魔乡，同屏弹幕上限 640
> * 2007 年的东方风神录，同屏弹幕上限 2000（参见[这里](https://www.zybuluo.com/wz520/note/83366)，这两个是使用 C++ 和 DirectX 制作的 PC 游戏）

由于 pygame 仅使用软件渲染，并且我没有使用多进程，所以只要 CPU 主频足够这个数值的差别就不会很大，显卡性能也不会产生影响。

~~Python 写的东西，还想要什么性能 (╯‵□′)╯︵┻━┻~~

</details>

### 目录结构

<details>

```plaintext
project-striker
│  .gitignore
│  build-info.txt # 在打包时记录打包时间及对应的commit信息
│  build.ps1 # 打包脚本
│  build.sh # 打包脚本
│  icon.ico
│  LICENSE
│  main.py # 入口文件
│  README.md
│  requirements-build.txt
│  requirements.txt
│
├─.github
│  └─workflows
│          build.yml # Github Actions 自动打包脚本
│
├─.vscode
│      launch.json
│
├─assets # 图片素材
│      ...
│
├─font # 字体
│      README.md
│      SourceHanSerifSC-Medium.otf
│
├─lib
│  │  constants.py # 部分常数
│  │  debug.py # 测试用函数，目前只有显示弹幕判定大小
│  │  font.py # 字体渲染，主要是处理多行文本
│  │  globals.py # 全局变量
│  │  scroll_map.py # 背景卷轴
│  │  sound.py # 背景音乐和音效播放
│  │  stg_overlay.py # 游戏主界面上提示分数/残机奖励等等的图层
│  │  utils.py # 一些工具函数及各种插值函数
│  │  __init__.py
│  │
│  ├─bullet
│  │  enemy_bullet.py # 敌机弹幕相关
│  │  player_bullet.py # 自机弹幕相关
│  │  __init__.py
│  │
│  ├─scene # 游戏中的各个界面
│  │  config.py
│  │  manual.py
│  │  result.py
│  │  select_option.py
│  │  stg.py
│  │  title.py
│  │  __init__.py
│  │
│  ├─script_engine # 敌机行动脚本和关卡脚本的解析
│  │  enemy.py
│  │  README.md
│  │  stage.py
│  │  __init__.py
│  │
│  └─sprite # 各种活动块相关
│     debris.py # 击破敌机后的碎片效果
│     enemy.py # 敌机
│     explosion.py # 击破敌机后的爆炸效果
│     item.py # 道具
│     option.py # 自机的子机
│     player.py # 自机
│     __init__.py
│
├─native # 以C/C++代码编译的函数库
│     ...
│
├─psd # 背景图片的源文件
│     ...
│
├─scriptfiles
│  ├─enemy # 敌机脚本
│  │      ...
│  │
│  ├─map # 背景卷轴内容
│  │      ...
│  │
│  └─stage # 关卡脚本
│         ...
│
├─sound
│  ├─bgm # 背景音乐
│  │      ...
│  │
│  └─sfx # 音效
│         ...
│
└─tool # 其他的工具脚本
      generate-font-subset.py # 生成子集化字体
      map-editor.html # 背景卷轴编辑器
      script-tag.py # 在编写脚本时生成随机的标签
      webp-lossless.py # 将图片无损转换为webp
```

</details>