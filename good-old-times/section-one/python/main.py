#!/usr/bin/env python
"""
Python 3.11.5で実装し直す。
問題1-1, 1-2, 1-3を適用する。
使用している変数は：
    data, word_freqs, c, i, tf
"""
import os
import sys


def touchopen(filename: str, *args, **kwargs):
    """_summary_

    Args:
        filename (str): _description_

    Returns:
        _type_: _description_
    """
    try:
        os.remove(filename)
    except OSError:
        pass

    open(filename, "a").close()

    return open(filename, *args, **kwargs)

# 初期化が不要
# data = []

# ##########################
# 前半
# ##########################
f = open('../stop_words.txt')
# data[0]　
# この変数を使い回してメモリの使用を制限する
data: list[list[str]] = [f.read(1024).split(',')]
f.close()

"""
以下の初期化のところは現状、# type: ignoreが必要になる。
"""

# data[1], 読み込んだ行
data.append([])
# data[2], 単語の最初の文字位置
data.append([None]) # type: ignore
# data[3], 行中で処理を行う文字の位置
data.append(0) # type: ignore
# data[4], 既出単語かを表すフラグ
data.append(False) # type: ignore
# data[5], 見つけた単語
data.append('') # type: ignore
# data[6], 中間ファイルから読み込んだ行で、単語、NNNNの形式をもつ
data.append('') # type: ignore
# data[7], その単語の頻度であるNNNN部分の整数値
data.append(0) # type: ignore

# ２次記憶をオープン
word_freqs = touchopen('word_freqs', 'rb+')

# 入力ファイルをオープン
f = open(sys.argv[1], 'r')

# 入力ファイルの行ごとにループ
while True:

    data[1] = [f.readline()]

    if data[1] == ['']:
        break

    if data[1][0][len(data[1][0])-1] != '\n':
        data[1][0] = data[1][0] + '\n'

    data[2] = None # type: ignore
    data[3] = 0 # type: ignore

    # 行中の1文字ごとにループ
    for c in data[1][0]:

        if data[2] is None:
            if c.isalnum():
                data[2] = data[3]

        else:
            if not c.isalnum():

                data[4] = False # type: ignore
                data[5] = data[1][0][data[2]:data[3]].lower()

                # ストップワードと長さが２未満の単語は無視する。
                if len(data[5]) >= 2 and data[5] not in data[0]:
                    # 既出の単語かを確認
                    while True:
                        data[6] = str(word_freqs.readline().strip(), 'utf-8') # type: ignore
                        if data[6] == '':
                            break;
                        data[7] = int(data[6].split(',')[1]) # type: ignore

                        # 単語部分。空白は含めず。
                        data[6] = data[6].split(',')[0].strip() # type: ignore
                        if data[5] == data[6]:
                            data[7] += 1 # type: ignore
                            data[4] = True # type: ignore
                            break

                    if not data[4]:
                        word_freqs.seek(0, 1) # Windowsでは必要
                        word_freqs.write(bytes("%20s,%04d\n" % (data[5], 1), 'utf-8'))

                    else:
                        word_freqs.seek(-26, 1) # Windowsでは必要
                        word_freqs.write(bytes("%20s,%04d\n" % (data[5], data[7]), 'utf-8'))

                    word_freqs.seek(0,0)

                data[2] = None # type: ignore

            data[3] += 1 # type: ignore

# 入力ファイルの終わりに達したので、終了する。
f.close()
word_freqs.flush()


# ##########################
# 後半
# ##########################
# 続いて、頻出する25語を見つける
# ここまで使用したデータは不要なので一旦削除する
del data[:]

# 最初の25要素は、頻出25単語用に開けておく
data = data + [[]]*(25 - len(data))
data.append('') # data[25]は、ファイルに格納された単語、頻度の行 # type: ignore
data.append(0) # data[26]は、頻度部分 # type: ignore

# 2次記憶ファイルの行ごとにループ
while True:
    data[25] = str(word_freqs.readline().strip(), 'utf-8') # type: ignore
    if data[25] == '': # EoF
        break
    data[26] = int(data[25].split(',')[1]) # type: ignore
    data[25] = data[25].split(',')[0].strip() # type: ignore

    for i in range(25):
        if data[i] == [] or data[i][1] < data[26]: # type: ignore
            data.insert(i, [data[25], data[26]]) # type: ignore
            del data[26]
            break

for tf in data[0:25]:
    if len(tf) == 2:
        print(tf[0], '-', tf[1])

word_freqs.close()
