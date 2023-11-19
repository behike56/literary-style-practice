#!/usr/bin/env python

data: list[list[str]] = []

data.append(["I", "and", "for"])
data.append(["ABC", "E", "fgHIJKlmn"])

while True:
    print(data[1][0])
    break

for c in data[1][0]:
    print(c)

data[1][0][0]