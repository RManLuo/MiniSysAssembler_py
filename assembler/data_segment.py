#!/usr/bin/python3
# -*-coding:utf-8 -*-
# Reference:**********************************************
# @Time     : 2019/7/16 14:38
# @Author   : Raymond Luo
# @File     : data_segment.py
# @User     : luoli
# @Software: PyCharm
# Reference:**********************************************
import re


class Data():
    global_offset = 0

    def __init__(self, line, name, type, data):
        self.line = line
        self.name = name
        self.type = type
        split_data = re.split(r"\s*,\s*", data)
        self.data = split_data
        self.address = Data.global_offset
        Data.global_offset = Data.global_offset + len(self.data) * 4  # 每个词占32位
