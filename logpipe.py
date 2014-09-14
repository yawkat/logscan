#!/usr/bin/env python2

from util import *

last_time = 0xffffff
span_days = 0

files = sorted(filter(filename_pattern.match, os.listdir(indir)), key=filename_score)

for f in files:
    ab = os.path.join(indir, f)
    with open(ab, "rb") as h:
        first_line = h.readline()[:-1]
        h.seek(-1, 2)
        while True:
            pos = h.tell()
            if h.tell() < seek_step_size:
                break
            seek_to_line_start(h)
            time = read_time(h)
            if time > last_time:
                span_days += 1
            last_time = time
            h.seek(pos - seek_step_size, 0)
    if first_line_pattern.match(first_line):
        break

last_time = 0
day = span_days

for f in reversed(files):
    ab = os.path.join(indir, f)
    with open(ab, "r") as fh:
        while True:
            line = fh.readline()
            if line == "":
                break
            line = line[:-1]
            time = 0xffffff
            try:
                h = int(line[0:2])
                m = int(line[3:5])
                s = int(line[6:8])
                time = (h * 60 + m) * 60 + s
                if time < last_time:
                    day -= 1
                last_time = time
            except ValueError:
                pass
            print str(day) + "\t" + line
