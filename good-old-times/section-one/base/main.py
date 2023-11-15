#!/usr/bin/env python
import sys, os

def touchopen(filename, *args, **kwargs):

    try:
        os.remove(filename)
    except OSError:
        pass

    open(filename, "a").close()

    return open(filename, *args, **kwargs)

data = []

f = open('../stop_words.txt')
data = [f.read(1024).split(',')]
f.close()

data.append([])
data.append(None)
data.append(0)
data.append(False)
data.append('')
data.append('')
data.append(0)