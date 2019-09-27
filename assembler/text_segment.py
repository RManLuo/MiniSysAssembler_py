#!/usr/bin/python3
# -*-coding:utf-8 -*-
# Reference:**********************************************
# @Time     : 2019/7/16 15:15
# @Author   : Raymond Luo
# @File     : text_segment.py
# @User     : luoli
# @Software: PyCharm
# Reference:**********************************************
class Text():
    global_offset = 0

    def __init__(self, line, instruction, rs, rt, rd):
        self.line = line
        self.instruction = instruction.lower()  # 转成小写
        self.rs = rs
        self.rt = rt
        self.rd = rd
        self.address = Text.global_offset
        Text.global_offset += 4
