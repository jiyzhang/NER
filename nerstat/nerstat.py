# -*- coding: utf-8 -*-

import json
import demjson
import numpy as np
from os.path import abspath, dirname
import os

def find_all_index(arr,item):
    return [i for i,a in enumerate(arr) if a==item]


''''' 
求两个字符串的最长公共子串 
思想：建立一个二维数组，保存连续位相同与否的状态 
'''
def getMaximumCommonSubstr(str1, str2):

    if not isinstance(str1, unicode):
        str1 = str1.decode("utf-8")

    if not isinstance(str2, unicode):
        str2 = str2.decode("utf-8")

    lstr1 = len(str1)
    lstr2 = len(str2)
    record = [[0 for i in range(lstr2 + 1)] for j in range(lstr1 + 1)]  # 多一位
    maxNum = 0  # 最长匹配长度
    p = 0  # 匹配的起始位

    for i in range(lstr1):
        for j in range(lstr2):
            if str1[i] == str2[j]:
                # 相同则累加
                record[i + 1][j + 1] = record[i][j] + 1
                if record[i + 1][j + 1] > maxNum:
                    # 获取最大匹配长度
                    maxNum = record[i + 1][j + 1]
                    # 记录最大匹配长度的终止位置
                    p = i + 1
    maxsubstr = str1[p - maxNum:p]
    maxsubstr = maxsubstr.encode("utf-8")
    return maxsubstr, maxNum

# 识别entity, 位置，以及长度
# 需要合并多个Org/Person/Loc
# ner_name: "corenlp", "ltp", "hanlp"
# 对长度的计算，要改为unicode后再计算

# """
# 证券_代码_：_601888_股票_简称_：_中国_国旅_公告_编号_：_临_2013-022
# [0, 2, 4, 5, 23, 25, 27, 28, 30, 37, 39, 41, 42, 43]
#
# 中国_国旅_股份_有限_公司
# [0, 2, 4, 6, 8]
#
# CoreNLP对长度的计算，在中文英文数字混合的模式不正确
#
# 另外，对于英文，因为存在单词之间的空格，用offset相减的方式也不正确
# """
# 关注entities和entity_unicode_len即可

# input: myentity
# json["data"]

# ------2018-01-31---------
# 201608@2016_2016-08-22_1471854646_237857 证券代码：835875证券简称：天基新材主办券商：国泰君安 北京天基新材料股份有限公司股权质押公告 本公司及董事会全体成员保证公告内容的真实、准确和完整
# "国泰君安", "北京", "天基", "新", "材料", "股份", "有限", "公司"
# "ORGANIZATION", "ORGANIZATION", "ORGANIZATION", "ORGANIZATION", "ORGANIZATION", "ORGANIZATION", "ORGANIZATION", "ORGANIZATION"
# 66, 71, 73, 75, 76, 78, 80, 82

# 国泰君安北京天基新材料股份有限公司,ORGANIZATION,66,83,17

#国泰君安 和 北京天基新材料股份有限公司 之前存在空格，是两个实体
# 66 + 4 != 71, 所以不能把两个实体拼接在一起
# ------2018-01-31---------

def find_entity_info(myentity, ner_name):
    phrase_id = myentity["phrase_id"]
    nerObject = myentity[ner_name]

    words      = nerObject["words"]
    ner_tags   = nerObject["ner_tags"]
    offsets    = nerObject["char_offsets"]
    print "#######################"
    print phrase_id
    print "#######################"
    words_utf8 = [w.encode("utf-8") for w in words]
    offsets = [int(i) for i in offsets]

    # print "_".join(words_utf8)
    # print offsets



    num_segments = len(ner_tags)

    entities   = []
    startpos   = []
    endpos     = []
    entity_len = []
    entity_type = []
    entity_unicode_len = []

    entity_index = 0

    new_entity_flag = False
    previous_tag = "O"

    for i in range(num_segments):
        if ner_tags[i] not in ["LOCATION", "PERSON", "ORGANIZATION"]:
            if new_entity_flag == False:
                continue
            else:
                # complete the previous entity
                #endpos.append(offsets[i] - 1)
                endpos.append(end_pos_tmp)
                entity_len.append(offsets[i] - startpos[entity_index]) ## error
                new_entity_flag = False
                unicode_len = len(entities[entity_index].decode("utf-8"))
                entity_unicode_len.append(unicode_len)
                entity_index = entity_index + 1
        else:
        #if ner_tags[i] in ["LOCATION", "PERSON", "ORGANIZATION"]:
            if new_entity_flag == False:
                previous_tag = ner_tags[i]
                new_entity_flag = True

                entities.append(words_utf8[i])
                entity_type.append(ner_tags[i])
                startpos.append(offsets[i])

                unicode_len_tmp = len(words_utf8[i].decode("utf-8"))
                end_pos_tmp = offsets[i] + unicode_len_tmp - 1

            else:
                if ner_tags[i] == previous_tag and end_pos_tmp + 1 == offsets[i]: #而且相邻
                    # merge
                    entities[entity_index] += words_utf8[i]
                    previous_tag = ner_tags[i]

                    unicode_len_tmp = len(words_utf8[i].decode("utf-8"))
                    end_pos_tmp = offsets[i] + unicode_len_tmp - 1

                else:   # new entities
                    # complete the previous entity
                    #endpos.append(offsets[i] - 1)
                    endpos.append(end_pos_tmp)
                    entity_len.append(offsets[i] - startpos[entity_index])  ## error

                    unicode_len = len(entities[entity_index].decode("utf-8"))
                    entity_unicode_len.append(unicode_len)

                    new_entity_flag = True
                    entity_index = entity_index + 1

                    previous_tag = ner_tags[i]

                    entities.append(words_utf8[i])
                    entity_type.append(ner_tags[i])
                    startpos.append(offsets[i])

                    unicode_len_tmp = len(words_utf8[i].decode("utf-8"))
                    end_pos_tmp = offsets[i] + unicode_len_tmp - 1

    #end
    if new_entity_flag == True:
        endpos.append(offsets[num_segments - 1] + len(words_utf8[num_segments - 1].decode("utf-8")) -1)
        entity_len.append(offsets[num_segments - 1] + len(words_utf8[num_segments - 1].decode("utf-8")) - startpos[entity_index])

        unicode_len = len(entities[entity_index].decode("utf-8"))
        entity_unicode_len.append(unicode_len)
        new_entity_flag = False

    d = {}
    d["phrase_id"]  = phrase_id
    d["entity"]     = entities
    d["entity_type"]= entity_type
    d["entity_len"] = entity_len
    d["entity_unicode_len"] = entity_unicode_len
    d["startpos"]   = startpos
    d["endpos"]     = endpos

    return d

