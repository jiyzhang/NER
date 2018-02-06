# -*- coding: utf-8 -*-

import os
import sys
import json
import numpy as np
import time

from ner.corenlpner import CoreNLPNer
#from ner.ltpner     import LTPNer

import multiprocessing

reload(sys)
sys.setdefaultencoding("utf-8")

class Phrase(object):
    def __init__(self, document_id, id, text):
        self.document_id = document_id
        self.id = id
        self.text = text

class NERProcess(multiprocessing.Process):

    def __init__(self, nername, phrase_list, groupid=0):
        multiprocessing.Process.__init__(self)
        self.nername = nername
        self.phrase_list = phrase_list
        self.numofphrase = len(phrase_list)

        # batch ID, and will be used for file name
        self.group_id = str(groupid)


        # load NER modules
        self.corenlp_ner = CoreNLPNer()
        self.conn = self.corenlp_ner.connect()
        #self.ltp_ner = LTPNer()

        self.jsonData = {}

        print "creating subprocess : " + self.nername + ":" + self.group_id + ", number of phrase: " + str(self.numofphrase)


    def run(self):
        print "subprocess " + self.nername + ":" + self.group_id + " started @ " + time.ctime()

        jsonList = []

        for iter in range(self.numofphrase):
            raw_text = self.phrase_list[iter].text
            raw_text = raw_text.encode("utf-8", "error")

            jsonobject = {}

            document_id = str(self.phrase_list[iter].document_id)
            phrase_id = str(self.phrase_list[iter].id)

            jsonobject["document_id"] = document_id
            jsonobject["phrase_id"]   = phrase_id

            words = []
            pos_tags = []
            ner_tags = []
            char_offsets = []

            corenlp_generator = self.corenlp_ner.parse(raw_text, self.conn)
            # phrase is part of sentence, so only 1 item returned

            corenlpObject = {}

            num_sentences = 0

            for i in corenlp_generator:
                words.append( i["words"] )
                pos_tags.append( i["pos_tags"] )
                ner_tags.append( i["ner_tags"] )
                char_offsets.append( i["char_offsets"] )

                num_sentences = num_sentences + 1

                # for phrases got from db, there is only 1 sentence,
                # but for materials like boson_phrases, it includes more than 1 sentences

            # 2018-01-29
            # as ssplit is used, no matter the number of sentences, corenlp will split the phrase into a list of sentences
            # 2018-01-29
            
            # as ssplit is used in the parameter
            # if num_sentences > 1:
                # words, pos_tags, ner_tags, char_offsets
                # list of list: [[],[],[],[]]
                # The codes below are for the input with more than 1 sentences

            l_words    = [x for l in words for x in l]
            l_pos_tags = [x for l in pos_tags for x in l]
            l_ner_tags = [x for l in ner_tags for x in l]
            l_char_offsets = [x for l in char_offsets for x in l]

            corenlpObject["words"]    = l_words
            corenlpObject["pos_tags"] = l_pos_tags
            corenlpObject["ner_tags"] = l_ner_tags
            corenlpObject["char_offsets"]  = l_char_offsets
            # else:
            #     corenlpObject["words"]    = words
            #     corenlpObject["pos_tags"] = pos_tags
            #     corenlpObject["ner_tags"] = ner_tags
            #     corenlpObject["char_offsets"]  = char_offsets

            jsonobject[self.nername] = corenlpObject

            jsonList.append(jsonobject)

        self.jsonData["data"] = jsonList

        with open(self.nername + "_" + self.group_id + ".json", "w") as fp:
            json.dump(self.jsonData, fp, ensure_ascii=False)

        print "subprocess " + self.nername + ":" + self.group_id + " ended @ " + time.ctime()

if __name__ == "__main__":

    print("Begining to fetch phrases from DB : " + time.ctime())

    with open("./boson_phrases.txt", "r") as f:
        phrase_lines = f.readlines()

    phrases = []

    for line in phrase_lines:
        items = line.split("\t")
        if len(items) == 3:
            document_id = items[0]
            id          = items[1]
            text        = items[2]
            print "hit0"
        elif len(items) == 2:
            document_id = items[0]
            id          = items[1]
            text        = ""
            print "hit1"
            continue
        else:
            document_id = items[0]
            id          = ""
            text        = ""
            print "hit2"
            continue

        # 多个空格合并为一个
        text = " ".join(text.split())

        phrase = Phrase(document_id, id, text)
        phrases.append(phrase)

    print "Done to fetch phrases from DB : " + time.ctime()

    batch_size = 10000
    numberofphrase = len(phrases)
    #numberofphrase = 4321
    last_id  = numberofphrase - 1 # 0..numberofphrase - 1
    rounds = numberofphrase / batch_size + 1
    last_round = rounds - 1


    print "create subprocesses......"

    # instance list
    processes = []

    phrases_group = [ phrases[i*batch_size:(i+1) * batch_size] for i in range(rounds - 1)]
    phrases_group.append(phrases[last_round * batch_size: last_id + 1])

    group_size = [len(p) for p in phrases_group]
    print ",".join(str(p) for p in group_size)


    for i in range(rounds):
        processes.append(NERProcess("corenlp", phrases_group[i], i))


    print "runnning processes, started @ " + time.ctime()
    for pi in processes:
        pi.start()

    print ("process information from active_children: ")
    for p in multiprocessing.active_children():
        print("child   p.name: " + p.name + "\tp.id: " + str(p.pid))

    print "runnning processes, ended @ " + time.ctime()
