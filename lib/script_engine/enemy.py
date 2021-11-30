import collections
import enum
import pygame
import random
import typing

import lib.bullet.enemy_bullet
import lib.globals
import lib.sprite
import lib.sprite.debris
import lib.sprite.enemy
import lib.sprite.explosion
import lib.sound
import lib.utils

class Opcode(enum.IntEnum):
    NOOP = enum.auto()
    DEBUGGER = enum.auto()
    HALT = enum.auto()
    WAIT = enum.auto()

    JUMP = enum.auto()
    JUMP_E = enum.auto()
    JUMP_NE = enum.auto()
    JUMP_L = enum.auto()
    JUMP_LE = enum.auto()
    JUMP_G = enum.auto()
    JUMP_GE = enum.auto()
    REGISTER_DEATH = enum.auto()

    STORE = enum.auto()
    RANDOM_INT = enum.auto()
    RANDOM_FLOAT = enum.auto()
    CALC_OFFSET = enum.auto()
    CALC_DIRECTION = enum.auto()
    INC = enum.auto()
    DEC = enum.auto()
    ADD = enum.auto()
    SUB = enum.auto()
    MUL = enum.auto()
    DIV = enum.auto()
    MOD = enum.auto()
    FDIV = enum.auto()

    SET_POSITION = enum.auto()
    SET_POSITION_RELATIVE = enum.auto()
    SET_TEXTURE = enum.auto()
    SET_HITPOINT = enum.auto()
    SET_SCORE = enum.auto()
    SET_INVINCIBLE = enum.auto()
    SET_EXPLOSION = enum.auto()
    SET_DEBRIS = enum.auto()
    SET_HITBOX = enum.auto()
    SET_SPEED = enum.auto()
    SET_ANGLE = enum.auto()
    SET_ANGLE_RELATIVE = enum.auto()
    SET_EXPLODE_SFX = enum.auto()

    SET_BOSS = enum.auto()
    SET_BOSS_REMAIN = enum.auto()
    SET_BOSS_HPRANGE = enum.auto()

    MOVE = enum.auto()
    MOVE_RELATIVE = enum.auto()
    MOVE_RANDOM = enum.auto()

    SHOOT = enum.auto()
    SHOOT_AHEAD = enum.auto()
    SHOOT_AIMING = enum.auto()
    SHOOT_MULTIWAY = enum.auto()
    SHOOT_AHEAD_MULTIWAY = enum.auto()
    SHOOT_AIMING_MULTIWAY = enum.auto()

    SFX = enum.auto()

    CLEAR_BULLET = enum.auto()
    BONUS_BULLET = enum.auto()
    EXTEND_LIFE = enum.auto()
    EXTEND_HYPER = enum.auto()

    PRESET_ENEMY_A = enum.auto()
    PRESET_ENEMY_B = enum.auto()
    PRESET_ENEMY_C = enum.auto()
    PRESET_ENEMY_D = enum.auto()
    PRESET_ENEMY_E = enum.auto()

    # = enum.auto()

EnemyTexturesTable = {
    'ENEMY_A': tuple(pygame.image.load(f'assets/enemy-a-{i}.png').convert_alpha() for i in range(2)),
    'ENEMY_B': tuple(pygame.image.load(f'assets/enemy-b-{i}.png').convert_alpha() for i in range(2)),
    'ENEMY_C': tuple(pygame.image.load(f'assets/enemy-c-{i}.png').convert_alpha() for i in range(2)),
    'ENEMY_D': tuple(pygame.image.load(f'assets/enemy-d-{i}.png').convert_alpha() for i in range(2)),
    'ENEMY_E': tuple(pygame.image.load(f'assets/enemy-e-{i}.png').convert_alpha() for i in range(2)),
    'BOSS_A': tuple(pygame.image.load(f'assets/boss-a-{i}.png').convert_alpha() for i in range(2)),
    'BOSS_B': tuple(pygame.image.load(f'assets/boss-b-{i}.png').convert_alpha() for i in range(2)),
}

