import enum
import pygame
import random
import typing

import lib.globals
import lib.scene
import lib.sound
import lib.sprite
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
    JUMP_BOSS = enum.auto()
    JUMP_NOBOSS = enum.auto()

    STORE = enum.auto()
    RANDOM_INT = enum.auto()
    RANDOM_FLOAT = enum.auto()
    INC = enum.auto()
    DEC = enum.auto()
    ADD = enum.auto()
    SUB = enum.auto()
    MUL = enum.auto()
    DIV = enum.auto()
    MOD = enum.auto()
    FDIV = enum.auto()

    SET_SCROLL_SPEED = enum.auto()
    LOAD_STAGE = enum.auto()
    SPAWN = enum.auto()
    BGM = enum.auto()
    BOSS_WARNING = enum.auto()
    SET_CLEARED = enum.auto()
    SHOW_RESULT = enum.auto()

    # = enum.auto()

enemyScriptCache: dict[str, str] = {}

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

    def __init__(self, script: str) -> None:
        self.instruction = Engine.parseScript(script)
        self.pointer = 0
        self.wait = 0
        self.halted = False
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
                if value == '%PLAYER_X%':
                    result.append(lib.globals.groupPlayer.sprite.position.x)
                elif value == '%PLAYER_Y%':
                    result.append(lib.globals.groupPlayer.sprite.position.y)
                else:
                    result.append(value)
        return result

    def update(self):
        if self.wait > 0:
            self.wait -= 1

        while not self.halted and not self.wait:
            opcode, params = self.instruction[self.pointer]
            params = self.applyParamsReplacement(params)
            self.pointer += 1
            self.executeOpcode(opcode, params)

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
        elif opcode == Opcode.JUMP_BOSS:
            # 有BOSS时才跳转
            params: tuple[int] = params
            offset, = params

            if lib.globals.groupBoss.sprite:
                self.pointer += offset - 1
        elif opcode == Opcode.JUMP_NOBOSS:
            # 没有BOSS时才跳转
            params: tuple[int] = params
            offset, = params

            if not lib.globals.groupBoss.sprite:
                self.pointer += offset - 1
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
        elif opcode == Opcode.SET_SCROLL_SPEED:
            # 设置背景卷轴卷动的速度
            params: tuple[float] = params
            speed, = params

            lib.globals.backgroundScrollSpeed = speed
        elif opcode == Opcode.LOAD_STAGE:
            # 加载另一个关卡脚本，当前运行的这个脚本将会被替代
            params: tuple[str] = params
            scriptFile, = params

            self.halted = True
            with open(scriptFile, 'r', encoding='utf-8') as f:
                lib.globals.stageEngine = Engine(f.read())
        elif opcode == Opcode.SPAWN:
            # 在场景中刷出一个敌机，设置脚本和刷出位置
            # 对于所有的敌机，超过显示区域30px就会被清除
            # 显示区域是384x448，所以坐标范围就是(-30, -30)到(424, 478)
            params: tuple[float, float, float, str] = params
            x, y, angle, scriptFile = params

            enemy = lib.sprite.enemy.Enemy()
            enemy.position.update(x, y)
            enemy.angle = angle
            if scriptFile in enemyScriptCache:
                script = enemyScriptCache[scriptFile]
            else:
                with open(scriptFile, 'r', encoding='utf-8') as f:
                    script = f.read()
            enemy.setScript(script)
        elif opcode == Opcode.BGM:
            # 切换BGM，由两个部分组成
            # 先播放一遍A部分，之后循环播放B部分
            params: tuple[str] = params
            bgmName, = params

            lib.sound.playBgm(bgmName)
        elif opcode == Opcode.BOSS_WARNING:
            # 显示BOSS战的警告
            lib.globals.messageQueue.append(['WARNING!', 120])
            lib.globals.messageQueue.append(['Powerful enemy is approaching.\n                  Are you ready?', 300])
            lib.sound.sfx['BOSS_ALERT'].play(loops=1)
        elif opcode == Opcode.SET_CLEARED:
            # 将表示通关的全局变量设为True
            lib.globals.allCleared = True
        elif opcode == Opcode.SHOW_RESULT:
            # 结束游戏，跳转到结果画面
            pygame.mixer.music.stop()
            lib.globals.currentScene = lib.scene.Scene.RESULT

        # elif opcode == Opcode.:
        #     params: tuple[] = params
        #      = params
        else:
            print('Unknown opcode:', opcode)
