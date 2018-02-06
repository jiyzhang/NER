import sys
sys.path.append(".")

import unittest
import nerstat
import demjson

class testfind_fool_entity(unittest.TestCase):
    def setUp(self):
        # a705f39be129883f0241bf8762d129d8	5665
        self.doc_id = "a705f39be129883f0241bf8762d129d8"
        self.phrase_id = "5665"

    def test1(self):
        json_fool = demjson.decode_file("./" + "foolnltk_0_test.json")
        data_fool = json_fool["data"]

        number_of_phrase = len(data_fool)

        for j in range(3):
            myentity = nerstat.find_foolnltk_entity(data_fool[j])
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