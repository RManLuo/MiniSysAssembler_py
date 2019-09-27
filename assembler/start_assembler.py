#!/usr/bin/python3
# -*-coding:utf-8 -*-
# Reference:**********************************************
# @Time     : 2019/7/16 13:39
# @Author   : Raymond Luo
# @File     : start_assembler.py
# @User     : luoli
# @Software: PyCharm
# Reference:**********************************************
import re
from .utils import preprocess, find_segment
from .data_segment import Data
from .text_segment import Text
from .instruct_analysis import analysis
from .utils import save_file


def do_assembler(path):
    '''

    :param path: assembler file path
    :return:
    '''
    with open(path, encoding='utf-8') as f:
        file = f.read()
    lines = preprocess(file)

    data_dict = {}
    code_dict = {}
    label_dict = {}
    for index, line in enumerate(lines):
        seg_label = find_segment(line)
        if seg_label == "data":  # 第一次找到data
            state = "data"
            continue
        elif seg_label == "text":  # 第一找到text段
            state = "text"
            continue
        if state == "data":
            search_data = re.match(r"(\w+):\s+\.(\w+)\s+(.+)", line)
            tmp_data = Data(index, search_data.group(1), search_data.group(2), search_data.group(3))
            data_dict[tmp_data.name] = tmp_data  # 记录名字对应的数据
        elif state == "text":
            # pat_lable = re.compile(r'.+:')
            find_label = re.match(r'(\w+):', line)
            if find_label:
                label_name = find_label.group(1)  # 去掉冒号
            else:
                tmp_line = line.split(" ")  # 以空格分隔
                instruct = tmp_line[0]  # instruct
                tmp_line = re.split(r"\s*,\s*", "".join(tmp_line[1:]))  # 取操作数)
                # tmp_line = "".join(tmp_line[1:])  # 取操作数
                # tmp_line = tmp_line.split(",")  # 逗号区分操作数
                # tmp_line = list(map(lambda x: x.strip(), tmp_line))  # 去除首尾空格
                if 3 - len(tmp_line) > 0:  # 补充够三个操作数
                    t = [None for _ in range(3 - len(tmp_line))]
                    tmp_line.extend(t)
                tmp_text = Text(index, instruct, tmp_line[0], tmp_line[1], tmp_line[2])
                code_dict[tmp_text.address] = tmp_text  # 记录对应offset对应的指令
                if label_name:  # 如果有label
                    label_dict[label_name] = tmp_text.address  # 给label一个跳转
                    label_name = None
    # print(data_dict)
    # print(code_dict)
    # print(label_dict)
    # with open("assembler/prgmie_true") as f:
    #     right_code = f.readlines()
    #
    # with open("dmem32.coe") as f:
    #     right_data = f.readlines()
    code_list = []
    data_list = []
    # index = 0
    for offset in code_dict:
        machine_code = analysis(code_dict[offset], data_dict, label_dict)
        custom = "{:0>8x}".format(int(machine_code, 2))
        # 验证用的
        # if custom != right_code[index].strip("\n"):
        #     print(index)
        #     print(custom)
        #     print(right_code[index].strip("\n"))
        #     print(code_dict[offset].line, code_dict[offset].instruction, code_dict[offset].rs, code_dict[offset].rt,
        #           code_dict[offset].rd)
        # index += 1
        code_list.append(custom)
    # index = 0
    for offset in data_dict:
        for data in data_dict[offset].data:
            data = "{:0>8x}".format(int(data, 0))
            # 验证用的
            # if data != right_data[index].strip("\n"):
            #     print(index)
            #     print(data)
            #     print(right_data[index].strip("\n"))
            data_list.append(data)
            # index += 1
    # for index, code in enumerate(code_list):
    save_file(data_list, code_list)
