# -*- coding: utf-8 -*-
import os
import sys
import json
import signal
import socket
import string
import warnings
from os.path import dirname, abspath

from collections import defaultdict

#from .recognizer import Recognizer, RecognizerConnection


from pyltp import *

class LTPNer(object):
    '''
    LTP Parser

    Implementation uses the LTP API(pyltp)
    https://github.com/hit-scir/pyltp

    '''
    def __init__(self):
        #super(LTPNer, self).__init__(name="LTP")
        self.name = "LTP"
        # load model
        d = abspath(dirname(__file__))
        parent_path = os.path.dirname(d)

        LTP_DATA_DIR = parent_path + "/ltp/ltp_data"
        LTP_EXT_DIC = parent_path + "/mydic/ltp_all.dic"

        # print LTP_DATA_DIR

        #LTP_DATA_DIR = 'ltp/ltp_data'  # ltp模型目录的路径
        cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
        pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')
        ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')

        # 加载模型
        self.segmentor = Segmentor()
        # 加载自定义词典
        self.segmentor.load_with_lexicon(cws_model_path, LTP_EXT_DIC)

        self.postagger = Postagger()
        self.postagger.load(pos_model_path)

        self.recognizer = NamedEntityRecognizer()
        self.recognizer.load(ner_model_path)

    def __del__(self):
        # 释放模型
        self.recognizer.release()
        self.postagger.release()
        self.segmentor.release()

    # @property
    # def connect(self):
    #     '''
    #     Return URL connection object for this server
    #     :return:
    #     '''
    #     return RecognizerConnection(self)


    def parse(self, text):
        '''
        Parse LTP results. Requires an external connection/request object to remain threadsafe

        :param document:
        :param text:
        :return:
        '''
        if len(text.strip()) == 0:
            print>> sys.stderr, "Warning, empty text passed to CoreNLP"
            return

        # handle encoding (force to unicode)
        if isinstance(text, unicode):
            text = text.encode('utf-8', 'error')


        # 整个Phrase一起分词
        # sents = SentenceSplitter.split(text)

        blocks = []
        # for sent in sents:
        words   = self.segmentor.segment(text) #(sent)
        postags = self.postagger.postag(words)
        nertags = self.recognizer.recognize(words, postags)
        #for word, ntag in zip(words, nertags):
        #    print word + '/' + ntag
        blocks.append(zip(words, postags, nertags))

        # 释放模型
        # recognizer.release()
        # postagger.release()
        # segmentor.release()

#        position = 0


        for block in blocks:
            parts = defaultdict(list)

            offset = 0
            # 确保语句中没有空格
            for word, pos, ner in block:

                word_u = word.decode("utf-8")
                parts['words'].append(word_u)
                parts['lemmas'].append(word)
                parts['pos_tags'].append(pos)

                # LTP ner-tags: O/S/B/I/E Nh/Ns/Ni
                # changed to CoreNLP style

                if ner == "O":
                    ner_tag = "O"
                elif ner[2:4] == "Nh":
                    ner_tag = "PERSON"
                elif ner[2:4] == "Ni":
                    ner_tag = "ORGANIZATION"
                elif ner[2:4] == "Ns":
                    ner_tag = "LOCATION"
                else:
                    ner_tag = ner

                parts['ner_tags'].append(ner_tag)
                parts['char_offsets'].append(offset)


                #print type(word_u)
                word_len = len(word_u)
                offset = offset + word_len

#            parts['position'] = position

#            position += 1

            yield parts

