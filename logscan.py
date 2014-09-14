#!/usr/bin/env python2

from util import *

finish = False
last_time = 0xffffff
offset = 0
last_switch = None

for f in sorted(filter(filename_pattern.match, os.listdir(indir)), key=filename_score):
    ab = os.path.join(indir, f)
    with open(ab, "rb") as h:
        first_line = h.readline()[:-1]
        if first_line_pattern.match(first_line):
            finish = True
        h.seek(-1, 2)
        while True:
            pos = h.tell()
            if h.tell() < seek_step_size:
                break
            seek_to_line_start(h)
            time = read_time(h)
            if time > last_time:
                offset -= 1
                if offset <= target_offset:
                    print "Found date around byte %s in %s" % last_switch
                    finish = True
                    break
                last_switch = (pos, f)
            last_time = time
            h.seek(pos - seek_step_size, 0)
    if finish:
        break
