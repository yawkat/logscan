#!/usr/bin/env python2

from util import *

files = sorted(filter(filename_pattern.match, os.listdir(indir)), key=filename_score)

last_time = 0
day = 0

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
                    day += 1
                last_time = time
            except ValueError:
                pass
            print str(day) + "\t" + line
