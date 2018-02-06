# -*- coding: utf-8 -*-
import os
import sys
import json
import signal
import socket
import string
import warnings

from subprocess import Popen,PIPE
from collections import defaultdict

from .recognizer import Recognizer, URLRecognizerConnection

class CoreNLPNer(Recognizer):
    '''
    Stanford CoreNLP Server

    Implementation uses the simple default web API server
    https://stanfordnlp.github.io/CoreNLP/corenlp-server.html

    Useful configuration examples:

    (1) Disable Penn Treebank Normalization and force strict PTB compliance,
        disabling the following default behaviors:
         (a) Add "." to the end of sentences that end with an abbrv, e.g., Corp.
         (b) Adds a non-breaking space to fractions 5 1/2

        annotator_opts = {}
        annotator_opts['tokenize'] = {"invertible": True,
                                    "normalizeFractions": False,
                                    "normalizeParentheses": False,
                                    "normalizeOtherBrackets": False,
                                    "normalizeCurrency": False,
                                    "asciiQuotes": False,
                                    "latexQuotes": False,
                                    "ptb3Ellipsis": False,
                                    "ptb3Dashes": False,
                                    "escapeForwardSlashAsterisk": False,
                                    "strictTreebank3": True}

    '''
    # Penn TreeBank normalized tokens
    PTB = {'-RRB-': ')', '-LRB-': '(', '-RCB-': '}', '-LCB-': '{', '-RSB-': ']', '-LSB-': '['}

    # CoreNLP changed some JSON element names across versions
    # BLOCK_DEFS = {"3.6.0":"basic-dependencies", "3.7.0":"basicDependencies"}
    # modified by zhengshun to employ corenlp 3.8.0
    BLOCK_DEFS = {"3.6.0":"basic-dependencies", "3.7.0":"basicDependencies", "3.8.0":"basicDependencies"}

    # def __init__(self, annotators=['tokenize', 'ssplit', 'pos', 'lemma', 'ner'],
    #              annotator_opts={}, tokenize_whitespace=False,
    #              split_newline=False, encoding="utf-8", java_xmx='4g',
    #              port=12345, num_threads=1, delimiter=None, verbose=False,
    #              version='3.8.0'):

    def __init__(self, annotators=['tokenize', 'ssplit', 'pos', 'lemma', 'depparse', 'ner'],
                 annotator_opts={}, tokenize_whitespace=False,
                 split_newline=False, encoding="utf-8", java_xmx='4g',
                 port=12345, num_threads=1, delimiter=None, verbose=False,
                 version='3.8.0'):
        '''
        Create CoreNLP server instance.
        :param annotators:
        :param annotator_opts:
        :param tokenize_whitespace:
        :param split_newline:
        :param java_xmx:
        :param port:
        :param num_threads:
        :param verbose:
        :param version:
        '''
        super(CoreNLPNer, self).__init__(name="CoreNLP", encoding=encoding)

        self.tokenize_whitespace = tokenize_whitespace
        self.split_newline = split_newline
        self.annotators = annotators
        self.annotator_opts = annotator_opts

        self.java_xmx = java_xmx
        self.port = port
        self.timeout = 600000
        self.num_threads = num_threads
        self.verbose = verbose
        self.version = version
        self.delimiter = delimiter

        # configure connection request options
        opts = self._conn_opts(annotators, annotator_opts, tokenize_whitespace, split_newline, delimiter)
        #self.endpoint = 'http://127.0.0.1:%d/?%s' % (self.port, opts)
        self.endpoint = 'http://10.18.0.154:%d/?%s' % (self.port, opts)
        ##self._start_server()

        if self.verbose:
            self.summary()

    # def _start_server(self, force_load=False):
    #     '''
    #     Launch CoreNLP server
    #     :param force_load:  Force server to pre-load models vs. on-demand
    #     :return:
    #     '''
    #
    #     snorkelhome = "/Users/richardz/00_wind/nlpwrapper"
    #     loc = os.path.join(snorkelhome, 'corenlp')
    #     #loc = os.path.join(os.environ['SNORKELHOME'], 'parser')
    #     # cmd = 'java -Xmx%s -cp "%s/*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer --port %d --timeout %d --threads %d > /dev/null'
    #     # modify by zhengshun to use chinese corenlp 3.8.0
    #     cmd = 'java -Xmx%s -cp "%s/*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -serverProperties StanfordCoreNLP-chinese.properties --port %d --timeout %d --threads %d > /dev/null'
    #     cmd = [cmd % (self.java_xmx, loc, self.port, self.timeout, self.num_threads)]
    #
    #     # Setting shell=True returns only the pid of the screen, not any spawned child processes
    #     # Killing child processes correctly requires using a process group
    #     # http://stackoverflow.com/questions/4789837/how-to-terminate-a-python-subprocess-launched-with-shell-true
    #     self.process_group = Popen(cmd, stdout=PIPE, shell=True, preexec_fn=os.setsid)
    #
    #     if force_load:
    #         conn = self.connect()
    #         text = "This forces the server to preload all models."
    #         parts = list(conn.parse(None, text))

    def _conn_opts(self, annotators, annotator_opts, tokenize_whitespace, split_newline, delimiter):
        '''
        Server connection properties

        :param annotators:
        :param annotater_opts:
        :param tokenize_whitespace:
        :param split_newline:
        :return:
        '''
        # TODO: ssplit options aren't being recognized (but they don't throw any errors either...)
        ssplit_opts = annotator_opts["ssplit"] if "ssplit" in  annotator_opts else {}
        props = [self._get_props(annotators, annotator_opts)]
        if tokenize_whitespace:
            props += ['"tokenize.whitespace": "true"']
        if split_newline:
            props += ['"ssplit.eolonly": "true"']
        if ssplit_opts and 'newlineIsSentenceBreak' in ssplit_opts:
            props += ['"ssplit.newlineIsSentenceBreak": "{}"'.format(ssplit_opts['newlineIsSentenceBreak'])]
        if delimiter:
            props += ["\"ssplit.htmlBoundariesToDiscard\": \"%s\"" % delimiter]
        props = ",".join(props)
        return 'properties={%s}' % (props)

    def _get_props(self, annotators, annotator_opts):
        '''
        Enable advanced configuration options for CoreNLP
        Options are configured by each separate annotator

        :param opts: options dictionary
        :return:
        '''
        opts = []
        for name in annotator_opts:
            if not annotator_opts[name]:
                continue
            props = ["{}={}".format(key, str(value).lower()) for key, value in annotator_opts[name].items()]
            opts.append('"{}.options":"{}"'.format(name, ",".join(props)))

        props = []
        props += ['"annotators": {}'.format('"{}"'.format(",".join(annotators)))]
        props += ['"outputFormat": "json"']
        props += [",".join(opts)] if opts else []
        return ",".join(props)

    # def __del__(self):
    #     '''
    #     Clean-up this object by forcing the server process to shut-down
    #     :return:
    #     '''
    #     self.close()

    def summary(self):
        '''
        Print server parameters
        :return:
        '''
        print("-" * 40)
        print(self.endpoint)
        print("version:", self.version)
        ##print("shell pid:", self.process_group.pid)
        print("port:", self.port)
        print("timeout:", self.timeout)
        print("threads:", self.num_threads)
        print("-" * 40)

    def connect(self):
        '''
        Return URL connection object for this server
        :return:
        '''
        return URLRecognizerConnection(self)

    # def close(self):
    #     '''
    #     Kill the process group linked with this server.
    #     :return:
    #     '''
    #     if self.verbose:
    #         print("Killing CoreNLP server [{}]...".format(self.process_group.pid))
    #     if self.process_group is not None:
    #         try:
    #             os.killpg(os.getpgid(self.process_group.pid), signal.SIGTERM)
    #         except Exception as e:
    #             sys.stderr.write('Could not kill CoreNLP server [{}] {}\n'.format(self.process_group.pid,e))

    def parse(self, text, conn):
        '''
        Parse CoreNLP JSON results. Requires an external connection/request object to remain threadsafe

        :param text:
        :param conn: server connection
        :return:
        '''
        if len(text.strip()) == 0:
            print>> sys.stderr, "Warning, empty text passed to CoreNLP"
            return

        # handle encoding (force to unicode)
        if isinstance(text, unicode):
            text = text.encode('utf-8', 'error')

        # POST request to CoreNLP Server
        try:
            content = conn.post(self.endpoint, text)
            content = content.decode(self.encoding)

        except socket.error as e:
            print>>sys.stderr,"Socket error"
            raise ValueError("Socket Error")

        # check for parsing error messages
        CoreNLPNer.validate_response(content)

        try:
            blocks = json.loads(content, strict=False)['sentences']
        except:
            warnings.warn("CoreNLP skipped a malformed text.")

        position = 0

        for block in blocks:
            parts = defaultdict(list)
            dep_order, dep_par, dep_lab = [], [], []
            for tok, deps in zip(block['tokens'], block[CoreNLPNer.BLOCK_DEFS[self.version]]):
                # Convert PennTreeBank symbols back into characters for words/lemmas
                parts['words'].append(CoreNLPNer.PTB.get(tok['word'], tok['word']))
                parts['lemmas'].append(CoreNLPNer.PTB.get(tok['lemma'], tok['lemma']))
                parts['pos_tags'].append(tok['pos'])
                parts['ner_tags'].append(tok['ner'])
                parts['char_offsets'].append(tok['characterOffsetBegin'])

            yield parts


    @staticmethod
    def strip_non_printing_chars(s):
        return "".join([c for c in s if c in string.printable])

    @staticmethod
    def validate_response(content):
        '''
        Report common parsing errors
        :param content:
        :return:
        '''
        if content.startswith("Request is too long"):
            raise ValueError("File too long. Max character count is 100K.")
        if content.startswith("CoreNLP request timed out"):
            raise ValueError("CoreNLP request timed out on file.")
