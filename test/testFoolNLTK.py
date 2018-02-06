# -*- coding: utf-8 -*-



import demjson
import numpy
import sys
import json

reload(sys)
sys.setdefaultencoding("utf-8")

for i in range(1):
    print(i)
    # json_corenlp = demjson.decode_file("./" + "test_" + "corenlp_" + str(i) + ".json")
    # json_ltp     = demjson.decode_file("./" + "test_" + "ltp_"     + str(i) + ".json")
    # json_hanlp   = demjson.decode_file("./" + "test_" + "hanlp_"   + str(i) + ".json")
    # with open("./fool_" + str(i) + ".json", 'r') as f:
    #     #str_fool = f.read()
    #     json_fool = json.load(f)

    json_fool     = demjson.decode_file("hanlp_" + str(i) + ".json")
    #json_fool = json.load(str_fool)
    # json_corenlp = demjson.decode_file("./" + "corenlp_" + str(i) + ".json")
    # json_ltp = demjson.decode_file("./" + "ltp_" + str(i) + ".json")
    # json_hanlp = demjson.decode_file("./" + "hanlp_" + str(i) + ".json")

    # data array
    # data_corenlp = json_corenlp["data"]
    # data_ltp = json_ltp["data"]
    # data_hanlp = json_hanlp["data"]

    data_fool = json_fool["data"]

    number_of_phrase = len(data_fool)

    for j in range(5):
        #foolnltk = data_fool[j]["foolnltk"]
        foolnltk = data_fool[j]["hanlp"]
        words = foolnltk["words"]
        # text = text.decode('string_escape', errors='ignore')
        #words_u = [i.encode("utf-8") for i in words]
        words_t = [type(i) for i in words]

        for w in words:
            print w.encode("utf-8")

        #print words
        #print words_u
        print(words_t)

    aaa = "\u8bc1\u5238".decode("unicode-escape")
    print(aaa)

# rimacpro:test richardz$ python test_foolnltk.py
# 0
# Traceback (most recent call last):
#   File "test_foolnltk.py", line 9, in <module>
#     json_fool     = demjson.decode("./foolnltk" + str(i) + ".json")
#   File "/Users/richardz/anaconda/lib/python2.7/site-packages/demjson.py", line 5701, in decode
#     return_stats=(return_stats or write_stats) )
#   File "/Users/richardz/anaconda/lib/python2.7/site-packages/demjson.py", line 4917, in decode
#     raise errors[0]
# demjson.JSONDecodeError: ('Bad number', u'.')