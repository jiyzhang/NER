# -*- coding:utf-8 -*-

"""
2018-02-06
从BosonNLP的实体识别结果，反推出sentence,然后由
CoreNLP, HanLP, LTP, FoolNLTK, FNLP去做实体
识别，之后对比识别识别的异同
"""

import json
import demjson
import sys
import os
import string

path = os.path.dirname(__file__)
path = os.path.join(path, "boson_cache")

#print path
files = os.listdir("./boson_cache")

# for file in files:
#     print os.path.join(path, file)

phrases = ""

num = 0
#for file in files and i < 10:
phrase_num = len(files)
for i in range(phrase_num):
    file = files[i]
    #print file
    abs_file = os.path.join(path, file)
    json_text = ""
    try:
        with open(abs_file, "r") as f:
            json_text = f.read()
            if string.find(json_text, "isConvertError") != -1:
                print "Error: " + file + " " + "has isConvertError, ignored"
                continue
            elif string.find(json_text, "502 Bad Gateway") != -1:
                print "Error: " + file + " " + "502 Bad Gateway, ignored"
                continue
            elif string.find(json_text, "More than 5000 characters in some lines") != -1:
                print "Error: " + file + " " + "Error: More than 5000 characters in some lines, ignored"
                continue
            else:
                boson_json = demjson.decode(json_text, encoding="utf8")

                # words in unicode mode
                words = boson_json[0]["word"]

                phrase = file + "\t" + str(num) + "\t" + "".join(words)
                num = num + 1
    except Exception, e:
        print abs_file
        print e.message
    phrases = phrases + phrase + os.linesep #"\n"


phrases_utf8 = phrases.encode("utf-8")

with open("./boson_phrases.txt", "w") as f:
    f.write(phrases_utf8)