# myentity: data_fool[j]
def find_foolnltk_entity(myentity):
    phrase_id = myentity["phrase_id"]
    nerObject = myentity["foolnltk"]

    words      = nerObject["words"]
    ner_tags   = nerObject["ner_tags"]
    offsets    = nerObject["char_offsets"]

    words_utf8 = [w.encode("utf-8") for w in words]
    offsets = [int(i) for i in offsets]

    num_segments = len(ner_tags)

    entities   = []
    startpos   = []
    endpos     = []
    entity_len = []
    entity_type = []
    entity_unicode_len = []

    entity_index = 0

    for i in range(num_segments):
        entities.append(words_utf8[i])
        startpos.append(offsets[i])
        # the string reads from json are encoded in "unicode"
        unicode_len = len(words[i]) # len(words.decode("utf-8"))
        utf8_len = len(words_utf8[i])
        endpos.append(offsets[i] + unicode_len - 1)
        entity_len.append(utf8_len)
        entity_unicode_len.append(unicode_len)
        fool_type = ner_tags[i]

        if fool_type == "COMPANY":
            ner_tag = "ORGANIZATION"
        else:
            ner_tag = fool_type

        entity_type.append(ner_tag)

    d = {}
    d["phrase_id"]  = phrase_id
    d["entity"]     = entities
    d["entity_type"]= entity_type
    d["entity_len"] = entity_len
    d["entity_unicode_len"] = entity_unicode_len
    d["startpos"]   = startpos
    d["endpos"]     = endpos

    return d


#doc_id: the correponding file name in the directory "boson_cache"
# [
# {"tag": ["m", "w", "m", "w", "t", "w", "m", "w", "m", "wkz", "nx", "wky", "nz", "n", "n", "n", "wkz", "nx", "wky", "p", "ns", "nz", "n",
#  "word": ["201705", "@", "2017", "_", "2017-06-16", "_", "1497608794", "_", "772884", "<", "NB", ">", "国融", "证券", "股份", "有限公司", "<", "NB"
#  "entity": [[2, 3, "person_name"], [4, 5, "time"], [12, 16, "company_name"], [20, 25, "company_name"], [39, 44, "company_name"], [53, 54,
# }
# ]
def find_boson_entity(doc_id, phrase_id):
    if doc_id.strip() == "":
        return ""

    print "#######################"
    print "find_boson_entity: ", doc_id, phrase_id
    print "#######################"

    curdir = dirname(__file__)
    parentdir = dirname(curdir)
    doc_path = os.path.join(parentdir, "boson_cache", doc_id)

    try:
        boson_json = demjson.decode_file(doc_path, encoding="utf8")

        words        = boson_json[0]["word"]
        # format: [12, 16, "company_name"]
        # entity要根据 start, end来合并words中的word来组成
        entity_infos = boson_json[0]["entity"]
        pos_tags     = boson_json[0]["tag"]
        entities     = []
        startpos     = []
        endpos       = []
        entity_unicode_lens = []
        ner_tags     = []
    except Exception, e:
        print doc_id
        print e.message()

    # Boson NER的 start,end是以分词后的词为单位，而不是以字为单位
    segment_unicode_lens = [len(w) for w in words]
    # print words
    # print segment_unicode_lens

    # 计算每个分词的长度，以及其实位置
    char_start = []
    char_end   = []
    s = 0
    for i in segment_unicode_lens:
        char_start.append(s)
        char_end.append(s + i -1)
        s = s + i

    for e in entity_infos:
        start = e[0]
        end   = e[1]
        boson_type  = e[2]

        entity = "".join(words[start:end])
        if boson_type == "person_name":
            ner_tag = "PERSON"
        elif boson_type == "company_name":
            ner_tag = "ORGANIZATION"
        elif boson_type == "location":
            ner_tag = "LOCATION"
        else:
            ner_tag = boson_type.upper()
        # just include entity
        entity_utf8 = entity.encode("utf-8")
        entities.append(entity_utf8)
        ner_tags.append(ner_tag)

        startpos.append(char_start[start])
        # -1 is by the definition of boson ner
        endpos.append(char_end[end - 1])
        entity_unicode_lens.append(char_end[end -1 ] - char_start[start] + 1)

    d = {}
    d["phrase_id"]  = phrase_id
    d["entity"]     = entities
    d["entity_type"]= ner_tags
    d["entity_unicode_len"] = entity_unicode_lens
    d["startpos"]   = startpos
    d["endpos"]     = endpos

    return d

