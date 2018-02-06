# --*-- coding:utf-8 --*--

from os.path import abspath, dirname
import os

cur = dirname(abspath(__file__))
parentdir = dirname(cur)
print parentdir

boson_1 = os.path.join(parentdir, "bason_cache", "11111")

print boson_1