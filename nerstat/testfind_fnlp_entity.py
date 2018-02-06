import sys
sys.path.append(".")

import unittest
import nerstat
import demjson

class testfind_corenlp_entity(unittest.TestCase):
    def setUp(self):
        # a705f39be129883f0241bf8762d129d8	5665
        self.doc_id = "a705f39be129883f0241bf8762d129d8"
        self.phrase_id = "5665"

    def test1(self):
        json_fnlp = demjson.decode_file("./" + "fnlp_0_test.json")
        data_fnlp = json_fnlp["data"]

        number_of_phrase = len(data_fnlp)

        for j in range(3):
            fnlp_entities_info = nerstat.find_entity_info(data_fnlp[j], "fnlp")
            entities = fnlp_entities_info["entity"]
            ner_tags = fnlp_entities_info["entity_type"]
            entity_unicode_lens = fnlp_entities_info["entity_unicode_len"]
            startposes = fnlp_entities_info["startpos"]
            endposes   = fnlp_entities_info["endpos"]
            num = len(entities)
            for i in range(num):
                print entities[i].decode("utf-8")
                print ner_tags[i]
                print startposes[i], endposes[i], entity_unicode_lens[i]

if __name__ == '__main__':
    unittest.main()