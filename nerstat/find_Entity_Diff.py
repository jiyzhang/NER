# -*- coding:utf-8 -*-

import sys
sys.path.append(".")

import nerstat
from nerstat import *
import demjson
import numpy as np
import json

def setupDic():
    dic1 = {}
    dic2 = {}

    with open("./boson_phrases.txt", "r") as f:
        lines = f.readlines()

    for line in lines:
        items = line.split("\t")
        if len(items) != 3:
            continue

        doc_id, phrase_id, text = line.split("\t")
        dic1[phrase_id] = doc_id
        dic2[phrase_id] = text

    return dic1, dic2

class find_entity_diff(object):

    def test1(self):
        # jsonObject = {}
        # jsonObjArray = []

        # create phrase_id <--> doc_id dictionary for look up doc_id by phrase_id
        # for boson NER
        myDocDic, myTextDic = setupDic()

        # 文件个数
        for i in range(1):  # there is only 1 file for boson
            # for i in range(22):
            print i

            json_corenlp = demjson.decode_file("./" + "corenlp_" + str(i) + ".json")
            json_ltp = demjson.decode_file("./" + "ltp_" + str(i) + ".json")
            json_hanlp = demjson.decode_file("./" + "hanlp_" + str(i) + ".json")
            json_fnlp = demjson.decode_file("./" + "fnlp_" + str(i) + ".json")
            json_fool = demjson.decode_file("./" + "foolnltk_" + str(i) + ".json")

            # data array
            data_corenlp = json_corenlp["data"]
            data_ltp = json_ltp["data"]
            data_hanlp = json_hanlp["data"]
            data_fnlp = json_fnlp["data"]
            data_fool = json_fool["data"]

            number_of_phrase = len(data_corenlp)

            for j in range(100):
            #for j in range(number_of_phrase):
                # for j in range(3):
                # 合并organization/personal/location, 获取entities
                print "No. " + str(j)
                corenlp_entities_info = nerstat.find_entity_info(data_corenlp[j], "corenlp")
                ltp_entities_info =     nerstat.find_entity_info(data_ltp[j], "ltp")
                hanlp_entities_info =   nerstat.find_entity_info(data_hanlp[j], "hanlp")
                fnlp_entities_info =    nerstat.find_entity_info(data_fnlp[j], "fnlp")
                fool_entities_info =    nerstat.find_foolnltk_entity(data_fool[j])

                # ltp: 1, corenlp: 2, hanlp 4, 根据sum来得知两两是否相同

                # 实体名、实体长度、实体起始位置
                # 1. 先比较三者的实体个数是否相等

                # 2. 实际比较
                # 2.1 PERSON 个数，有几个相同
                # 2.2 LOCATION 个数，有几个相同
                # 2.3 ORGANIZATION个数，有几个相同

                # 通过set的 &, in, not in来处理

                phrase_id = corenlp_entities_info["phrase_id"]

                # ----------------------------------------------------------
                doc_id = myDocDic[phrase_id]
                phrase = myTextDic[phrase_id]
                boson_entities_info = nerstat.find_boson_entity(doc_id, phrase_id)
                # ----------------------------------------------------------

                np_entity_corenlp = np.array(corenlp_entities_info["entity"])
                np_entity_ltp = np.array(ltp_entities_info["entity"])
                np_entity_hanlp = np.array(hanlp_entities_info["entity"])
                np_entity_fnlp = np.array(fnlp_entities_info["entity"])
                np_entity_fool = np.array(fool_entities_info["entity"])
                np_entity_boson = np.array(boson_entities_info["entity"])

                np_type_corenlp = np.array(corenlp_entities_info["entity_type"])
                np_type_ltp = np.array(ltp_entities_info["entity_type"])
                np_type_hanlp = np.array(hanlp_entities_info["entity_type"])
                np_type_fnlp = np.array(fnlp_entities_info["entity_type"])
                np_type_fool = np.array(fool_entities_info["entity_type"])
                np_type_boson = np.array(boson_entities_info["entity_type"])


                #phrase = "".join(np_entity_corenlp)

                #
                # # for the overlap of entity between corenlp, ltp and hanlp
                # np_startpos_corenlp = np.array(corenlp_entities_info["startpos"])
                # np_startpos_ltp = np.array(ltp_entities_info["startpos"])
                # np_startpos_hanlp = np.array(hanlp_entities_info["startpos"])
                # np_startpos_fnlp = np.array(fnlp_entities_info["startpos"])
                # np_startpos_fool = np.array(fool_entities_info["startpos"])
                # np_startpos_boson = np.array(boson_entities_info["startpos"])
                #
                # np_endpos_corenlp = np.array(corenlp_entities_info["endpos"])
                # np_endpos_ltp = np.array(ltp_entities_info["endpos"])
                # np_endpos_hanlp = np.array(hanlp_entities_info["endpos"])
                # np_endpos_fnlp = np.array(fnlp_entities_info["endpos"])
                # np_endpos_fool = np.array(fool_entities_info["endpos"])
                # np_endpos_boson = np.array(boson_entities_info["endpos"])
                #
                # np_entitylen_corenlp = np.array(corenlp_entities_info["entity_unicode_len"])
                # np_entitylen_ltp = np.array(ltp_entities_info["entity_unicode_len"])
                # np_entitylen_hanlp = np.array(hanlp_entities_info["entity_unicode_len"])
                # np_entitylen_fnlp = np.array(fnlp_entities_info["entity_unicode_len"])
                # np_entitylen_fool = np.array(fool_entities_info["entity_unicode_len"])
                # np_entitylen_boson = np.array(boson_entities_info["entity_unicode_len"])

            #     subJsonObject = {}
            #     subJsonObject["phrase_id"] = phrase_id
            #
            #     # 统计每个NER中PERSON、LOCATION, ORGANIZATION的个数
            #
                # for i in ["PERSON", "LOCATION", "ORGANIZATION"]:
                c_person_indexes =          find_all_index(np_type_corenlp, "PERSON")
                c_location_indexes =        find_all_index(np_type_corenlp, "LOCATION")
                c_organization_indexes =    find_all_index(np_type_corenlp, "ORGANIZATION")

                # # for detecting the overlap of entity between corenlp, ltp and hanlp
                c_person_list       = np_entity_corenlp[c_person_indexes]
                c_location_list     = np_entity_corenlp[c_location_indexes]
                c_organization_list = np_entity_corenlp[c_organization_indexes]

                # # set
                # c_person_set = set(np_entity_corenlp[c_person_indexes])
                # c_location_set = set(np_entity_corenlp[c_location_indexes])
                # c_organization_set = set(np_entity_corenlp[c_organization_indexes])

                # for i in ["PERSON", "LOCATION", "ORGANIZATION"]:
                l_person_indexes = find_all_index(np_type_ltp, "PERSON")
                l_location_indexes = find_all_index(np_type_ltp, "LOCATION")
                l_organization_indexes = find_all_index(np_type_ltp, "ORGANIZATION")

                l_person_list = np_entity_ltp[l_person_indexes]
                l_location_list = np_entity_ltp[l_location_indexes]
                l_organization_list = np_entity_ltp[l_organization_indexes]

                # for i in ["PERSON", "LOCATION", "ORGANIZATION"]:
                h_person_indexes = find_all_index(np_type_hanlp, "PERSON")
                h_location_indexes = find_all_index(np_type_hanlp, "LOCATION")
                h_organization_indexes = find_all_index(np_type_hanlp, "ORGANIZATION")

                h_person_list = np_entity_hanlp[h_person_indexes]
                h_location_list = np_entity_hanlp[h_location_indexes]
                h_organization_list = np_entity_hanlp[h_organization_indexes]

                # FNLP
                # for i in ["PERSON", "LOCATION", "ORGANIZATION"]:
                f_person_indexes = find_all_index(np_type_fnlp, "PERSON")
                f_location_indexes = find_all_index(np_type_fnlp, "LOCATION")
                f_organization_indexes = find_all_index(np_type_fnlp, "ORGANIZATION")

                f_person_list = np_entity_fnlp[f_person_indexes]
                f_location_list = np_entity_fnlp[f_location_indexes]
                f_organization_list = np_entity_fnlp[f_organization_indexes]

                # foolnltk
                # for i in ["PERSON", "LOCATION", "ORGANIZATION"]:
                o_person_indexes = find_all_index(np_type_fool, "PERSON")
                o_location_indexes = find_all_index(np_type_fool, "LOCATION")
                o_organization_indexes = find_all_index(np_type_fool, "ORGANIZATION")

                o_person_list = np_entity_fool[o_person_indexes]
                o_location_list = np_entity_fool[o_location_indexes]
                o_organization_list = np_entity_fool[o_organization_indexes]

                # boson_ner
                # for i in ["PERSON", "LOCATION", "ORGANIZATION"]:
                b_person_indexes = find_all_index(np_type_boson, "PERSON")
                b_location_indexes = find_all_index(np_type_boson, "LOCATION")
                b_organization_indexes = find_all_index(np_type_boson, "ORGANIZATION")

                b_person_list = np_entity_boson[b_person_indexes]
                b_location_list = np_entity_boson[b_location_indexes]
                b_organization_list = np_entity_boson[b_organization_indexes]

                print phrase
                print "corenlp"
                print " " + "person: ",
                for e in c_person_list:
                    print e,
                print ""
                print " " + "organization:",
                for e in c_organization_list:
                    print e,
                print ""

                print "ltp"
                print " " + "person: ",
                for e in l_person_list:
                    print e,
                print ""
                print " " + "organization:",
                for e in l_organization_list:
                    print e,
                print ""

                print "HanLP"
                print " " + "person: ",
                for e in h_person_list:
                    print e,
                print ""
                print " " + "organization:",
                for e in h_organization_list:
                    print e,
                print ""

                print "FNLP"
                print " " + "person: ",
                for e in f_person_list:
                    print e,
                print ""
                print " " + "organization:",
                for e in f_organization_list:
                    print e,
                print ""

                print "foolNLTK"
                print " " + "person: ",
                for e in o_person_list:
                    print e,
                print ""
                print " " + "organization:",
                for e in o_organization_list:
                    print e,
                print ""

                try:
                    print "BosonNER"
                    print " " + "person: ",
                    for e in b_person_list:
                        print e,
                    print ""
                    print " " + "organization:",
                    for e in b_organization_list:
                        print e,
                    print ""
                except UnicodeDecodeError, e:
                    print e.message()
            #
            #     corenlp_amount_stat = [len(c_person_indexes), len(c_location_indexes), len(c_organization_indexes)]
            #     ltp_amount_stat = [len(l_person_indexes), len(l_location_indexes), len(l_organization_indexes)]
            #     hanlp_amount_stat = [len(h_person_indexes), len(h_location_indexes), len(h_organization_indexes)]
            #     fnlp_amount_stat = [len(f_person_indexes), len(f_location_indexes), len(f_organization_indexes)]
            #     fool_amount_stat = [len(o_person_indexes), len(o_location_indexes), len(o_organization_indexes)]
            #     boson_amount_stat = [len(b_person_indexes), len(b_location_indexes), len(b_organization_indexes)]
            #
            #     # corenlp_amount_stat = [len(c_person_set), len(c_location_set), len(c_organization_set)]
            #     # ltp_amount_stat     = [len(l_person_set), len(l_location_set), len(l_organization_set)]
            #     # hanlp_amount_stat   = [len(h_person_set), len(h_location_set), len(h_organization_set)]
            #
            #     # ------------------------------------------------
            #     subJsonObject["corenlp"] = corenlp_amount_stat
            #     subJsonObject["ltp"] = ltp_amount_stat
            #     subJsonObject["hanlp"] = hanlp_amount_stat
            #     subJsonObject["fnlp"] = fnlp_amount_stat
            #     subJsonObject["fool"] = fool_amount_stat
            #     subJsonObject["boson"] = boson_amount_stat
            #     # ------------------------------------------------
            #     # 11
            #     # cl_person_set        = c_person_set & l_person_set
            #     # ch_person_set        = c_person_set & h_person_set
            #     # cf_person_set        = c_person_set & f_person_set
            #     # lh_person_set        = l_person_set & h_person_set
            #     # lf_person_set        = l_person_set & f_person_set
            #     # hf_person_set        = h_person_set & f_person_set
            #     # clh_person_set       = c_person_set & l_person_set & h_person_set
            #     # clf_person_set       = c_person_set & l_person_set & f_person_set
            #     # chf_person_set       = c_person_set & h_person_set & f_person_set
            #     # lhf_person_set       = l_person_set & h_person_set & f_person_set
            #     # clhf_person_set       = c_person_set & l_person_set & h_person_set & f_person_set
            #     #
            #     # cl_location_set = c_location_set & l_location_set
            #     # ch_location_set = c_location_set & h_location_set
            #     # cf_location_set = c_location_set & f_location_set
            #     # lh_location_set = l_location_set & h_location_set
            #     # lf_location_set = l_location_set & f_location_set
            #     # hf_location_set = h_location_set & f_location_set
            #     # clh_location_set = c_location_set & l_location_set & h_location_set
            #     # clf_location_set = c_location_set & l_location_set & f_location_set
            #     # chf_location_set = c_location_set & h_location_set & f_location_set
            #     # lhf_location_set = l_location_set & h_location_set & f_location_set
            #     # clhf_location_set = c_location_set & l_location_set & h_location_set & f_location_set
            #     #
            #     # cl_organization_set = c_organization_set & l_organization_set
            #     # ch_organization_set = c_organization_set & h_organization_set
            #     # cf_organization_set = c_organization_set & f_organization_set
            #     # lh_organization_set = l_organization_set & h_organization_set
            #     # lf_organization_set = l_organization_set & f_organization_set
            #     # hf_organization_set = h_organization_set & f_organization_set
            #     # clh_organization_set = c_organization_set & l_organization_set & h_organization_set
            #     # clf_organization_set = c_organization_set & l_organization_set & f_organization_set
            #     # chf_organization_set = c_organization_set & h_organization_set & f_organization_set
            #     # lhf_organization_set = l_organization_set & h_organization_set & f_organization_set
            #     # clhf_organization_set = c_organization_set & l_organization_set & h_organization_set & f_organization_set
            #     #
            #     #
            #     # cl  = [len(cl_person_set),  len(cl_location_set),  len(cl_organization_set)]
            #     # ch  = [len(ch_person_set),  len(ch_location_set),  len(ch_organization_set)]
            #     # cf  = [len(cf_person_set),  len(cf_location_set),  len(cf_organization_set)]
            #     # lh  = [len(lh_person_set),  len(lh_location_set),  len(lh_organization_set)]
            #     # lf  = [len(lf_person_set),  len(lf_location_set),  len(lf_organization_set)]
            #     # hf  = [len(hf_person_set),  len(hf_location_set),  len(hf_organization_set)]
            #     # clh = [len(clh_person_set), len(clh_location_set), len(clh_organization_set)]
            #     # clf = [len(clf_person_set), len(clf_location_set), len(clf_organization_set)]
            #     # chf = [len(chf_person_set), len(chf_location_set), len(chf_organization_set)]
            #     # lhf = [len(lhf_person_set), len(lhf_location_set), len(lhf_organization_set)]
            #     # clhf = [len(clhf_person_set), len(clhf_location_set), len(clhf_organization_set)]
            #     #
            #     #
            #     #
            #     # # ------------------------------------------------
            #     # subJsonObject["cl"  ] =  cl
            #     # subJsonObject["ch"  ] =  ch
            #     # subJsonObject["cf"  ] =  cf
            #     # subJsonObject["lh"  ] =  lh
            #     # subJsonObject["lf"  ] =  lf
            #     # subJsonObject["hf"  ] =  hf
            #     # subJsonObject["clh" ] =  clh
            #     # subJsonObject["clf" ] =  clf
            #     # subJsonObject["chf" ] =  chf
            #     # subJsonObject["lhf" ] =  lhf
            #     # subJsonObject["clhf"] =  clhf
            #     # # ------------------------------------------------
            #     #
            #     # # for overlap inforamtion
            #     # cl_overlapped = find_overlaps(corenlp_entities_info, c_person_indexes, c_location_indexes, c_organization_indexes,
            #     #                               ltp_entities_info, l_person_indexes, l_location_indexes, l_organization_indexes)
            #     #
            #     # ch_overlapped = find_overlaps(corenlp_entities_info, c_person_indexes, c_location_indexes, c_organization_indexes,
            #     #                               hanlp_entities_info, h_person_indexes, h_location_indexes, h_organization_indexes)
            #     #
            #     # cf_overlapped = find_overlaps(corenlp_entities_info, c_person_indexes, c_location_indexes, c_organization_indexes,
            #     #                               fnlp_entities_info, f_person_indexes, f_location_indexes, f_organization_indexes)
            #     #
            #     # lh_overlapped = find_overlaps(ltp_entities_info, l_person_indexes, l_location_indexes, l_organization_indexes,
            #     #                               hanlp_entities_info, h_person_indexes, h_location_indexes, h_organization_indexes)
            #     #
            #     # lf_overlapped = find_overlaps(ltp_entities_info, l_person_indexes, l_location_indexes, l_organization_indexes,
            #     #                               fnlp_entities_info, f_person_indexes, f_location_indexes, f_organization_indexes)
            #     #
            #     # hf_overlapped = find_overlaps(hanlp_entities_info, h_person_indexes, h_location_indexes, h_organization_indexes,
            #     #                               fnlp_entities_info, f_person_indexes, f_location_indexes, f_organization_indexes)
            #     #
            #     # # ------------------------------------------------
            #     # subJsonObject["cl_overlapped"] = cl_overlapped
            #     # subJsonObject["ch_overlapped"] = ch_overlapped
            #     # subJsonObject["cf_overlapped"] = cf_overlapped
            #     # subJsonObject["lh_overlapped"] = lh_overlapped
            #     # subJsonObject["lf_overlapped"] = lf_overlapped
            #     # subJsonObject["hf_overlapped"] = hf_overlapped
            #     # #subJsonObject["clh"] = clh
            #     # # ------------------------------------------------
            #
            #     bc_person_set = b_person_set & c_person_set
            #     bl_person_set = b_person_set & l_person_set
            #     bh_person_set = b_person_set & h_person_set
            #     bf_person_set = b_person_set & f_person_set
            #     bo_person_set = b_person_set & h_person_set
            #
            #     bc_location_set = b_location_set & c_location_set
            #     bl_location_set = b_location_set & l_location_set
            #     bh_location_set = b_location_set & h_location_set
            #     bf_location_set = b_location_set & f_location_set
            #     bo_location_set = b_location_set & h_location_set
            #
            #     bc_organization_set = b_organization_set & c_organization_set
            #     bl_organization_set = b_organization_set & l_organization_set
            #     bh_organization_set = b_organization_set & h_organization_set
            #     bf_organization_set = b_organization_set & f_organization_set
            #     bo_organization_set = b_organization_set & h_organization_set
            #
            #     bc = [len(bc_person_set), len(bc_location_set), len(bc_organization_set)]
            #     bl = [len(bl_person_set), len(bl_location_set), len(bl_organization_set)]
            #     bh = [len(bh_person_set), len(bh_location_set), len(bh_organization_set)]
            #     bf = [len(bf_person_set), len(bf_location_set), len(bf_organization_set)]
            #     bo = [len(bo_person_set), len(bo_location_set), len(bo_organization_set)]
            #
            #     # ------------------------------------------------
            #     subJsonObject["bc"] = bc
            #     subJsonObject["bl"] = bl
            #     subJsonObject["bh"] = bh
            #     subJsonObject["bf"] = bf
            #     subJsonObject["bo"] = bo
            #     # ------------------------------------------------
            #
            #     # for overlap inforamtion
            #
            #     bc_overlapped = find_overlaps(boson_entities_info, b_person_indexes, b_location_indexes,
            #                                   b_organization_indexes,
            #                                   corenlp_entities_info, c_person_indexes, c_location_indexes,
            #                                   c_organization_indexes)
            #
            #     bl_overlapped = find_overlaps(boson_entities_info, b_person_indexes, b_location_indexes,
            #                                   b_organization_indexes,
            #                                   ltp_entities_info, l_person_indexes, l_location_indexes,
            #                                   l_organization_indexes)
            #
            #     bh_overlapped = find_overlaps(boson_entities_info, b_person_indexes, b_location_indexes,
            #                                   b_organization_indexes,
            #                                   hanlp_entities_info, h_person_indexes, h_location_indexes,
            #                                   h_organization_indexes)
            #
            #     bf_overlapped = find_overlaps(boson_entities_info, b_person_indexes, b_location_indexes,
            #                                   b_organization_indexes,
            #                                   fnlp_entities_info, f_person_indexes, f_location_indexes,
            #                                   f_organization_indexes)
            #
            #     bo_overlapped = find_overlaps(boson_entities_info, b_person_indexes, b_location_indexes,
            #                                   b_organization_indexes,
            #                                   fool_entities_info, o_person_indexes, o_location_indexes,
            #                                   o_organization_indexes)
            #
            #     # ------------------------------------------------
            #     subJsonObject["bc_overlapped"] = bc_overlapped
            #     subJsonObject["bl_overlapped"] = bl_overlapped
            #     subJsonObject["bh_overlapped"] = bh_overlapped
            #     subJsonObject["bf_overlapped"] = bf_overlapped
            #     subJsonObject["bo_overlapped"] = bo_overlapped
            #     # subJsonObject["clh"] = clh
            #     # ------------------------------------------------
            #
            #     jsonObjArray.append(subJsonObject)
            #
            # jsonObject["stats"] = jsonObjArray
            # #
            # print "*" * 20
            # print "writing to : o_" + str(i) + ".json"
            #
            # # demjson.encode_to_file("./" + str(i) + ".json", encoding="utf-8")
            #
            # with open("o_" + str(i) + ".json", "w") as fp:
            #     json.dump(jsonObject, fp)
            # print "done."

if __name__ == '__main__':
    obj = find_entity_diff()
    obj.test1()