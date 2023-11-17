#!/usr/bin/env python

import os


def touchopen(filename: str, *args, **kwargs):
    try:
        os.remove(filename)
    except OSError:
        pass
    open(filename, "a").close()

    return open(filename, *args, **kwargs)

# 初期化が不要
# data = []

# 前半
f = open('../stop_words.txt')
# data[0]
data: list[list[str]] = [f.read(1024).split(',')]
f.close()

"""
以下の初期化のところは現状、# type: ignoreが必要になる。
"""
# data[1], 読み込んだ行
data.append([])
# data[2]
data.append(None) # type: ignore
# data[3]
data.append(0) # type: ignore
# data[4]
data.append()
# data[5]
data.append()
# data[6]
data.append()
# data[7]
data.append()
