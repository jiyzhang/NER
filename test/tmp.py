from jpype import *

import sys


reload(sys)
sys.setdefaultencoding("utf-8")

javaClassPath = "/home/snorkel-admin/wind_fonduer/snorkel/hanlp/lib/hanlp-1.5.2/hanlp-1.5.2.jar:/home/snorkel-admin/wind_fonduer/snorkel/hanlp/lib/hanlp-1.5.2/"
startJVM(getDefaultJVMPath(), '-Djava.class.path='+javaClassPath, '-Xms1g', '-Xmx1g')
NLPTokenizer = JClass('com.hankcs.hanlp.tokenizer.NLPTokenizer')

doc_text = u'聘任周克军女士执行总裁、毛新礼先生、董绍学先生、张文先生为公司副总经理，张明为总园艺师，李思先生为副总会计师，王五为总工程师，赵六为财务总监。'

if isinstance(doc_text, unicode):
    doc_text = doc_text.encode("utf-8", "error")

print getDefaultJVMPath()
results =  NLPTokenizer.segment(doc_text)
for v in NLPTokenizer.segment(doc_text):
    print v




from jpype import *

import sys


reload(sys)
sys.setdefaultencoding("utf-8")

javaClassPath = "/Users/richardz/00_wind/nlpwrapper/hanlp/lib/hanlp-1.5.2/hanlp-1.5.2.jar:/Users/richardz/00_wind/nlpwrapper/hanlp/lib/hanlp-1.5.2/"
startJVM(getDefaultJVMPath(), '-Djava.class.path='+javaClassPath, '-Xms1g', '-Xmx1g')
NLPTokenizer = JClass('com.hankcs.hanlp.tokenizer.NLPTokenizer')

doc_text = u'聘任周克军女士执行总裁、毛新礼先生、董绍学先生、张文先生为公司副总经理，张明为总园艺师，李思先生为副总会计师，王五为总工程师，赵六为财务总监。'

if isinstance(doc_text, unicode):
    doc_text = doc_text.encode("utf-8", "error")

print getDefaultJVMPath()
results =  NLPTokenizer.segment(doc_text)

for v in NLPTokenizer.segment(doc_text):
    print v