MoveInterpolationFunctionTable = {
    'LINEAR': lib.utils.linearInterpolation,
    'EASE_IN_QUAD': lib.utils.easeInQuadInterpolation,
    'EASE_OUT_QUAD': lib.utils.easeOutQuadInterpolation,
    'EASE_INOUT_QUAD': lib.utils.easeInOutQuadInterpolation,
    'EASE_IN_CUBIC': lib.utils.easeInCubicInterpolation,
    'EASE_OUT_CUBIC': lib.utils.easeOutCubicInterpolation,
    'EASE_INOUT_CUBIC': lib.utils.easeInOutCubicInterpolation,
}

ExplosionTable = {
    'SMALL_A': lib.sprite.explosion.ExplosionPlaneSmallA,
    'SMALL_B': lib.sprite.explosion.ExplosionPlaneSmallB,
    'MEDIUM_A': lib.sprite.explosion.ExplosionPlaneMediumA,
    'MEDIUM_B': lib.sprite.explosion.ExplosionPlaneMediumB,
    'LARGE': lib.sprite.explosion.ExplosionPlaneLarge,
}

DebrisTable = {
    'DEBRIS_A': lib.sprite.debris.DebrisA,
    'DEBRIS_B': lib.sprite.debris.DebrisB,
}

BulletTextureTable = {
    'TYPE_A': pygame.image.load('assets/enemy-bullet-a.png').convert_alpha(),
    'TYPE_B': pygame.image.load('assets/enemy-bullet-b.png').convert_alpha(),
    'TYPE_C': pygame.image.load('assets/enemy-bullet-c.png').convert_alpha(),
    'TYPE_D': pygame.image.load('assets/enemy-bullet-d.png').convert_alpha(),
    'TYPE_E': pygame.image.load('assets/enemy-bullet-e.png').convert_alpha(),
}

BulletSizeTable = {
    'TYPE_A': 2,
    'TYPE_B': 4,
    'TYPE_C': 2.5,
    'TYPE_D': 3,
    'TYPE_E': 5,
}

