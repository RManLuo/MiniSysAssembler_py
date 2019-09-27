#!/usr/bin/python3
# -*-coding:utf-8 -*-
# Reference:**********************************************
# @Time     : 2019/7/16 13:27
# @Author   : Raymond Luo
# @File     : Assembler.py
# @User     : luoli
# @Software: PyCharm
# Reference:**********************************************
import argparse
from assembler.start_assembler import do_assembler
parser = argparse.ArgumentParser()
parser.add_argument('path', type=str, help='Input the file path')
args = parser.parse_args()


if __name__ == "__main__":
    filepath = args.path
    print(filepath)
    do_assembler(filepath)
