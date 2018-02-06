# coding:utf-8

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import re
import json

# fp = open(r"../ner_sample.json", "r")
# strjson = fp.read()
# fp.close()
# print len(strjson)
#
# #rule = "\"ltp\"\:\s{(.*)},"
# # rule1 = r"\"ltp\":\s*{.*?(},)"
# # rule2 = r"\"ltp\":\s*{.*?}"
#
# rule = r"\s+},\n}"
# pattern = re.compile(rule, re.S)
#
# result = pattern.findall(strjson)
#
# for i in result:
#     print i
#     print "-" * 20
#
#
# res, num = pattern.subn("\n\t}\n}", strjson)
#
# #print res
# print num
#
# # fp2 = open(r"../ner_sample2.json", "w")
# # fp2.writelines(res)
# # fp2.close()
#
# res = res.encode("utf-8")

##### for json test

fp3 = open(r"../test.json", "r")
res2 = fp3.read()

res2 = res2.encode("utf-8")
fp3.close()
# decodedJson = json.loads(res)
# print type(decodedJson)

try:
    myjson = json.loads(res2, encoding="utf-8")
except ValueError, e:
    print ("JSON object issue: %s") % e

print myjson

print type(myjson)

print myjson["corenlp"]["pos_tags"]
print myjson["corenlp"]["char_offsets"]