class Engine:
    @staticmethod
    def parseLine(line: str) -> tuple[tuple[Opcode, list[typing.Union[int, float, str]]], typing.Optional[str]]:
        params = line.split()
        if not params:
            return (None, None)
        opcode = params.pop(0)
        if opcode == '#':
            return (None, None)
        opcode = Opcode[opcode]

        for index, value in enumerate(params):
            if value == '#':
                return ((opcode, params[:index]), None)
            elif value == '@':
                return ((opcode, params[:index]), params[index + 1])
            try:
                params[index] = int(value)
            except ValueError:
                try:
                    params[index] = float(value)
                except ValueError:
                    pass
        return ((opcode, params), None)

    @staticmethod
    def parseScript(script: str) -> typing.Sequence[tuple[Opcode, typing.Sequence[typing.Union[int, float, str]]]]:
        result: list[tuple[Opcode, list[typing.Union[int, float, str]]]] = []
        lineTags: dict[str, int] = {}
        lineCounter = 0
        for line in script.splitlines():
            parsed, tag = Engine.parseLine(line)
            if tag:
                lineTags[tag] = lineCounter
            if parsed:
                result.append(parsed)
                lineCounter += 1
        for i, r in enumerate(result):
            for j, p in enumerate(r[1]):
                if isinstance(p, str) and p[0] == '@':
                    r[1][j] = lineTags[p[1:]] - i
        # for r in result:
        #     print(r)
        return result

    def __init__(self, context: 'lib.sprite.enemy.Enemy', script: str) -> None:
        self.instruction = Engine.parseScript(script)
        self.context = context
        self.pointer = 0
        self.pointerDeath: int = None
        self.wait = 0
        self.halted = False
        self.movementTask: tuple[
            pygame.Vector2,
            int,
            typing.Callable[
                [float, pygame.Vector2, pygame.Vector2],
                pygame.Vector2
            ]
        ] = None
        self.movementCounter = 0
        self.movementFrom: pygame.Vector2 = None
        # 只使用append和popleft作为队列使用
        self.movementQueue: typing.Deque[tuple[pygame.Vector2, int]] = collections.deque()
        self.vars: list[typing.Union[int, float, str]] = list(None for x in range(8))

    def applyParamsReplacement(self, params: typing.Sequence[typing.Union[int, float, str]]) -> None:
        result = []
        for value in params:
            isVar = False
            if isinstance(value, str) and value.startswith('%VAR_'):
                for i in range(8):
                    if value == f'%VAR_{i}%':
                        result.append(self.vars[i])
                        isVar = True
                        break
            if not isVar:
                if value == '%HITPOINT%':
                    result.append(self.context.hitpoint)
                elif value == '%FRAMECOUNTER%':
                    result.append(self.context.frameCounter)
                elif value == '%AIM_PLAYER%':
                    result.append(-pygame.Vector2().angle_to(lib.globals.groupPlayer.sprite.position - self.context.position) - 90)
                elif value == '%PLAYER_X%':
                    result.append(lib.globals.groupPlayer.sprite.position.x)
                elif value == '%PLAYER_Y%':
                    result.append(lib.globals.groupPlayer.sprite.position.y)
                elif value == '%ENEMY_X%':
                    result.append(self.context.position.x)
                elif value == '%ENEMY_Y%':
                    result.append(self.context.position.y)
                else:
                    result.append(value)
        return result

    def update(self):
        if self.wait > 0:
            self.wait -= 1

        while not self.halted and not self.wait:
            opcode, params = self.instruction[self.pointer]
            params = self.applyParamsReplacement(params)
            # print(opcode, params, self.vars)
            self.pointer += 1
            self.executeOpcode(opcode, params)

        if not self.movementTask and self.movementQueue:
            self.movementCounter = 0
            self.movementFrom = pygame.Vector2(self.context.position)
            self.movementTask = self.movementQueue.popleft()
        if self.movementTask:
            self.movementCounter += 1
            self.context.position.update(
                self.movementTask[2](
                    self.movementCounter / self.movementTask[1],
                    self.movementFrom,
                    self.movementTask[0],
                )
            )
            if self.movementCounter >= self.movementTask[1]:
                self.movementTask = None

    def executeOpcode(self, opcode: Opcode, params: typing.Sequence[typing.Union[int, float, str]]):
        if opcode == Opcode.NOOP:
            # 什么也不做
            pass
        elif opcode == Opcode.DEBUGGER:
            # 便于下断点，或者只是输出一个debugger而已
            print('Debugger triggered from line', self.pointer)
        elif opcode == Opcode.WAIT:
            # 让脚本阻塞暂停一段时间，时间都是以帧表示的，60f=1s
            params: tuple[int] = params
            waitTime, = params

            self.wait = waitTime
        elif opcode == Opcode.HALT:
            # 停止执行脚本

            self.halted = True
        elif opcode == Opcode.JUMP:
            # 跳转到这行指令往后offset行的位置上
            params: tuple[int] = params
            offset, = params

            self.pointer += offset - 1
        elif opcode == Opcode.JUMP_E:
            # 相等时才跳转
            params: tuple[typing.Union[int, float], typing.Union[int, float], int] = params
            a, b, offset = params

            if a == b:
                self.pointer += offset - 1
        elif opcode == Opcode.JUMP_NE:
            # 不等时才跳转
            params: tuple[typing.Union[int, float], typing.Union[int, float], int] = params
            a, b, offset = params

            if a != b:
                self.pointer += offset - 1
        elif opcode == Opcode.JUMP_L:
            # 小于时才跳转
            params: tuple[typing.Union[int, float], typing.Union[int, float], int] = params
            a, b, offset = params

            if a < b:
                self.pointer += offset - 1
        elif opcode == Opcode.JUMP_LE:
            # 小于等于时才跳转
            params: tuple[typing.Union[int, float], typing.Union[int, float], int] = params
            a, b, offset = params

            if a <= b:
                self.pointer += offset - 1
        elif opcode == Opcode.JUMP_G:
            # 大于时才跳转
            params: tuple[typing.Union[int, float], typing.Union[int, float], int] = params
            a, b, offset = params

            if a > b:
                self.pointer += offset - 1
        elif opcode == Opcode.JUMP_GE:
            # 大于等于时才跳转
            params: tuple[typing.Union[int, float], typing.Union[int, float], int] = params
            a, b, offset = params

            if a >= b:
                self.pointer += offset - 1
        elif opcode == Opcode.REGISTER_DEATH:
            # 设定在敌机被击破时跳转到某一条指令执行（和上面的类似，指令的参数是相对于这一条的偏移）
            # 不设置的话就不会执行
            # 可以设置死尸弹或者击破消弹之类的
            params: tuple[int] = params
            offset, = params

            self.pointerDeath = self.pointer + offset - 1
        elif opcode == Opcode.STORE:
            # 在指定位置（0-7）保存数值
            params: tuple[int, typing.Union[int, float]] = params
            address, value = params

            self.vars[address] = value
        elif opcode == Opcode.RANDOM_INT:
            # 在指定位置保存指定范围的随机整数
            params: tuple[int, int, int] = params
            address, minValue, maxValue = params

            self.vars[address] = random.randint(minValue, maxValue)
        elif opcode == Opcode.RANDOM_FLOAT:
            # 在指定位置保存指定范围的随机浮点数
            params: tuple[int, float, float] = params
            address, minValue, maxValue = params

            self.vars[address] = minValue + (maxValue - minValue) * random.random()
        elif opcode == Opcode.CALC_OFFSET:
            # 将相对于敌机的偏移转换绝对坐标，保存在指定位置
            params: tuple[int, float, float] = params
            address, x, y = params

            position = self.context.position + pygame.Vector2(x, y).rotate(-self.context.angle)
            self.vars[address] = position.x
            self.vars[address + 1] = position.y
        elif opcode == Opcode.CALC_DIRECTION:
            # 计算从(x1, y1)指向(x2, y2)的角度，保存在指定位置
            # 例如计算自机狙的角度就是：
            # CALC_DIRECTION 0 %ENEMY_X% %ENEMY_Y% %PLAYER_X% %PLAYER_Y%
            params: tuple[int, float, float, float, float] = params
            address, x1, y1, x2, y2 = params

            self.vars[address] = -pygame.Vector2().angle_to(pygame.Vector2(x2 - x1, y2 - y1)) - 90
        elif opcode == Opcode.INC:
            # 变量值+1
            params: tuple[int] = params
            address, = params

            self.vars[address] += 1
        elif opcode == Opcode.DEC:
            # 变量值-1
            params: tuple[int] = params
            address, = params

            self.vars[address] -= 1
        elif opcode == Opcode.ADD:
            # 变量值相加
            params: tuple[int, typing.Union[int, float]] = params
            address, value = params

            self.vars[address] += value
        elif opcode == Opcode.SUB:
            # 变量值相减
            params: tuple[int, typing.Union[int, float]] = params
            address, value = params

            self.vars[address] -= value
        elif opcode == Opcode.MUL:
            # 变量值相乘
            params: tuple[int, typing.Union[int, float]] = params
            address, value = params

            self.vars[address] *= value
        elif opcode == Opcode.DIV:
            # 变量值相除（整数），返回商
            params: tuple[int, int] = params
            address, value = params

            self.vars[address] = int(self.vars[address]) // int(value)
        elif opcode == Opcode.MOD:
            # 变量值相除（整数），返回余数
            params: tuple[int, int] = params
            address, value = params

            self.vars[address] = int(self.vars[address]) % int(value)
        elif opcode == Opcode.FDIV:
            # 变量值相除（浮点）
            params: tuple[int, typing.Union[int, float]] = params
            address, value = params

            self.vars[address] /= value
        elif opcode == Opcode.SET_POSITION:
            # 设置位置（绝对值）
            params: tuple[float, float] = params
            x, y = params

            self.context.position.update(x, y)
        elif opcode == Opcode.SET_POSITION_RELATIVE:
            # 设置位置（相当于现在的位置）
            params: tuple[float, float] = params
            x, y = params

            self.context.position += pygame.Vector2(x, y)
        elif opcode == Opcode.SET_TEXTURE:
            # 设置贴图
            params: tuple[str] = params
            textures, = params

            self.context.textures = EnemyTexturesTable[textures]
        elif opcode == Opcode.SET_HITPOINT:
            # 设置血量
            params: tuple[int] = params
            hitpoint, = params

            self.context.hitpoint = hitpoint
        elif opcode == Opcode.SET_SCORE:
            # 设置击破后的分数
            params: tuple[int] = params
            score, = params

            self.context.score = score
        elif opcode == Opcode.SET_INVINCIBLE:
            # 设置无敌时间
            params: tuple[int] = params
            invincibleRemain, = params

            self.context.invincibleRemain = invincibleRemain
        elif opcode == Opcode.SET_EXPLOSION:
            # 设置爆炸效果
            params: tuple[str] = params
            explosion, = params

            self.context.explosion = ExplosionTable[explosion]
        elif opcode == Opcode.SET_DEBRIS:
            # 添加爆炸后产生的碎片，坐标相对于中心
            params: tuple[str, float, float, float, float, float, float, int] = params
            debris, x, y, spreadSpeedMin, spreadSpeedMax, rotateSpeedMin, rotateSpeedMax, count = params

            for i in range(count):
                self.context.debris.append((
                    DebrisTable[debris],
                    pygame.Vector2(x, y),
                    spreadSpeedMin, spreadSpeedMax,
                    rotateSpeedMin, rotateSpeedMax,
                ))
        elif opcode == Opcode.SET_HITBOX:
            # 添加碰撞箱（中弹和体术判定，实际是个圆），坐标相对于中心
            params: tuple[float, float, float] = params
            x, y, r = params

            self.context.hitbox.append(lib.sprite.Hitbox(pygame.Vector2(x, y), r))
        elif opcode == Opcode.SET_SPEED:
            # 设置速度，之后会按照这个速度和指定角度移动
            # 设置了MOVE以后速度就会被清零
            params: tuple[float] = params
            speed, = params

            self.context.speed.update(pygame.Vector2(0, -speed).rotate(-self.context.angle))
        elif opcode == Opcode.SET_ANGLE:
            # 设置角度，正上方为0，逆时针方向
            params: tuple[float] = params
            angle, = params

            self.context.angle = angle
        elif opcode == Opcode.SET_ANGLE_RELATIVE:
            # 设置角度，相对于原始值
            params: tuple[float] = params
            angle, = params

            self.context.angle += angle
        elif opcode == Opcode.SET_EXPLODE_SFX:
            # 设置击破后的音效
            params: tuple[str] = params
            sfxName, = params

            self.context.explodeSfx = lib.sound.sfx[sfxName]
        elif opcode == Opcode.SET_BOSS:
            # 设置这个敌机为BOSS，可以读取血量显示在右侧

            lib.globals.groupBoss.sprite = self.context
        elif opcode == Opcode.SET_BOSS_REMAIN:
            # 设置BOSS还有几个攻击形态，只是在右侧展示而已
            params: tuple[int] = params
            remain, = params

            lib.globals.bossRemain = remain
        elif opcode == Opcode.SET_BOSS_HPRANGE:
            # 设置显示的BOSS血量范围，例如设置成2000-3000且BOSS血量为2400则显示为400/1000
            params: tuple[int, int] = params
            hpMin, hpMax = params

            lib.globals.bossHitpointRangeMin = hpMin
            lib.globals.bossHitpointRangeMax = hpMax
        elif opcode == Opcode.MOVE:
            # 在一段时间内以指定的缓动函数直线移动到某坐标
            # 这个移动过程是异步的，因此如果需要等待移动完成再执行指令的话需要使用WAIT
            params: tuple[float, float, int, str] = params
            x, y, time, mode = params

            self.context.speed.update(0, 0)
            self.movementQueue.append((
                pygame.Vector2(x, y),
                time,
                MoveInterpolationFunctionTable[mode],
            ))
        elif opcode == Opcode.MOVE_RELATIVE:
            # 同上，但是坐标改成了相对的
            params: tuple[float, float, int, str] = params
            x, y, time, mode = params

            self.context.speed.update(0, 0)
            self.movementQueue.append((
                self.context.position + pygame.Vector2(x, y),
                time,
                MoveInterpolationFunctionTable[mode],
            ))
        elif opcode == Opcode.MOVE_RANDOM:
            # 移动到区域中的随机位置
            params: tuple[float, float, float, float, int, str] = params
            x, y, width, height, time, mode = params

            self.context.speed.update(0, 0)
            self.movementQueue.append((
                pygame.Vector2(x + random.random() * width, y + random.random() * height),
                time,
                MoveInterpolationFunctionTable[mode],
            ))
        elif opcode == Opcode.SHOOT:
            # 在指定偏移的位置以绝对角度射击
            params: tuple[str, float, float, float, float] = params
            bullet, x, y, speed, angle = params

            lib.bullet.enemy_bullet.EnemyBullet(
                self.context.position + pygame.Vector2(x, y).rotate(-self.context.angle),
                speed,
                angle,
                BulletSizeTable[bullet],
                BulletTextureTable[bullet],
            )
        elif opcode == Opcode.SHOOT_MULTIWAY:
            # 同上，但是可以设置扇形角度和way数了，可以用来发射奇数弹/偶数弹/开花弹
            params: tuple[str, float, float, float, float, float, int] = params
            bullet, x, y, speed, angle, fanSize, ways = params

            for i in range(ways):
                fanAngle = (i - (ways - 1) / 2) / (ways - 1) * fanSize
                lib.bullet.enemy_bullet.EnemyBullet(
                    self.context.position + pygame.Vector2(x, y).rotate(-self.context.angle),
                    speed,
                    fanAngle + angle,
                    BulletSizeTable[bullet],
                    BulletTextureTable[bullet],
                )
        elif opcode == Opcode.SHOOT_AHEAD:
            # 在指定偏移的位置以相对于敌机自己的角度射击
            params: tuple[str, float, float, float, float] = params
            bullet, x, y, speed, angle = params

            lib.bullet.enemy_bullet.EnemyBullet(
                self.context.position + pygame.Vector2(x, y).rotate(-self.context.angle),
                speed,
                self.context.angle + angle,
                BulletSizeTable[bullet],
                BulletTextureTable[bullet],
            )
        elif opcode == Opcode.SHOOT_AHEAD_MULTIWAY:
            # 同上
            params: tuple[str, float, float, float, float, float, int] = params
            bullet, x, y, speed, angle, fanSize, ways = params

            for i in range(ways):
                fanAngle = (i - (ways - 1) / 2) / (ways - 1) * fanSize
                lib.bullet.enemy_bullet.EnemyBullet(
                    self.context.position + pygame.Vector2(x, y).rotate(-self.context.angle),
                    speed,
                    fanAngle + self.context.angle + angle,
                    BulletSizeTable[bullet],
                    BulletTextureTable[bullet],
                )
        elif opcode == Opcode.SHOOT_AIMING:
            # 在指定偏移的位置以相对瞄准自机的角度射击
            params: tuple[str, float, float, float, float] = params
            bullet, x, y, speed, angle = params

            shootPosition = self.context.position + pygame.Vector2(x, y).rotate(-self.context.angle)
            lib.bullet.enemy_bullet.EnemyBullet(
                shootPosition,
                speed,
                -pygame.Vector2().angle_to(lib.globals.groupPlayer.sprite.position - shootPosition) - 90 + angle,
                BulletSizeTable[bullet],
                BulletTextureTable[bullet],
            )
        elif opcode == Opcode.SHOOT_AIMING_MULTIWAY:
            # 同上
            params: tuple[str, float, float, float, float, float, int] = params
            bullet, x, y, speed, angle, fanSize, ways = params

            shootPosition = self.context.position + pygame.Vector2(x, y).rotate(-self.context.angle)
            for i in range(ways):
                fanAngle = (i - (ways - 1) / 2) / (ways - 1) * fanSize
                lib.bullet.enemy_bullet.EnemyBullet(
                    shootPosition,
                    speed,
                    -pygame.Vector2().angle_to(lib.globals.groupPlayer.sprite.position - shootPosition) - 90 + fanAngle + angle,
                    BulletSizeTable[bullet],
                    BulletTextureTable[bullet],
                )
        elif opcode == Opcode.SFX:
            # 播放音效
            params: tuple[str] = params
            sfxName, = params

            lib.sound.sfx[sfxName].play()
        elif opcode == Opcode.CLEAR_BULLET:
            # 消除所有敌弹
            for b in lib.globals.groupEnemyBullet:
                b: lib.bullet.enemy_bullet.EnemyBullet
                b.explode()
        elif opcode == Opcode.BONUS_BULLET:
            # 根据同屏弹量结算一次加分
            bonus = len(lib.globals.groupEnemyBullet) * (50 + lib.globals.grazeCount // 3)
            lib.globals.score += bonus
            lib.globals.messageQueue.append([f'Bonus!        {bonus:8d}', 180])
        elif opcode == Opcode.EXTEND_LIFE:
            # 奖残
            if lib.globals.lifeNum < 8:
                lib.globals.lifeNum += 1
                lib.globals.messageQueue.append(['Life Extend!', 180])
                lib.sound.sfx['EXTEND_LIFE'].play()
        elif opcode == Opcode.EXTEND_HYPER:
            # 奖hyper
            if lib.globals.hyperNum < 8:
                lib.globals.hyperNum += 1
                lib.globals.messageQueue.append(['Hyper Extend!', 180])
                lib.sound.sfx['EXTEND_HYPER'].play()
        elif opcode == Opcode.PRESET_ENEMY_A:
            # 大型杂鱼敌机的预设，等效于以下脚本：
            # SET_TEXTURE ENEMY_A
            # SET_EXPLOSION LARGE
            # SET_HITBOX 0 12 10
            # SET_HITBOX 0 -10 12
            # SET_HITBOX -19 -6 8
            # SET_HITBOX 19 -6 8
            # SET_DEBRIS DEBRIS_A -20 -6 .125 2 1 5 1
            # SET_DEBRIS DEBRIS_A 20 -6 .125 2 1 5 1
            # SET_DEBRIS DEBRIS_B 0 12 .125 2 1 5 2
            # SET_DEBRIS DEBRIS_B 0 -10 .125 2 1 5 1
            # SET_SCORE 1000
            self.context.textures = EnemyTexturesTable['ENEMY_A']
            self.context.explosion = ExplosionTable['LARGE']
            self.context.hitbox = [
                lib.sprite.Hitbox(pygame.Vector2(0, 12), 10),
                lib.sprite.Hitbox(pygame.Vector2(0, -10), 12),
                lib.sprite.Hitbox(pygame.Vector2(-19, -6), 8),
                lib.sprite.Hitbox(pygame.Vector2(19, -6), 8),
            ]
            self.context.debris = [
                (DebrisTable['DEBRIS_A'], pygame.Vector2(-20, -6), .125, 2, 1, 5),
                (DebrisTable['DEBRIS_A'], pygame.Vector2(20, -6), .125, 2, 1, 5),
                (DebrisTable['DEBRIS_B'], pygame.Vector2(0, 12), .125, 2, 1, 5),
                (DebrisTable['DEBRIS_B'], pygame.Vector2(0, 12), .125, 2, 1, 5),
                (DebrisTable['DEBRIS_B'], pygame.Vector2(0, -10), .125, 2, 1, 5),
            ]
            self.context.score = 1000
            self.context.explodeSfx = lib.sound.sfx['EXPLODE_ENEMY_C']
        elif opcode == Opcode.PRESET_ENEMY_B:
            # 中型杂鱼敌机的预设，对应的脚本略
            self.context.textures = EnemyTexturesTable['ENEMY_B']
            self.context.explosion = ExplosionTable['MEDIUM_A']
            self.context.hitbox = [
                lib.sprite.Hitbox(pygame.Vector2(0, 5), 6),
                lib.sprite.Hitbox(pygame.Vector2(6, -2), 8),
                lib.sprite.Hitbox(pygame.Vector2(-6, -2), 8),
            ]
            self.context.debris = [
                (DebrisTable['DEBRIS_B'], pygame.Vector2(0, 5), .125, 1.75, 1, 3),
                (DebrisTable['DEBRIS_A'], pygame.Vector2(6, -2), .125, 1.75, 1, 3),
                (DebrisTable['DEBRIS_A'], pygame.Vector2(-6, -2), .125, 1.75, 1, 3),
            ]
            self.context.score = 500
            self.context.explodeSfx = lib.sound.sfx['EXPLODE_ENEMY_B']
        elif opcode == Opcode.PRESET_ENEMY_C:
            # 中型杂鱼敌机的预设
            self.context.textures = EnemyTexturesTable['ENEMY_C']
            self.context.explosion = ExplosionTable['MEDIUM_B']
            self.context.hitbox = [
                lib.sprite.Hitbox(pygame.Vector2(0, 5), 6),
                lib.sprite.Hitbox(pygame.Vector2(6, -2), 8),
                lib.sprite.Hitbox(pygame.Vector2(-6, -2), 8),
            ]
            self.context.debris = [
                (DebrisTable['DEBRIS_B'], pygame.Vector2(0, 5), .125, 1.75, 1, 3),
                (DebrisTable['DEBRIS_A'], pygame.Vector2(6, -2), .125, 1.75, 1, 3),
                (DebrisTable['DEBRIS_A'], pygame.Vector2(-6, -2), .125, 1.75, 1, 3),
            ]
            self.context.score = 500
            self.context.explodeSfx = lib.sound.sfx['EXPLODE_ENEMY_B']
        elif opcode == Opcode.PRESET_ENEMY_D:
            # 比较小的中型杂鱼敌机的预设
            self.context.textures = EnemyTexturesTable['ENEMY_D']
            self.context.explosion = ExplosionTable['MEDIUM_B']
            self.context.hitbox = [
                lib.sprite.Hitbox(pygame.Vector2(0, 5), 6),
                lib.sprite.Hitbox(pygame.Vector2(6, -2), 8),
                lib.sprite.Hitbox(pygame.Vector2(-6, -2), 8),
            ]
            self.context.debris = [
                (DebrisTable['DEBRIS_B'], pygame.Vector2(0, 5), .125, 1.75, 1, 3),
                (DebrisTable['DEBRIS_A'], pygame.Vector2(6, -2), .125, 1.75, 1, 3),
                (DebrisTable['DEBRIS_A'], pygame.Vector2(-6, -2), .125, 1.75, 1, 3),
            ]
            self.context.score = 200
            self.context.explodeSfx = lib.sound.sfx['EXPLODE_ENEMY_B']
        elif opcode == Opcode.PRESET_ENEMY_E:
            # 小型杂鱼敌机的预设
            self.context.textures = EnemyTexturesTable['ENEMY_E']
            self.context.explosion = ExplosionTable['SMALL_A']
            self.context.hitbox = [
                lib.sprite.Hitbox(pygame.Vector2(4, 0), 6),
                lib.sprite.Hitbox(pygame.Vector2(-4, 0), 6),
            ]
            self.context.debris = [
                (DebrisTable['DEBRIS_A'], pygame.Vector2(4, 0), .125, 1.75, .5, 2),
                (DebrisTable['DEBRIS_B'], pygame.Vector2(-4, 0), .125, 1.75, .5, 2),
            ]
            self.context.score = 100
            self.context.explodeSfx = lib.sound.sfx['EXPLODE_ENEMY_A']

        # elif opcode == Opcode.:
        #     params: tuple[] = params
        #      = params
        else:
            print('Unknown opcode:', opcode)