def setupDoc_ID_Dic():
    """
    读取boson_phrases.txt文件，构建 dictionary {phrase_id: [doc_id, sentence]}
    :return:   dictionary {phrase_id: [doc_id, sentence]}
    """
    dic = {}

    with open("./boson_phrases.txt", "r") as f:
        lines = f.readlines()

    for line in lines:
        items = line.split("\t")
        if len(items) != 3:
            continue

        doc_id, phrase_id, sentence = line.split("\t")
        dic[phrase_id] = [doc_id, sentence]

    return dic


# Boson, FNLP, LTP三个工具，在分词时去掉了所有的空格，导致entity的offset值，与corenlp, hanlp, foolnltk不同
# 影响实体对比的效果。
# 此函数用于获取sentence中的所用空格的信息，以用来纠正Boson, FNLP, LTP的offset值
# 输入: 确保str是unicode值
# 输出: [[index, offset]], index是空格的位置，offset是之后的实体的偏移量
# 遇到多个连续空格时，只记录最后一个空格的信息
def getspaceinfo(sent):
    """
    :param sent:   sentence
    :return:  [[space_index, offset_to_be_added]]
    """
    if type(sent) == str:
        sent = sent.decode("utf-8")

    spaceinfo = []
    if type(sent) == unicode:

        pre = ""
        offset = 0
        for i in range(len(sent)):
            cur = sent[i]
            if cur == " ":
                index = i
                offset = offset + 1
            else:
                if pre == " ":
                    spaceinfo.append([index, offset])
            pre = cur

    return spaceinfo


def updateentityoffset(spaceinfo, entityinfo):
    """
    :param: spaceinfo: list generated by getspaceinfo
    :param: entityinfo:
    :return: none
    
    function description : update entityinfo via spaceinfo
    list是传引用
    """

    startpos = entityinfo["startpos"]
    endpos   = entityinfo["endpos"]

    entity_num = len(startpos)

    space_index  = [a[0] for a in spaceinfo]
    space_index.append(9999)
    space_offset = [a[1] for a in spaceinfo]
    space_offset.append(9999)

    space_num = len(space_index) - 1

    i = 0
    for j in range(space_num):

        startrange = space_index[j] - space_offset[j]
        endrange   = space_index[j + 1] - space_offset[j + 1]
        while i < entity_num:
            if startpos[i] <= startrange:
                i = i + 1
                continue
            elif startpos[i] > startrange and startpos[i] <= endrange:
                startpos[i] += space_offset[j]
                endpos[i]   += space_offset[j]
                i = i + 1
            else:
                break


def find_entity_overlap(entity_ner1, startpos_ner1, endpos_ner1,
                        entity_ner2, startpos_ner2, endpos_ner2):
    """

    :param entity_ner1:   list
    :param startpos_ner1: list
    :param endpos_ner1:   list
    :param entity_ner2:   list
    :param startpos_ner2: list
    :param endpos_ner2:   list
    :return: number of overlapped entites， number of totally matched (included in overlapped)
    """

    num_overlapped = 0
    totally_matched = 0

    for i in range(len(entity_ner1)):
        for j in range(len(entity_ner2)):
            if isPositionOverlapped(startpos_ner1[i], endpos_ner1[i], startpos_ner2[j], endpos_ner2[j]) == True:
                # substr, maxlength = getMaximumCommonSubstr(entity_ner1[i], entity_ner2[j])
                # if maxlength > 0:
                #     num_overlapped = num_overlapped + 1
                num_overlapped = num_overlapped+ 1

                # 可能会有错位，但如果两个实体overlapped, 同时属性相同，实体相同，应该认为是totally match
                if entity_ner1[i] == entity_ner2[j]:
                    totally_matched = totally_matched + 1
            else:
                continue

    return num_overlapped, totally_matched


def isPositionOverlapped(start1, end1, start2, end2):
    """

    :param start1: int
    :param end1:   int
    :param start2: int
    :param end2:   int
    :return: True and False
    """
    if end2 < start1:
        return False
    elif start2 > end1:
        return False
    else:
        return True



