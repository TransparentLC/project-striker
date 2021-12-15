# 脚本系统说明

## 基本格式

每个脚本读取后会生成一个“执行环境”，包含这几个参数：

* `pointer` 类似于 CPU 中的 PC 寄存器，表示当前执行第几条指令，各种跳转指令会修改这个值。
* `wait` 剩余的需要等待的时间。
* `halted` 是否已终止执行。
* `vars` 一共 8 个变量，可以是数值或字符串。

脚本为纯文本，每一行对应一条指令，形如以下格式：

```plaintext
OPERATION param0 param1 param2 ... @ tag # comment
```

* `OPERATION` 指令名称。
* `param*` 指令中用到的参数，可以是整数、浮点数或字符串，每个指令所需的参数数量和类型都是固定的。
* `@ tag` 为这一行设置标签，主要用于自动计算跳转偏移。
* `# comment` 注释。

参数的值如果形如 `%...%`，则表示在运行时会被动态替换为某些值。例如 `%VAR_0%` 就表示替换为 0 号变量的值。

如果形如 `@tag`（注意这里的 `@` 后面没有空格），表示 tag 所代表的那一行相对于这一行的偏移，一般在跳转时使用。

一般来说，只要不处于 `wait` 或 `halted` 状态，脚本在每一帧就会连续地按照顺序和跳转执行指令。

## 指令说明

### 通用

`NOOP`

什么都不做。

`DEBUGGER`

便于下断点，或者只是 `print('debugger')` 而已。

`WAIT time:int`

让脚本阻塞等待一段时间，然后才会继续往下执行。时间都是以帧表示的，60f = 1s。

`HALT`

停止执行脚本。

`JUMP offset:int`

跳转到这行指令往后 `offset` 行的位置上。一般用 `@tag` 来自动计算偏移，当然直接填一个数上去也不是不行。

`JUMP_E  a:int|float b:int|float offset:int`

`JUMP_NE a:int|float b:int|float offset:int`

`JUMP_L  a:int|float b:int|float offset:int`

`JUMP_LE a:int|float b:int|float offset:int`

`JUMP_G  a:int|float b:int|float offset:int`

`JUMP_GE a:int|float b:int|float offset:int`

条件跳转。

`STORE        address:int value:int|float`

`RANDOM_INT   address:int min:int   max:int`

`RANDOM_FLOAT address:int min:float max:float`

将变量设为指定的值或一定范围内的随机整数/浮点数。

`INC address:int`

`DEC address:int`

将变量的值 +1 和 -1。

`ADD  address:int value:int|float`

`SUB  address:int value:int|float`

`MUL  address:int value:int|float`

`DIV  address:int value:int`

`MOD  address:int value:int`

`FDIV address:int value:int|float`

对变量的值进行四则运算，结果会覆盖那个变量的值。

### 敌机行动脚本

`REGISTER_DEATH offset:int`

设定在敌机被击破时跳转到某一条指令执行，可以设置死尸弹或者击破消弹之类的。

`REGISTER_BOSSBREAK offset:int`

设定在 BOSS 的血条打空时跳转到某一条指令执行。

`CALC_OFFSET address:int x:float y:float`

将相对于敌机的偏移转换绝对坐标，保存到变量。`address` 和 `address+1` 的值都会被修改。

`CALC_DIRECTION address:int x1:float y1:float x2:float y2:float`

计算从 `(x1, y1)` 指向 `(x2, y2)` 的角度，保存到变量。例如计算自机狙的角度就是 `CALC_DIRECTION 0 %ENEMY_X% %ENEMY_Y% %PLAYER_X% %PLAYER_Y%`。

`SET_POSITION          x:float y:float`

`SET_POSITION_RELATIVE x:float y:float`

设置敌机的位置，使用绝对值或相对于当前位置的值。

`SET_TEXTURE texture:str`

设置敌机的贴图。

`SET_HITPOINT hp:int`

设置敌机的血量。

`SET_SCORE score:int`

设置敌机击破后的分数。

`SET_INVINCIBLE time:int`

设置敌机的无敌时间。

`SET_EXPLOSION explosion:str`

设置敌机击破后使用的爆炸效果。

