#!/usr/bin/python3
# -*-coding:utf-8 -*-
# Reference:**********************************************
# @Time     : 2019/7/17 11:09
# @Author   : Raymond Luo
# @File     : instruct_analysis.py
# @User     : luoli
# @Software: PyCharm
# Reference:**********************************************
from copy import copy
import re
from copy import deepcopy


class R_instruction():
    def __init__(self, op=None, rs=None, rt=None, rd=None, shamt=None, func=None):
        self.op = op
        self.rs = rs
        self.rt = rt
        self.rd = rd
        self.shamt = shamt
        self.func = func

    def generate_machine_code(self):
        machine_code = "{:0>6b}{:0>5b}{:0>5b}{:0>5b}{:0>5b}{:0>6b}".format(self.op, self.rs, self.rt, self.rd,
                                                                           self.shamt, self.func)
        return machine_code


class I_instruction():
    def __init__(self, op=None, rs=None, rt=None, immediate=None):
        self.op = op
        self.rs = rs
        self.rt = rt
        self.immediate = immediate

    def generate_machine_code(self):
        if self.immediate < 0:  # 出现负跳转
            def negative2bin16(i):
                return (bin(((1 << 16) - 1) & i)[2:]).zfill(16)

            machine_code = "{:0>6b}{:0>5b}{:0>5b}{}".format(self.op, self.rs, self.rt,
                                                                  negative2bin16(self.immediate))  # 暴力转换成源码表示负数
        else:
            machine_code = "{:0>6b}{:0>5b}{:0>5b}{:0>16b}".format(self.op, self.rs, self.rt, self.immediate)
        return machine_code


class J_instruction():
    def __init__(self, op=None, address=None):
        self.op = op
        self.address = address

    def generate_machine_code(self):
        machine_code = "{:0>6b}{:0>26b}".format(self.op, self.address)
        return machine_code


R_instruction_dict = {
    "add": R_instruction(op=0b000000, shamt=0b00000, func=0b100000),
    "addu": R_instruction(op=0b000000, shamt=0b00000, func=0b100001),
    "sub": R_instruction(op=0b000000, shamt=0b00000, func=0b100010),
    "subu": R_instruction(op=0b000000, shamt=0b00000, func=0b100011),
    "and": R_instruction(op=0b000000, shamt=0b00000, func=0b100100),
    "or": R_instruction(op=0b000000, shamt=0b00000, func=0b100101),
    "xor": R_instruction(op=0b000000, shamt=0b00000, func=0b100110),
    "nor": R_instruction(op=0b000000, shamt=0b00000, func=0b100111),
    "slt": R_instruction(op=0b000000, shamt=0b00000, func=0b100111),
    "sltu": R_instruction(op=0b000000, shamt=0b00000, func=0b101011),
    "sll": R_instruction(op=0b000000, rs=0b00000, func=0b000000),
    "srl": R_instruction(op=0b000000, rs=0b00000, func=0b000010),
    "sra": R_instruction(op=0b000000, rs=0b00000, func=0b000011),
    "sllv": R_instruction(op=0b000000, shamt=0b00000, func=0b000100),
    "srlv": R_instruction(op=0b000000, shamt=0b00000, func=0b000110),
    "srav": R_instruction(op=0b000000, shamt=0b00000, func=0b000111),
    "jr": R_instruction(op=0b000000, rt=0b00000, rd=0b00000, shamt=0b00000, func=0b001000)
}

I_instruction_dict = {
    "addi": I_instruction(op=0b001000),
    "addiu": I_instruction(op=0b001001),
    "andi": I_instruction(op=0b001100),
    "ori": I_instruction(op=0b001101),
    "xori": I_instruction(op=0b001110),
    "lui": I_instruction(op=0b001111, rs=0b00000),
    "lw": I_instruction(op=0b100011),
    "sw": I_instruction(op=0b101011),
    "beq": I_instruction(op=0b000100),
    "bne": I_instruction(op=0b000101),
    "slti": I_instruction(op=0b001010),
    "sltiu": I_instruction(op=0b001011),
}

J_instruction_dict = {
    "j": J_instruction(op=0b000010),
    "jal": J_instruction(op=0b000011)
}

