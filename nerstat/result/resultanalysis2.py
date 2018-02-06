# -*- coding: utf-8 -*-

import json
import demjson
import numpy as np
import time

from collections import defaultdict

import multiprocessing


class AnalysisProc(multiprocessing.Process):

    def __init__(self, jsonfile):
        multiprocessing.Process.__init__(self)
        self.jsonfile = jsonfile

        self.jsonData = {}

        print "creating subprocess : " + self.jsonfile


    def run(self):
        print "subprocess " + self.jsonfile +  " started @ " + time.ctime()

        c_entity = np.array([0, 0, 0])
        l_entity = np.array([0, 0, 0])
        h_entity = np.array([0, 0, 0])
        f_entity = np.array([0, 0, 0])
        o_entity = np.array([0, 0, 0])
        b_entity = np.array([0, 0, 0])

        bc_entity = np.array([0, 0, 0])
        bl_entity = np.array([0, 0, 0])
        bh_entity = np.array([0, 0, 0])
        bf_entity = np.array([0, 0, 0])
        bo_entity = np.array([0, 0, 0])

        bc_overlapped = np.array([0, 0, 0])
        bl_overlapped = np.array([0, 0, 0])
        bh_overlapped = np.array([0, 0, 0])
        bf_overlapped = np.array([0, 0, 0])
        bo_overlapped = np.array([0, 0, 0])

        result = demjson.decode_file(self.jsonfile)
        stats = result["stats"]  # list

        for i in range(len(stats)):
            c_entity      += np.array(stats[i]["corenlp"])
            l_entity      += np.array(stats[i]["ltp"])
            h_entity      += np.array(stats[i]["hanlp"])
            f_entity      += np.array(stats[i]["fnlp"])
            o_entity      += np.array(stats[i]["fool"])
            b_entity      += np.array(stats[i]["boson"])

            bc_entity     += np.array(stats[i]["bc"])
            bl_entity     += np.array(stats[i]["bl"])
            bh_entity     += np.array(stats[i]["bh"])
            bf_entity     += np.array(stats[i]["bf"])
            bo_entity     += np.array(stats[i]["bo"])

            bc_overlapped += np.array(stats[i]["bc_overlapped"])
            bl_overlapped += np.array(stats[i]["bl_overlapped"])
            bh_overlapped += np.array(stats[i]["bh_overlapped"])
            bf_overlapped += np.array(stats[i]["bf_overlapped"])
            bo_overlapped += np.array(stats[i]["bo_overlapped"])

        self.jsonData["c"  ] = list(c_entity)
        self.jsonData["l"  ] = list(l_entity)
        self.jsonData["h"  ] = list(h_entity)
        self.jsonData["f"  ] = list(f_entity)
        self.jsonData["o"  ] = list(o_entity)
        self.jsonData["b"  ] = list(b_entity)

        self.jsonData["bc"] = list(bc_entity)
        self.jsonData["bl"] = list(bl_entity)
        self.jsonData["bh"] = list(bh_entity)
        self.jsonData["bf"] = list(bf_entity)
        self.jsonData["bo"] = list(bo_entity)

        self.jsonData["bc_overlapped"] = list(bc_overlapped)
        self.jsonData["bl_overlapped"] = list(bl_overlapped)
        self.jsonData["bh_overlapped"] = list(bh_overlapped)
        self.jsonData["bf_overlapped"] = list(bf_overlapped)
        self.jsonData["bo_overlapped"] = list(bo_overlapped)

        with open("./r_" + self.jsonfile, "w") as fp:
            json.dump(self.jsonData, fp)

        print "subprocess " + self.jsonfile + " ended @ " + time.ctime()


# c_entity   = np.array([0,0,0])
# l_entity   = np.array([0,0,0])
# h_entity   = np.array([0,0,0])
# cl_entity  = np.array([0,0,0])
# ch_entity  = np.array([0,0,0])
# lh_entity  = np.array([0,0,0])
# clh_entity = np.array([0,0,0])
#
# for i in range(22):  # totally 22 results
#     result = demjson.decode_file("./" + str(i) + ".json")
#     stats = result["stats"]  # list
#
#     for i in range(len(stats)):
#         c_entity   += np.array(stats[i]["corenlp"])
#         l_entity   += np.array(stats[i]["ltp"])
#         h_entity   += np.array(stats[i]["hanlp"])
#         cl_entity  += np.array(stats[i]["cl"])
#         ch_entity  += np.array(stats[i]["ch"])
#         clh_entity += np.array(stats[i]["clh"])
#
#
# print c_entity
# print l_entity
# print h_entity
# print cl_entity
# print ch_entity
# print lh_entity
# print clh_entity

if __name__ == "__main__":

    print "create subprocesses......"

    # instance list
    processes = []

    for i in range(1):
        processes.append(AnalysisProc( "o_" + str(i) + ".json"))

    print "runnning processes, started @ " + time.ctime()
    for pi in processes:
        pi.start()

    print ("process information from active_children: ")
    for p in multiprocessing.active_children():
        print("child   p.name: " + p.name + "\tp.id: " + str(p.pid))

    print "runnning processes, ended @ " + time.ctime()