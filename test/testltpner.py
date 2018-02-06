# -*- coding: utf-8 -*-

from __future__ import print_function
from ner.ltpner import LTPNer

#doc_text = u'聘任周克军女士执行总裁、毛新礼先生、董绍学先生、张文先生为公司副总经理，张明为总园艺师，李思先生为副总会计师，王五为总工程师，赵六为财务总监。'
#doc_text = u"公司登记机关办理变更登记；公司解散的，应当依法办理公司注销登记；设立新公司的，应当依法办理公司设立登记。"
doc_text = "201608@2016_2016-08-22_1471854646_237857 证券代码：835875证券简称：天基新材主办券商：国泰君安 北京天基新材料股份有限公司股权质押公告 本公司及董事会全体成员保证公告内容的真实、准确和完整，没有虚假记载、误导性陈述或者重大遗漏，并对其内容的真实性、准确性和完整性承担个别及连带法律责任。"

#doc_text = u"""ご縄" 腎蕎奪ざタ麟独レ鱒' " 韓欝剛襖]疆嵩"""
reco = LTPNer()

# separators = ['{', '}', '[', ']', '"', '\'', ':', ',', ':']
# separators_repalce = [ '<LB>', '<RB>', '<LSB>', '<RSB>', '<Q>', '<SQ>', '<SC>', '<COMMA>', '<COLON>']


# def replace_separator(word):
#     for i in range(len(separators)):
#         #print word + ", " + separators[i]
#         if word == separators[i]:
#             return separators_repalce[i]
#     return word

mygenerator = reco.parse(doc_text)

for i in mygenerator:
    cws_len = len(i["words"])
    word_l = i["words"]
    # word_l = [replace_separator(x) for x in word_l]
    pos_l  = i["pos_tags"]
    ner_l  = i["ner_tags"]
    char_offset_l = i["char_offsets"]

    for j in range(cws_len):
        #print word_l[j] + "\t\t\t , pos =: " + pos_l[j] + "\t\t\t, ner =: " + ner_l[j]
        print("{0: <20s}\t{1: <10s}\t{2: <10s}\t{3: <5d}".format(word_l[j].encode("utf-8"), pos_l[j], ner_l[j], char_offset_l[j]))