`SET_DEBRIS debris:str x:float y:float spreadSpeedMin:float spreadSpeedMax:float rotateSpeedMin:float rotateSpeedMax:float count:int`

设置敌机击破后飞出的碎片效果，可以设置碎片产生的位置、数量、飞出速度和旋转速度。可以设置多次。

`SET_HITBOX x:float y:float r:float`

添加一个指定位置和半径的圆作为判定区域，作为中弹和体术判定。坐标相对于敌机贴图中心。

`SET_SPEED speed:float`

设置速度，之后会对着另外设定的角度按照这个速度移动。

`SET_ANGLE          angle:float`

`SET_ANGLE_RELATIVE angle:float`

设置敌机旋转的角度，正上方为 0，方向是逆时针。判定区域和发弹位置也会和贴图一起旋转。

`SET_EXPLODE_SFX sfx:str`

设置击破后的音效。

`SET_BOSS`

设置这个敌机为 BOSS，可以读取血量显示在右侧。

`SET_BOSS_REMAIN remain:int`

设置 BOSS 还有几个攻击形态，在右侧展示成“★3”的样子。

`SET_BOSS_HPRANGE min:int max:int`

设置在右侧显示的 BOSS 血量范围，例如设置成 2000 - 3000 且 BOSS 当前血量为 2400，则会显示为“400/1000”。当前血量超过范围则显示为范围的长度，小于范围时会跳转到 `REGISTER_BOSSBREAK` 所指的位置（如果设定了的话）并显示为 0.

`MOVE          x:float y:float time:int mode:str`

`MOVE_RELATIVE x:float y:float time:int mode:str`

`MOVE_RANDOM   x:float y:float width:float height:float time:int mode:str`

添加一个移动任务到队列，在接下来的一段时间内敌机会以指定的缓动函数移动到指定的位置（`MOVE_RANDOM`可以指定一个区域内的随机位置）。这个移动过程是异步的，所以如果需要等到移动完成再执行指令的话，需要使用 `WAIT` 等待相同的时间。

`MOVE_CLEAR`

清空移动任务队列，当前的移动任务也会停止。

`SHOOT                 bullet:str x:float y:float speed:float angle:float`

`SHOOT_MULTIWAY        bullet:str x:float y:float speed:float angle:float fanSize:float ways:int`

`SHOOT_AIMING          bullet:str x:float y:float speed:float angle:float`

`SHOOT_AIMING_MULTIWAY bullet:str x:float y:float speed:float angle:float fanSize:float ways:int`

发射单个敌弹或在扇形上等分的多个敌弹，可以是绝对角度或自机狙。

`SFX sfx:str`

播放音效。

`CLEAR_BULLET`

消除屏幕上的所有敌弹。

`BONUS_BULLET`

根据同屏弹量结算一次加分。

`EXTEND_LIFE`
`EXTEND_HYPER`

奖励一个残机或火力强化。

`PRESET_ENEMY_A`

`PRESET_ENEMY_B`

`PRESET_ENEMY_C`

`PRESET_ENEMY_D`

`PRESET_ENEMY_E`

一些杂鱼敌机的预设，包括设置贴图、判定区域、效果、分数等。

### 关卡脚本

`JUMP_BOSS   offset:int`

`JUMP_NOBOSS offset:int`

有/没有 BOSS 时才会跳转。

`SET_SCROLL_SPEED speed:float`

设置背景卷轴移动的速度。

`LOAD_STAGE script:str`

加载另一个关卡脚本，当前运行的这个脚本将会被替代。

`SPAWN x:float y:float angle:float script:str`

在场景中刷出一个敌机，设置刷出的位置和角度以及使用的脚本。对于所有的敌机，超过显示区域 30px（正上方为 80px）就会被清除，显示区域是 384x448，所以坐标范围就是 `(-30, -80)` 到 `(424, 478)`。

`BGM bgm:str`

播放 BGM，由两个部分组成，先播放一遍 A 部分，之后循环播放 B 部分。

`BOSS_WARNING`

显示 BOSS 战的警告。

`SET_CLEARED`

将表示通关的全局变量设为 True。

`DISABLE_CONTINUE`

设置不允许续关，残机用完直接跳转到结果画面。游戏开始时默认会设定成允许续关。

`SHOW_RESULT`

结束游戏，跳转到结果画面。