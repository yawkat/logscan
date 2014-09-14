#!/usr/bin/env python2

import re
import os

filename_pattern = re.compile(r"^proxy\.log\.\d+$")
first_line_pattern = re.compile(r"^\d\d:\d\d:\d\d \[INFO\] Using OpenSSL based native cipher\.$")
date_pattern = re.compile(r"^\d\d:\d\d:\d\d$")
date_pattern_length = 8
indir = "/home/yawkat/Development/Noxcrew/MinecraftStrike-Server/servers/bungee1000"
seek_step_size = 1024
target_offset = 0

def read_time(f):
    while True:
        line = f.readline()
        if date_pattern.match(line[:date_pattern_length]):
            h = int(line[0:2])
            m = int(line[3:5])
            s = int(line[6:8])
            return (h * 60 + m) * 60 + s
        f.seek(-len(line) - 1, 1)
        seek_to_line_start(f)

def seek_to_line_start(f):
    prev_step = 0
    step = 16
    while True:
        f.seek(-step, 1)
        section = f.read(step - prev_step)
        try:
            last_index = section.rfind("\n")
            if last_index is not -1:
                f.seek(last_index - len(section) + 1, 1)
                break
        except ValueError:
            pass
        prev_step = step
        step *= 2

def filename_score(f):
    index = int(f[10:])
    if index is 0:
        return -10000
    else:
        return -index
