# -*- coding:utf-8 -*-

import sys
sys.path.append(".")

import unittest
import nerstat

class testfind_boson_entity(unittest.TestCase):
    def setUp(self):
        # a705f39be129883f0241bf8762d129d8	5665
        self.doc_id = "a705f39be129883f0241bf8762d129d8"
        self.phrase_id = "5665"

    def test1(self):
        myentity = nerstat.find_boson_entity("a09e184cd67d967fc77815f10e6c23d4", "0")
        entities = myentity["entity"]
        ner_tags = myentity["entity_type"]
        entity_unicode_lens = myentity["entity_unicode_len"]
        startposes = myentity["startpos"]
        endposes   = myentity["endpos"]
        num = len(entities)
        for i in range(num):
            print entities[i].decode("utf-8")
            print ner_tags[i]
            print startposes[i], endposes[i], entity_unicode_lens[i]

if __name__ == '__main__':
    unittest.main()