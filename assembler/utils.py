#!/usr/bin/python3
# -*-coding:utf-8 -*-
# Reference:**********************************************
# @Time     : 2019/7/16 13:46
# @Author   : Raymond Luo
# @File     : utils.py
# @User     : luoli
# @Software: PyCharm
# Reference:**********************************************
import re
import os


def preprocess(file):
    '''
    去除注释，去除收尾空格和换行符
    :param file: raw file
    :return: file without comment
    '''
    pat = re.compile(r'#.*')
    new_file = re.sub(pat, "", file)
    lines = new_file.split("\n")
    new_line = []
    for i,line in enumerate(lines):
        line = line.strip()  # 去除收尾空格和换行符
        if not line:  # 跳过空行
            continue
        find_label = re.match(r'(\w+:)\s+(\w.*)', line)  # 防止标号和代码在一行
        if find_label and find_label.re.groups > 1:
            new_line.append(find_label.group(1))
            new_line.append(find_label.group(2))
        else:
            new_line.append(line)
    # lines = map(lambda line: line.strip(), lines)

    return new_line


def find_segment(line):
    '''
    find  segment
    :param line:
    :return:
    '''
    pat_data = re.compile(r'\.data', re.IGNORECASE)
    pat_text = re.compile(r"\.text", re.IGNORECASE)
    if re.match(pat_data, line):
        return "data"

    elif re.match(pat_text, line):
        return "text"


def save_file(data, code):
    if not os.path.exists("output"):
        os.mkdir("output")
    with open("output/dmem32.coe", 'w') as f:
        f.write("memory_initialization_radix = 16;\nmemory_initialization_vector =\n")
        for line in data:
            f.write(line + ',\n')
        for _ in range(16383 - len(data)):
            f.write("00000000" + ',\n')
        f.write("00000000" + ';\n')
    with open("output/prgmip32.coe", 'w') as f:
        f.write("memory_initialization_radix = 16;\nmemory_initialization_vector =\n")
        for line in code:
            f.write(line + ',\n')
        for _ in range(16383 - len(code)):
            f.write("00000000" + ',\n')
        f.write("00000000" + ';\n')
