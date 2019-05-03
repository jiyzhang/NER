# -*- coding: utf-8 -*-

# python3

import os
import sys
import json
import numpy as np
import time

# from ner.corenlpner import CoreNLPNer
# from ner.hanlpner   import HanLPNer
# from ner.ltpner     import LTPNer
import fool

import multiprocessing

#python2
# reload(sys)
# sys.setdefaultencoding("utf-8")

class FoolNER(object):

    def __init__(self):
        # 是否可以加载多个字典文件？
        """
        def load_userdict(path):
            _DICTIONARY.add_dict(path)
        """
        fool.load_userdict("mydic/hushen_company.txt")
        fool.load_userdict("mydic/company.dic")
        fool.load_userdict("mydic/name.dic")
        fool.load_userdict("mydic/term.dic")

    def parse(self, text):

        results = []
        result = {}
        words = []
        pos_tags = []
        ner_tags = []
        char_offsets = []
        entity_lens = []
        tmp_words, ners = fool.analysis(text)

        # ners: [[(12, 23, 'time', '2016-08-22'), (56, 61, 'company', '天基新材'),....]]
        #for ner in ners:    //requried after load_userdict
        for ner in ners[0]:
            char_offsets.append(ner[0])
            word = ner[3]
            words.append(word)
            tmp_ner_tag = ner[2]
            ner_tag = ""
            if tmp_ner_tag == "person":
                ner_tag = "PERSON"
            elif tmp_ner_tag == "location":
                ner_tag = "LOCATION"
            elif tmp_ner_tag == "org":
                ner_tag = "ORGANIZATION"
            else:
                ner_tag = tmp_ner_tag.upper()

            ner_tags.append(ner_tag)

            #unicode_len = len(word.decode("utf-8"))
            #entity_lens.append(unicode_len)
        result["words"] = words
        #TypeError: Object of type 'bytes' is not JSON serializable
        #result["words"] = [i.encode("utf-8") for i in words]
        result["pos_tags"] = pos_tags
        result["ner_tags"] = ner_tags
        result["char_offsets"] = char_offsets
        #result["word_lengths"] = entity_lens

        results.append(result)

        return results

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


        # # load NER modules
        # if self.nername == "corenlp":
        #     self.ner = CoreNLPNer()
        #     self.conn = self.corenlp_ner.connect()
        # elif self.nername == "ltp":
        #     self.ner = LTPNer()
        # else: # foolnltk
        #     self.ner = FoolNER()

        self.ner = FoolNER()

        self.jsonData = {}

        print("creating subprocess : " + self.nername + ":" + self.group_id + ", number of phrase: " + str(self.numofphrase))


    def run(self):
        print("subprocess " + self.nername + ":" + self.group_id + " started @ " + time.ctime())

        jsonList = []

        for iter in range(self.numofphrase):
            raw_text = self.phrase_list[iter].text
            # for python3
            #raw_text = raw_text.encode("utf-8", "error")

            jsonobject = {}

            document_id = str(self.phrase_list[iter].document_id)
            phrase_id = str(self.phrase_list[iter].id)

            jsonobject["document_id"] = document_id
            jsonobject["phrase_id"]   = phrase_id

            words = []
            pos_tags = []
            ner_tags = []
            char_offsets = []

            # if self.nername == "corenlp":
            #     parseresult = self.ner.parse(raw_text, self.conn)
            # elif self.nername == "ltp": #ltp
            #     parseresult = self.ner.parse(raw_text)
            # else: #foolNER
            #     parseresult = self.ner.parse(raw_text)

            parseresult = self.ner.parse(raw_text)
            # phrase is part of sentence, so only 1 item returned

            nerObject = {}
            for i in parseresult:
                words = i["words"]
                pos_tags = i["pos_tags"]
                ner_tags = i["ner_tags"]
                char_offsets = i["char_offsets"]

                # only 1 iteration
                nerObject["words"]    = words
                nerObject["pos_tags"] = pos_tags
                nerObject["ner_tags"] = ner_tags
                nerObject["char_offsets"]  = char_offsets

            jsonobject[self.nername] = nerObject

            jsonList.append(jsonobject)

        self.jsonData["data"] = jsonList

        with open(self.nername + "_" + self.group_id + ".json", "w") as fp:
            json.dump(self.jsonData, fp, ensure_ascii=False)

        print("subprocess " + self.nername + ":" + self.group_id + " ended @ " + time.ctime())

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
            print("hit0")
        elif len(items) == 2:
            document_id = items[0]
            id          = items[1]
            text        = ""
            print("hit1")
            continue
        else:
            document_id = items[0]
            id          = ""
            text        = ""
            print("hit2")
            continue

        # 多个空格合并为一个
        text = " ".join(text.split())

        phrase = Phrase(document_id, id, text)
        phrases.append(phrase)

    # for i in range(5):
    #     p = phrases[i]
    #     d_id = p.document_id
    #     id = p.id
    #     text = p.text
    #
    #     print("document_id = " + d_id + ", phrase_id = " + id + ", text = " + text)

    # fetch phrases from file phrase.txt

    # PARALLEL = 16 # assuming a quad-core machine
    # ATTRIBUTE = "wind_director2k_lf_zs"
    #
    # os.environ['SNORKELDBNAME'] = ATTRIBUTE
    # os.environ['SNORKELDB'] = 'postgres:///' + os.environ['SNORKELDBNAME']
    #
    # from snorkel.contrib.fonduer import SnorkelSession
    #
    # session = SnorkelSession()
    #
    # # omit copur parse
    # from snorkel.contrib.fonduer.models import Document, Phrase
    #
    # print("Documents:", session.query(Document).count())
    # print("Phrases:", session.query(Phrase).count())
    # # Documents: 1943
    # # Phrases: 212305
    #
    # print("fetching all phrases: ")
    # phrases = session.query(Phrase).all()
    #
    # print("Done to fetch phrases from DB : " + time.ctime())



    batch_size = 10000
    numberofphrase = len(phrases)
    #numberofphrase = 4321
    last_id  = numberofphrase - 1 # 0..numberofphrase - 1
    rounds = numberofphrase // batch_size + 1
    last_round = rounds - 1


    print("create subprocesses......")

    # instance list
    processes = []

    phrases_group = [ phrases[i*batch_size:(i+1) * batch_size] for i in range(rounds - 1)]
    phrases_group.append(phrases[last_round * batch_size: last_id + 1])

    group_size = [len(p) for p in phrases_group]
    print(",".join(str(p) for p in group_size))


    for i in range(rounds):
        processes.append(NERProcess("foolnltk", phrases_group[i], i))


    print("runnning processes, started @ " + time.ctime())
    for pi in processes:
        pi.start()

    print ("process information from active_children: ")
    for p in multiprocessing.active_children():
        print("child   p.name: " + p.name + "\tp.id: " + str(p.pid))

    print("runnning processes, ended @ " + time.ctime())
