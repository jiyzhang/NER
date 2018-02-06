# coding:utf-8

import jnius_config

from os.path import dirname, abspath
hanlp_modue = dirname(abspath(dirname(__file__))) + "/hanlp/"

jnius_config.add_options('-Xrs', '-Xmx4G')
jnius_config.set_classpath(".:" + hanlp_modue + "hanlp-1.5.2.jar:" + hanlp_modue )


from jnius import autoclass

print jnius_config.get_classpath()

from jnius import PythonJavaClass


HanLP = autoclass('com.hankcs.hanlp.HanLP')


content = '聘任周克军女士执行总裁、毛新礼先生、董绍学先生、张文先生为公司副总经理，张明为总园艺师，李思先生为副总会计师，王五为总工程师，赵六为财务总监。'

segments = []
if isinstance(content, str) and len(content) > 0:
    # java.util.List
    result = HanLP.segment(content).listIterator()
    while result.hasNext():
        tempString = result.next().toString()
        segments.append(tempString)

for i in segments:
    print i