def find_overlaps(entities_info_ner1, person_index_1, location_index_1, organization_index_1,
                  entities_info_ner2, person_index_2, location_index_2, organization_index_2):
    """
    :param entities_info_ner1:     np.array of entities
    :param person_index_1:    list
    :param location_index_1:  list
    :param organization_index_1: list
    :param entities_info_ner2:     np.array of entities
    :param person_index_2: list
    :param location_index_2: list
    :param organization_index_2: list
    :return: a list pair: [ num_person_overlap, num_location_overlap, num_organzation_overlap ], [num_person_matched, num_location_matched, num_organization_matched]
    """
    
    # entity_info1
    # *********************************************************************
    entities_ner1   = np.array(entities_info_ner1["entity"])
    startpos_ner1   = np.array(entities_info_ner1["startpos"])
    endpos_ner1     = np.array(entities_info_ner1["endpos"])
    entity_len_ner1 = np.array(entities_info_ner1["entity_unicode_len"])

    persons_ner1        = entities_ner1[person_index_1]
    locations_ner1      = entities_ner1[location_index_1]
    organizations_ner1  = entities_ner1[organization_index_1]

    persons_startpos_ner1       = startpos_ner1[person_index_1]
    locations_startpos_ner1     = startpos_ner1[location_index_1]
    organizations_startpos_ner1 = startpos_ner1[organization_index_1]
    
    persons_endpos_ner1      = endpos_ner1[person_index_1]
    locations_endpos_ner1    = endpos_ner1[location_index_1]
    organizations_endpos_ner1 = endpos_ner1[organization_index_1]
    
    # entity_info2
    # *********************************************************************
    entities_ner2 = np.array(entities_info_ner2["entity"])
    startpos_ner2 = np.array(entities_info_ner2["startpos"])
    endpos_ner2 = np.array(entities_info_ner2["endpos"])
    entity_len_ner2 = np.array(entities_info_ner2["entity_unicode_len"])

    persons_ner2 = entities_ner2[person_index_2]
    locations_ner2 = entities_ner2[location_index_2]
    organizations_ner2 = entities_ner2[organization_index_2]

    persons_startpos_ner2 = startpos_ner2[person_index_2]
    locations_startpos_ner2 = startpos_ner2[location_index_2]
    organizations_startpos_ner2 = startpos_ner2[organization_index_2]

    persons_endpos_ner2 = endpos_ner2[person_index_2]
    locations_endpos_ner2 = endpos_ner2[location_index_2]
    organizations_endpos_ner2 = endpos_ner2[organization_index_2]

    # get the number of overlapped entities
    num_person_overlapped, num_person_matched = find_entity_overlap(persons_ner1, persons_startpos_ner1,persons_endpos_ner1,
                                                persons_ner2, persons_startpos_ner2,persons_endpos_ner2)
    
    num_location_overlapped, num_location_matched = find_entity_overlap(locations_ner1, locations_startpos_ner1, locations_endpos_ner1,
                                                  locations_ner2, locations_startpos_ner2, locations_endpos_ner2)
    
    num_organization_overlapped, num_organization_matched = find_entity_overlap(organizations_ner1, organizations_startpos_ner1, organizations_endpos_ner1,
                                                      organizations_ner2, organizations_startpos_ner2, organizations_endpos_ner2)

    return [num_person_overlapped, num_location_overlapped, num_organization_overlapped], [num_person_matched, num_location_matched, num_organization_matched]


def printset(name, aset):
    print name + ": " ,
    for i in aset:
        print i.decode("string_escape") ,
    print ""

