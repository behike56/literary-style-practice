#!/usr/bin/env python
import sys, os

def touchopen(filename, *args, **kwargs):
    """_summary_
        「2次記憶」としての中間ファイルを扱うユーティリティ関数
    Args:
        filename (_type_): _description_

    Returns:
        _type_: _description_
    """
    try:
        os.remove(filename)
    except OSError:
        pass

    open(filename, "a").close()

    return open(filename, *args, **kwargs)

data = []

# 前半
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
    data[2] = None
    data[3] = 0

    # 行中の文字ごとにループ
    for c in data[1][0]:
        if data[2] is None:
            if c.isalnum():
                data[2] = data[3]
        else:
            if not c.isalnum():
                data[4] = False
                data[5] = data[1][0][data[2]:data[3]].lower()

                # ストップワードと長さが２未満の単語は無視する。
                if len(data[5]) >= 2 and data[5] not in data[0]:
                    # 既出の単かを確認
                    while True:
                        data[6] = str(word_freqs.readline().strip(), 'utf-8')
                        if data[6] == '':
                            break;
                        data[7] = int(data[6].split(',')[1])

                        # 単語部分。空白は含めず。
                        data[6] = data[6].split(',')[0].strip()
                        if data[5] == data[6]:
                            data[7] += 1
                            data[4] = True
                            break
                    
                    if not data[4]:
                        word_freqs.seek(0, 1) # Windowsでは必要
                        word_freqs.write(bytes("%20s,%04d\n" % (data[5], 1), 'utf-8'))
                    else:
                        word_freqs.seek(-26, 1) # Windowsでは必要
                        word_freqs.write(bytes("%20s,%04d\n" % (data[5], data[7]), 'utf-8'))
                    
                    word_freqs.seek(0,0)
                data[2] = None
            data[3] += 1

# 入力ファイルの終わりに達したので、終了する。
f.close()
word_freqs.flush()

# 後半
# 続いて、頻出する25語を見つける
# ここまで使用したデータは不要なので一旦削除する
del data[:]

# 最初の25要素は、頻出25単語用に開けておく
data = data + [[]]*(25 - len(data))
data.append('') # data[25]は、ファイルに格納された単語、頻度の行
data.append(0) # data[26]は、頻度部分

# 2次記憶ファイルの行ごとにループ
while True:
    data[25] = str(word_freqs.readline().strip(), 'utf-8')
    if data[25] == '': # EoF
        break
    data[26] = int(data[25].split(',')[1])
    data[25] = data[25].split(',')[0].strip()

    for i in range(25):
        if data[i] == [] or data[i][1] < data[26]:
            data.insert(i, [data[25], data[26]])
            del data[26]
            break

for tf in data[0:25]:
    if len(tf) == 2:
        print(tf[0], '-', tf[1])

word_freqs.close()