Register_dict = {
    "$zero": 0,
    "$at": 1,
    "$v0": 2,
    "$v1": 3,
    "$a0": 4,
    "$a1": 5,
    "$a2": 6,
    "$a3": 7,
    "$t0": 8,
    "$t1": 9,
    "$t2": 10,
    "$t3": 11,
    "$t4": 12,
    "$t5": 13,
    "$t6": 14,
    "$t7": 16,
    "$s0": 16,
    "$s1": 17,
    "$s2": 18,
    "$s3": 19,
    "$s4": 20,
    "$s5": 21,
    "$s6": 22,
    "$s7": 23,
    "$t8": 24,
    "$t9": 25,
    "$i0": 26,
    "$i1": 27,
    "$gp": 28,
    "$28": 28,
    "$sp": 29,
    "$s8": 30,
    "$ra": 31,
}


def analysis(code, data_dict, label_dict):
    '''
    把指令翻译成机器码
    :param code: 汇编语言
           data dict:数据段
           label dict:代码段
    :return: 机器码
    '''
    instruction = code.instruction
    # 三个操作数对应的情况
    if instruction in ['add', 'addu', 'sub', 'subu', 'and', 'or', 'xor', 'slt', 'sltu', 'sllv', 'srlv', 'srav']:
        option = deepcopy(R_instruction_dict[instruction])  # 拷贝，不修改dict的模板
        option.rs = Register_dict[code.rs]
        option.rt = Register_dict[code.rt]
        option.rd = Register_dict[code.rd]
    elif instruction in ['sll', 'srl', 'sra']:
        option = deepcopy(R_instruction_dict[instruction])  # 拷贝，不修改dict的模板
        option.rt = Register_dict[code.rs]
        option.rd = Register_dict[code.rt]
        option.shamt = int(code.rd, 0)
    elif instruction in ['jr']:
        option = deepcopy(R_instruction_dict[instruction])  # 拷贝，不修改dict的模板
        option.rs = Register_dict[code.rs]
    # 直接输入立即数情况
    elif instruction in ['addi', 'addiu', 'andi', 'ori', 'xori']:
        option = deepcopy(I_instruction_dict[instruction])  # 拷贝，不修改dict的模板
        option.rs = Register_dict[code.rt]
        option.rt = Register_dict[code.rs]
        option.immediate = int(code.rd, 0)
    elif instruction in 'lui':
        option = deepcopy(I_instruction_dict[instruction])  # 拷贝，不修改dict的模板
        option.rt = Register_dict[code.rs]
        option.immediate = int(code.rt, 0)
    # 涉及到data段
    elif instruction in ['lw', 'sw']:
        option = deepcopy(I_instruction_dict[instruction])  # 拷贝，不修改dict的模板
        option.rt = Register_dict[code.rs]  # 第一个操作数
        rt = code.rt  # lw $s1,0xc60($s5) or LED($s6)
        option.rs = Register_dict[re.findall(r'[(](.*?)[)]', rt)[0]]  # rs= $s5
        tmp_offset = re.findall(r'^(.*?)[(]', rt)[0]
        if tmp_offset in data_dict:  # offset是在地址段
            offset = data_dict[tmp_offset].address
        else:  # offset是一个直接的数字
            offset = int(tmp_offset, 0)
        option.immediate = offset
    elif instruction in ['beq', 'bne']:
        option = deepcopy(I_instruction_dict[instruction])  # 拷贝，不修改dict的模板
        option.rs = Register_dict[code.rs]  # 第一个操作数
        option.rt = Register_dict[code.rt]  # 第二个操作数
        tmp_offset = code.rd  # 第三个操作数
        if tmp_offset in label_dict:  # offset是在地址段
            label_address = label_dict[tmp_offset]
            instruction_address = code.address
            offset = (label_address - instruction_address) // 4 - 1
        else:  # offset是一个直接的数字
            offset = int(tmp_offset, 0)
        option.immediate = offset
    elif instruction in ['slti', 'sltiu']:
        option = deepcopy(I_instruction_dict[instruction])  # 拷贝，不修改dict的模板
        option.rs = Register_dict[code.rt]  # 第二个操作数
        option.rt = Register_dict[code.rs]  # 第一个操作数
        option.immediate = int(code.rd, 0)  # 第三个操作数
    elif instruction in ['j', 'jal']:
        option = deepcopy(J_instruction_dict[instruction])  # 拷贝，不修改dict的模板
        adr = code.rs
        if adr in label_dict:
            addr = label_dict[adr] // 4
        else:
            addr = int(adr, 0)
        option.address = addr
    machine_code = option.generate_machine_code()
    return machine_code
