# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from ner.deepnlpner import DeepNLPNer

doc_text = u'聘任周克军女士执行总裁、毛新礼先生、董绍学先生、张文先生为公司副总经理，张明为总园艺师，李思先生为副总会计师，王五为总工程师，赵六为财务总监。'
#doc_text = u"我爱吃北京烤鸭"

reco = DeepNLPNer()

mygenerator = reco.parse(doc_text)

for i in mygenerator:
    cws_len = len(i["words"])
    word_l = i["words"]
    pos_l  = i["pos_tags"]
    ner_l  = i["ner_tags"]
    for j in range(cws_len):
        print word_l[j] + "\t\t\t\t\t , pos =: " + pos_l[j] + "\t\t\t, ner =: " + ner_l[j]