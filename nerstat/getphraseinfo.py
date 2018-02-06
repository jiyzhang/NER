# -*- coding: utf-8 -*-

import json
import demjson
import numpy as np

if __name__ == "__main__":

    jsonObject = {}
    jsonObjArray  = []

    phrase_ids = ["1868", "1874", "1876", "1878", "1887"]

    #文件个数
    for i in range(1):
        print i
        # json_corenlp = demjson.decode_file("./" + "test_" + "corenlp_" + str(i) + ".json")
        # json_ltp     = demjson.decode_file("./" + "test_" + "ltp_"     + str(i) + ".json")
        # json_hanlp   = demjson.decode_file("./" + "test_" + "hanlp_"   + str(i) + ".json")

        json_corenlp = demjson.decode_file("./" + "corenlp_" + str(i) + ".json")
        json_ltp     = demjson.decode_file("./" + "ltp_"     + str(i) + ".json")
        json_hanlp   = demjson.decode_file("./" + "hanlp_"   + str(i) + ".json")

        # data array
        data_corenlp = json_corenlp["data"]
        data_ltp     = json_ltp["data"]
        data_hanlp   = json_hanlp["data"]

        number_of_phrase = len(data_ltp)

        for j in range(number_of_phrase):
            if data_corenlp[j]["phrase_id"] in phrase_ids:
                c_words    = data_corenlp[j]["corenlp"]["words"]
                c_ner_tags = data_corenlp[j]["corenlp"]["ner_tags"]
                c_offsets  = data_corenlp[j]["corenlp"]["char_offsets"]
                c_words_utf8 = [w.encode("utf-8") for w in c_words]
                c_offsets_str = [str(i) for i in c_offsets]

                l_words    = data_ltp[j]["ltp"]["words"]
                l_ner_tags = data_ltp[j]["ltp"]["ner_tags"]
                l_offsets  = data_ltp[j]["ltp"]["char_offsets"]
                l_words_utf8 = [w.encode("utf-8") for w in l_words]
                l_offsets_str = [str(i) for i in l_offsets]

                h_words    = data_hanlp[j]["hanlp"]["words"]
                h_ner_tags = data_hanlp[j]["hanlp"]["ner_tags"]
                h_offsets  = data_hanlp[j]["hanlp"]["char_offsets"]
                h_words_utf8 = [w.encode("utf-8") for w in h_words]
                h_offsets_str = [str(i) for i in h_offsets]

                print "*" * 20
                print "prhase id: " + data_corenlp[j]["phrase_id"]
                print "corenlp: "
                print ",".join(c_words_utf8)
                print ",".join(c_ner_tags)
                print ",".join(c_offsets_str)

                print "ltpp: "
                print ",".join(l_words_utf8)
                print ",".join(l_ner_tags)
                print ",".join(l_offsets_str)

                print "hanlp: "
                print ",".join(h_words_utf8)
                print ",".join(h_ner_tags)
                print ",".join(h_offsets_str)