if __name__ == "__main__":

    jsonObject = {}
    jsonObjArray  = []

    # create phrase_id <--> [doc_id, sentence] dictionary for look up doc_id by phrase_id
    # for boson NER
    myDocDic = setupDoc_ID_Dic()

    #文件个数
    for i in range(1): # there is only 1 file for boson
    #for i in range(22):
        print i

        json_corenlp = demjson.decode_file("./" + "corenlp_" + str(i) + ".json", encoding='utf8')
        json_ltp     = demjson.decode_file("./" + "ltp_"     + str(i) + ".json", encoding='utf8')
        json_hanlp   = demjson.decode_file("./" + "hanlp_"   + str(i) + ".json", encoding='utf8')
        json_fnlp    = demjson.decode_file("./" + "fnlp_"    + str(i) + ".json", encoding='utf8')
        json_fool    = demjson.decode_file("./" + "foolnltk_"+ str(i) + ".json", encoding='utf8')

        # data array
        data_corenlp = json_corenlp["data"]
        data_ltp     = json_ltp["data"]
        data_hanlp   = json_hanlp["data"]
        data_fnlp    = json_fnlp["data"]
        data_fool    = json_fool["data"]

        number_of_phrase = len(data_ltp)

        for j in range(number_of_phrase):
        #for j in range(3):
            # 合并organization/personal/location, 获取entities
            corenlp_entities_info = find_entity_info(data_corenlp[j], "corenlp")
            ltp_entities_info     = find_entity_info(data_ltp[j]    , "ltp"    )
            hanlp_entities_info   = find_entity_info(data_hanlp[j]  , "hanlp"  )
            fnlp_entities_info    = find_entity_info(data_fnlp[j],     "fnlp"  )
            fool_entities_info    = find_foolnltk_entity(data_fool[j])

            # ltp: 1, corenlp: 2, hanlp 4, 根据sum来得知两两是否相同

            # 实体名、实体长度、实体起始位置
            #1. 先比较三者的实体个数是否相等

            #2. 实际比较
            #2.1 PERSON 个数，有几个相同
            #2.2 LOCATION 个数，有几个相同
            #2.3 ORGANIZATION个数，有几个相同

            # 通过set的 &, in, not in来处理

            phrase_id = corenlp_entities_info["phrase_id"]

            #----------------------------------------------------------
            doc_id, sentence = myDocDic[phrase_id]
            boson_entities_info = find_boson_entity(doc_id, phrase_id)
            # ----------------------------------------------------------

            spaceinfo = getspaceinfo(sentence)

            updateentityoffset(spaceinfo, ltp_entities_info)
            updateentityoffset(spaceinfo, fnlp_entities_info)
            updateentityoffset(spaceinfo, boson_entities_info)

            np_entity_corenlp = np.array(corenlp_entities_info["entity"])
            np_entity_ltp     = np.array(ltp_entities_info["entity"])
            np_entity_hanlp   = np.array(hanlp_entities_info["entity"])
            np_entity_fnlp    = np.array(fnlp_entities_info["entity"])
            np_entity_fool    = np.array(fool_entities_info["entity"])
            np_entity_boson   = np.array(boson_entities_info["entity"])

            np_type_corenlp = np.array(corenlp_entities_info["entity_type"])
            np_type_ltp     = np.array(ltp_entities_info["entity_type"])
            np_type_hanlp   = np.array(hanlp_entities_info["entity_type"])
            np_type_fnlp    = np.array(fnlp_entities_info["entity_type"])
            np_type_fool    = np.array(fool_entities_info["entity_type"])
            np_type_boson   = np.array(boson_entities_info["entity_type"])

            # for the overlap of entity between corenlp, ltp and hanlp
            np_startpos_corenlp = np.array(corenlp_entities_info["startpos"])
            np_startpos_ltp     = np.array(ltp_entities_info["startpos"])
            np_startpos_hanlp   = np.array(hanlp_entities_info["startpos"])
            np_startpos_fnlp    = np.array(fnlp_entities_info["startpos"])
            np_startpos_fool    = np.array(fool_entities_info["startpos"])
            np_startpos_boson   = np.array(boson_entities_info["startpos"])

            np_endpos_corenlp = np.array(corenlp_entities_info["endpos"])
            np_endpos_ltp     = np.array(ltp_entities_info["endpos"])
            np_endpos_hanlp   = np.array(hanlp_entities_info["endpos"])
            np_endpos_fnlp    = np.array(fnlp_entities_info["endpos"])
            np_endpos_fool    = np.array(fool_entities_info["endpos"])
            np_endpos_boson   = np.array(boson_entities_info["endpos"])

            np_entitylen_corenlp = np.array(corenlp_entities_info["entity_unicode_len"])
            np_entitylen_ltp     = np.array(ltp_entities_info["entity_unicode_len"])
            np_entitylen_hanlp   = np.array(hanlp_entities_info["entity_unicode_len"])
            np_entitylen_fnlp    = np.array(fnlp_entities_info["entity_unicode_len"])
            np_entitylen_fool    = np.array(fool_entities_info["entity_unicode_len"])
            np_entitylen_boson   = np.array(boson_entities_info["entity_unicode_len"])

            subJsonObject = {}
            subJsonObject["phrase_id"] =  phrase_id


            # 统计每个NER中PERSON、LOCATION, ORGANIZATION的个数

            # for i in ["PERSON", "LOCATION", "ORGANIZATION"]:
            c_person_indexes       = find_all_index(np_type_corenlp, "PERSON")
            c_location_indexes     = find_all_index(np_type_corenlp, "LOCATION")
            c_organization_indexes = find_all_index(np_type_corenlp, "ORGANIZATION")

            # # for detecting the overlap of entity between corenlp, ltp and hanlp
            # c_person_list       = np_entity_corenlp[c_person_indexes]
            # c_location_list     = np_entity_corenlp[c_location_indexes]
            # c_organization_list = np_entity_corenlp[c_organization_indexes]

            # set
            c_person_set       = set(np_entity_corenlp[c_person_indexes])
            c_location_set     = set(np_entity_corenlp[c_location_indexes])
            c_organization_set = set(np_entity_corenlp[c_organization_indexes])

            # for i in ["PERSON", "LOCATION", "ORGANIZATION"]:
            l_person_indexes       = find_all_index(np_type_ltp, "PERSON")
            l_location_indexes     = find_all_index(np_type_ltp, "LOCATION")
            l_organization_indexes = find_all_index(np_type_ltp, "ORGANIZATION")

            l_person_set       = set(np_entity_ltp[l_person_indexes])
            l_location_set     = set(np_entity_ltp[l_location_indexes])
            l_organization_set = set(np_entity_ltp[l_organization_indexes])

            # for i in ["PERSON", "LOCATION", "ORGANIZATION"]:
            h_person_indexes       = find_all_index(np_type_hanlp, "PERSON")
            h_location_indexes     = find_all_index(np_type_hanlp, "LOCATION")
            h_organization_indexes = find_all_index(np_type_hanlp, "ORGANIZATION")

            h_person_set       = set(np_entity_hanlp[h_person_indexes])
            h_location_set     = set(np_entity_hanlp[h_location_indexes])
            h_organization_set = set(np_entity_hanlp[h_organization_indexes])

            # FNLP
            # for i in ["PERSON", "LOCATION", "ORGANIZATION"]:
            f_person_indexes       = find_all_index(np_type_fnlp, "PERSON")
            f_location_indexes     = find_all_index(np_type_fnlp, "LOCATION")
            f_organization_indexes = find_all_index(np_type_fnlp, "ORGANIZATION")

            f_person_set       = set(np_entity_fnlp[f_person_indexes])
            f_location_set     = set(np_entity_fnlp[f_location_indexes])
            f_organization_set = set(np_entity_fnlp[f_organization_indexes])

            # foolnltk
            # for i in ["PERSON", "LOCATION", "ORGANIZATION"]:
            o_person_indexes        = find_all_index(np_type_fool, "PERSON")
            o_location_indexes      = find_all_index(np_type_fool, "LOCATION")
            o_organization_indexes  = find_all_index(np_type_fool, "ORGANIZATION")

            o_person_set            = set(np_entity_fool[o_person_indexes])
            o_location_set          = set(np_entity_fool[o_location_indexes])
            o_organization_set      = set(np_entity_fool[o_organization_indexes])

            # boson_ner
            # for i in ["PERSON", "LOCATION", "ORGANIZATION"]:
            b_person_indexes        = find_all_index(np_type_boson, "PERSON")
            b_location_indexes      = find_all_index(np_type_boson, "LOCATION")
            b_organization_indexes  = find_all_index(np_type_boson, "ORGANIZATION")

            b_person_set            = set(np_entity_boson[b_person_indexes])
            b_location_set          = set(np_entity_boson[b_location_indexes])
            b_organization_set      = set(np_entity_boson[b_organization_indexes])

            corenlp_amount_stat = [len(c_person_indexes), len(c_location_indexes), len(c_organization_indexes)]
            ltp_amount_stat     = [len(l_person_indexes), len(l_location_indexes), len(l_organization_indexes)]
            hanlp_amount_stat   = [len(h_person_indexes), len(h_location_indexes), len(h_organization_indexes)]
            fnlp_amount_stat    = [len(f_person_indexes), len(f_location_indexes), len(f_organization_indexes)]
            fool_amount_stat    = [len(o_person_indexes), len(o_location_indexes), len(o_organization_indexes)]
            boson_amount_stat   = [len(b_person_indexes), len(b_location_indexes), len(b_organization_indexes)]

            #------------------------------------------------
            subJsonObject["corenlp"] = corenlp_amount_stat
            subJsonObject["ltp"]     = ltp_amount_stat
            subJsonObject["hanlp"]   = hanlp_amount_stat
            subJsonObject["fnlp"]    = fnlp_amount_stat
            subJsonObject["fool"]    = fool_amount_stat
            subJsonObject["boson"]   = boson_amount_stat 
            # ------------------------------------------------
            # 11
            # cl_person_set        = c_person_set & l_person_set
            # ch_person_set        = c_person_set & h_person_set
            # cf_person_set        = c_person_set & f_person_set
            # lh_person_set        = l_person_set & h_person_set
            # lf_person_set        = l_person_set & f_person_set
            # hf_person_set        = h_person_set & f_person_set
            # clh_person_set       = c_person_set & l_person_set & h_person_set
            # clf_person_set       = c_person_set & l_person_set & f_person_set
            # chf_person_set       = c_person_set & h_person_set & f_person_set
            # lhf_person_set       = l_person_set & h_person_set & f_person_set
            # clhf_person_set       = c_person_set & l_person_set & h_person_set & f_person_set
            # 
            # cl_location_set = c_location_set & l_location_set
            # ch_location_set = c_location_set & h_location_set
            # cf_location_set = c_location_set & f_location_set
            # lh_location_set = l_location_set & h_location_set
            # lf_location_set = l_location_set & f_location_set
            # hf_location_set = h_location_set & f_location_set
            # clh_location_set = c_location_set & l_location_set & h_location_set
            # clf_location_set = c_location_set & l_location_set & f_location_set
            # chf_location_set = c_location_set & h_location_set & f_location_set
            # lhf_location_set = l_location_set & h_location_set & f_location_set
            # clhf_location_set = c_location_set & l_location_set & h_location_set & f_location_set
            # 
            # cl_organization_set = c_organization_set & l_organization_set
            # ch_organization_set = c_organization_set & h_organization_set
            # cf_organization_set = c_organization_set & f_organization_set
            # lh_organization_set = l_organization_set & h_organization_set
            # lf_organization_set = l_organization_set & f_organization_set
            # hf_organization_set = h_organization_set & f_organization_set
            # clh_organization_set = c_organization_set & l_organization_set & h_organization_set
            # clf_organization_set = c_organization_set & l_organization_set & f_organization_set
            # chf_organization_set = c_organization_set & h_organization_set & f_organization_set
            # lhf_organization_set = l_organization_set & h_organization_set & f_organization_set
            # clhf_organization_set = c_organization_set & l_organization_set & h_organization_set & f_organization_set
            # 
            # 
            # cl  = [len(cl_person_set),  len(cl_location_set),  len(cl_organization_set)]
            # ch  = [len(ch_person_set),  len(ch_location_set),  len(ch_organization_set)]
            # cf  = [len(cf_person_set),  len(cf_location_set),  len(cf_organization_set)]
            # lh  = [len(lh_person_set),  len(lh_location_set),  len(lh_organization_set)]
            # lf  = [len(lf_person_set),  len(lf_location_set),  len(lf_organization_set)]
            # hf  = [len(hf_person_set),  len(hf_location_set),  len(hf_organization_set)]
            # clh = [len(clh_person_set), len(clh_location_set), len(clh_organization_set)]
            # clf = [len(clf_person_set), len(clf_location_set), len(clf_organization_set)]
            # chf = [len(chf_person_set), len(chf_location_set), len(chf_organization_set)]
            # lhf = [len(lhf_person_set), len(lhf_location_set), len(lhf_organization_set)]
            # clhf = [len(clhf_person_set), len(clhf_location_set), len(clhf_organization_set)]
            # 
            # 
            # 
            # # ------------------------------------------------
            # subJsonObject["cl"  ] =  cl
            # subJsonObject["ch"  ] =  ch
            # subJsonObject["cf"  ] =  cf
            # subJsonObject["lh"  ] =  lh
            # subJsonObject["lf"  ] =  lf
            # subJsonObject["hf"  ] =  hf
            # subJsonObject["clh" ] =  clh
            # subJsonObject["clf" ] =  clf
            # subJsonObject["chf" ] =  chf
            # subJsonObject["lhf" ] =  lhf
            # subJsonObject["clhf"] =  clhf
            # # ------------------------------------------------
            # 
            # # for overlap inforamtion
            # cl_overlapped = find_overlaps(corenlp_entities_info, c_person_indexes, c_location_indexes, c_organization_indexes,
            #                               ltp_entities_info, l_person_indexes, l_location_indexes, l_organization_indexes)
            # 
            # ch_overlapped = find_overlaps(corenlp_entities_info, c_person_indexes, c_location_indexes, c_organization_indexes,
            #                               hanlp_entities_info, h_person_indexes, h_location_indexes, h_organization_indexes)
            # 
            # cf_overlapped = find_overlaps(corenlp_entities_info, c_person_indexes, c_location_indexes, c_organization_indexes,
            #                               fnlp_entities_info, f_person_indexes, f_location_indexes, f_organization_indexes)
            # 
            # lh_overlapped = find_overlaps(ltp_entities_info, l_person_indexes, l_location_indexes, l_organization_indexes,
            #                               hanlp_entities_info, h_person_indexes, h_location_indexes, h_organization_indexes)
            # 
            # lf_overlapped = find_overlaps(ltp_entities_info, l_person_indexes, l_location_indexes, l_organization_indexes,
            #                               fnlp_entities_info, f_person_indexes, f_location_indexes, f_organization_indexes)
            # 
            # hf_overlapped = find_overlaps(hanlp_entities_info, h_person_indexes, h_location_indexes, h_organization_indexes,
            #                               fnlp_entities_info, f_person_indexes, f_location_indexes, f_organization_indexes)
            # 
            # # ------------------------------------------------
            # subJsonObject["cl_overlapped"] = cl_overlapped
            # subJsonObject["ch_overlapped"] = ch_overlapped
            # subJsonObject["cf_overlapped"] = cf_overlapped
            # subJsonObject["lh_overlapped"] = lh_overlapped
            # subJsonObject["lf_overlapped"] = lf_overlapped
            # subJsonObject["hf_overlapped"] = hf_overlapped
            # #subJsonObject["clh"] = clh
            # # ------------------------------------------------

            # ## 2018-01-31 set operation deleted
            # bc_person_set = b_person_set & c_person_set
            # bl_person_set = b_person_set & l_person_set
            # bh_person_set = b_person_set & h_person_set
            # bf_person_set = b_person_set & f_person_set
            # bo_person_set = b_person_set & h_person_set
            # # print " b_person_set: ",  b_person_set
            # # print " c_person_set: ",  c_person_set
            # # print " l_person_set: ",  l_person_set
            # # print " h_person_set: ",  h_person_set
            # # print " f_person_set: ",  f_person_set
            # # print " o_person_set: ",  o_person_set
            # #
            # # print "bc_person_set: ", bc_person_set
            # # print "bl_person_set: ", bl_person_set
            # # print "bh_person_set: ", bh_person_set
            # # print "bf_person_set: ", bf_person_set
            # # print "bo_person_set: ", bo_person_set
            # #
            # printset(" b_person_set: ", b_person_set)
            # printset(" c_person_set: ", c_person_set)
            # printset(" l_person_set: ", l_person_set)
            # printset(" h_person_set: ", h_person_set)
            # printset(" f_person_set: ", f_person_set)
            # printset(" o_person_set: ", o_person_set)
            #
            # printset("bc_person_set: ",bc_person_set)
            # printset("bl_person_set: ",bl_person_set)
            # printset("bh_person_set: ",bh_person_set)
            # printset("bf_person_set: ",bf_person_set)
            # printset("bo_person_set: ",bo_person_set)
            #
            #
            #
            #
            # bc_location_set = b_location_set & c_location_set
            # bl_location_set = b_location_set & l_location_set
            # bh_location_set = b_location_set & h_location_set
            # bf_location_set = b_location_set & f_location_set
            # bo_location_set = b_location_set & h_location_set
            #
            # bc_organization_set = b_organization_set & c_organization_set
            # bl_organization_set = b_organization_set & l_organization_set
            # bh_organization_set = b_organization_set & h_organization_set
            # bf_organization_set = b_organization_set & f_organization_set
            # bo_organization_set = b_organization_set & h_organization_set
            #
            # # print " b_organization_set: ", b_organization_set
            # # print " c_organization_set: ", c_organization_set
            # # print " l_organization_set: ", l_organization_set
            # # print " h_organization_set: ", h_organization_set
            # # print " f_organization_set: ", f_organization_set
            # # print " o_organization_set: ", o_organization_set
            # #
            # # print "bc_organization_set: ", bc_organization_set
            # # print "bl_organization_set: ", bl_organization_set
            # # print "bh_organization_set: ", bh_organization_set
            # # print "bf_organization_set: ", bf_organization_set
            # # print "bo_organization_set: ", bo_organization_set
            # #
            # printset(" b_organization_set: ",  b_organization_set)
            # printset(" c_organization_set: ",  c_organization_set)
            # printset(" l_organization_set: ",  l_organization_set)
            # printset(" h_organization_set: ",  h_organization_set)
            # printset(" f_organization_set: ",  f_organization_set)
            # printset(" o_organization_set: ",  o_organization_set)
            #
            # printset("bc_organization_set: ", bc_organization_set)
            # printset("bl_organization_set: ", bl_organization_set)
            # printset("bh_organization_set: ", bh_organization_set)
            # printset("bf_organization_set: ", bf_organization_set)
            # printset("bo_organization_set: ", bo_organization_set)
            #
            #
            # bc  = [len(bc_person_set),  len(bc_location_set),  len(bc_organization_set)]
            # bl  = [len(bl_person_set),  len(bl_location_set),  len(bl_organization_set)]
            # bh  = [len(bh_person_set),  len(bh_location_set),  len(bh_organization_set)]
            # bf  = [len(bf_person_set),  len(bf_location_set),  len(bf_organization_set)]
            # bo  = [len(bo_person_set),  len(bo_location_set),  len(bo_organization_set)]
            #
            # # ------------------------------------------------
            # subJsonObject["bc"] = bc
            # subJsonObject["bl"] = bl
            # subJsonObject["bh"] = bh
            # subJsonObject["bf"] = bf
            # subJsonObject["bo"] = bo
            # # ------------------------------------------------
            # ## 2018-01-31 set operation deleted
            # for overlap inforamtion

            bc_overlapped, bc_matched = find_overlaps(boson_entities_info, b_person_indexes, b_location_indexes, b_organization_indexes,
                                          corenlp_entities_info, c_person_indexes, c_location_indexes, c_organization_indexes)

            bl_overlapped, bl_matched = find_overlaps(boson_entities_info, b_person_indexes, b_location_indexes, b_organization_indexes,
                                          ltp_entities_info, l_person_indexes, l_location_indexes, l_organization_indexes)
    
            bh_overlapped, bh_matched = find_overlaps(boson_entities_info, b_person_indexes, b_location_indexes, b_organization_indexes,
                                          hanlp_entities_info, h_person_indexes, h_location_indexes, h_organization_indexes)
    
            bf_overlapped, bf_matched = find_overlaps(boson_entities_info, b_person_indexes, b_location_indexes, b_organization_indexes,
                                          fnlp_entities_info, f_person_indexes, f_location_indexes, f_organization_indexes)
    
            bo_overlapped, bo_matched = find_overlaps(boson_entities_info, b_person_indexes, b_location_indexes, b_organization_indexes,
                                          fool_entities_info, o_person_indexes, o_location_indexes, o_organization_indexes)

            # ------------------------------------------------
            subJsonObject["bc"] = bc_matched
            subJsonObject["bl"] = bl_matched
            subJsonObject["bh"] = bh_matched
            subJsonObject["bf"] = bf_matched
            subJsonObject["bo"] = bo_matched
            # ------------------------------------------------
            # ------------------------------------------------
            subJsonObject["bc_overlapped"] = bc_overlapped
            subJsonObject["bl_overlapped"] = bl_overlapped
            subJsonObject["bh_overlapped"] = bh_overlapped
            subJsonObject["bf_overlapped"] = bf_overlapped
            subJsonObject["bo_overlapped"] = bo_overlapped
            # subJsonObject["clh"] = clh
            # ------------------------------------------------

            jsonObjArray.append(subJsonObject)

        jsonObject["stats"] = jsonObjArray
        #
        print "*" * 20
        print "writing to : o_" + str(i) + ".json"

        #demjson.encode_to_file("./" + str(i) + ".json", encoding="utf-8")

        with open("o_" + str(i) +  ".json", "w") as fp:
            json.dump(jsonObject, fp)
        print "done."





