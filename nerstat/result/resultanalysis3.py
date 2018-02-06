# -*- coding: utf-8 -*-

import json
import demjson
import numpy as np
import time

from matplotlib import pyplot as plt
from matplotlib_venn import venn3, venn3_circles, venn3_unweighted
from matplotlib_venn import venn2, venn2_circles, venn2_unweighted

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

for i in range(1):
    result = demjson.decode_file("./r_o_" + str(i) + ".json")

    # c_entity   += np.array(result["c"])
    # l_entity   += np.array(result["l"])
    # h_entity   += np.array(result["h"])
    # cl_entity  += np.array(result["cl"])
    # ch_entity  += np.array(result["ch"])
    # lh_entity  += np.array(result["lh"])
    # clh_entity += np.array(result["clh"])
    #
    # cl_overlapped += np.array(result["cl_overlapped"])
    # ch_overlapped += np.array(result["ch_overlapped"])
    # lh_overlapped += np.array(result["lh_overlapped"])

    c_entity += np.array(result["c"])
    l_entity += np.array(result["l"])
    h_entity += np.array(result["h"])
    f_entity += np.array(result["f"])
    o_entity += np.array(result["o"])
    b_entity += np.array(result["b"])

    bc_entity += np.array(result["bc"])
    bl_entity += np.array(result["bl"])
    bh_entity += np.array(result["bh"])
    bf_entity += np.array(result["bf"])
    bo_entity += np.array(result["bo"])

    bc_overlapped += np.array(result["bc_overlapped"])
    bl_overlapped += np.array(result["bl_overlapped"])
    bh_overlapped += np.array(result["bh_overlapped"])
    bf_overlapped += np.array(result["bf_overlapped"])
    bo_overlapped += np.array(result["bo_overlapped"])

# """
#  the functions venn3 and venn3_circles take a 7-element list of subset sizes
#  (Abc, aBc, ABc, abC, AbC, aBC, ABC),
#  and draw a three-circle area-weighted venn diagram
# """
# print "c + l + h"
#
# Clh = c_entity - cl_entity - ch_entity + clh_entity
# cLh = l_entity - cl_entity - lh_entity + clh_entity
# clH = h_entity - ch_entity - lh_entity + clh_entity
# CLh = cl_entity - clh_entity
# ClH = ch_entity - clh_entity
# cLH = lh_entity - clh_entity
# CLH = clh_entity
#
#
# print c_entity
# print l_entity
# print h_entity
# print cl_entity
# print ch_entity
# print lh_entity
# print clh_entity
#
# print "*" * 20
# print Clh
# print cLh
# print clH
# print CLh
# print ClH
# print cLH
# print CLH
#
#
# """
#  the functions venn3 and venn3_circles take a 7-element list of subset sizes
#  (Abc, aBc, ABc, abC, AbC, aBC, ABC),
#  and draw a three-circle area-weighted venn diagram
#
#  with FNLP
# """
# print "c+l+f"
# Clf = c_entity - cl_entity - cf_entity + clf_entity
# cLf = l_entity - cl_entity - lf_entity + clf_entity
# clF = f_entity - cf_entity - lf_entity + clf_entity
# CLf = cl_entity - clf_entity
# ClF = cf_entity - clf_entity
# cLF = lf_entity - clf_entity
# CLF = clf_entity
#
#
# print c_entity
# print l_entity
# print f_entity
# print cl_entity
# print cf_entity
# print lf_entity
# print clf_entity
#
# print "*" * 20
# print Clf
# print cLf
# print clF
# print CLf
# print ClF
# print cLF
# print CLF


# plt.figure(figsize=(4,4))
# #(Abc, aBc, ABc, abC, AbC, aBC, ABC)
#
# plt.subplot(121)
# # v = venn3(subsets=(Clh[0], cLh[0], CLh[0], clH[0], ClH[0], cLH[0], CLH[0]), set_labels = ('CoreNLP', 'LTP', 'HanLP'))
# v = venn3(subsets=(Clf[0], cLf[0], CLf[0], clF[0], ClF[0], cLF[0], CLF[0]), set_labels = ('CoreNLP', 'LTP', 'FNLP'))
#
# # v.get_patch_by_id('100').set_alpha(1.0)
# # v.get_patch_by_id('100').set_color('white')
# # v.get_label_by_id('100').set_text('Unknown')
# # v.get_label_by_id('A').set_text('Set "A"')
# # c = venn3_circles(subsets=(Clh[0], cLh[0], clH[0], CLh[0], ClH[0], cLH[0], CLH[0]), linestyle='dashed')
# # c[0].set_lw(1.0)
# # c[0].set_ls('dotted')
# plt.title("Person Entity")
# # plt.annotate('Unknown set', xy=v.get_label_by_id('100').get_position() - np.array([0, 0.05]), xytext=(-70,-70),
# #              ha='center', textcoords='offset points', bbox=dict(boxstyle='round,pad=0.5', fc='gray', alpha=0.1),
# #              arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.5',color='gray'))
#
# #plt.show()
#
# plt.subplot(122)
# #v2 = venn3(subsets=(Clh[2], cLh[2], CLh[2], clH[2], ClH[2], cLH[2], CLH[2]), set_labels = ('CoreNLP', 'LTP', 'HanLP'))
# v2 = venn3(subsets=(Clf[2], cLf[2], CLf[2], clF[2], ClF[2], cLF[2], CLF[2]), set_labels = ('CoreNLP', 'LTP', 'FNLP'))
# plt.title("Organization Entity")
# plt.show()

# 柱状图
# plt.figure(figsize=(4,4))
#
# plt.subplot(121)
# # for person
# plt.title("Person")
# plt.xlabel("category")
# plt.ylabel("entity num")
#
# plt.xticks((0,1,2,3,4,5,6,7,8,9),("CoreNLP", "LTP", "HanLP",
#                                   r'$C \cap L$', r'$C \cap H$', r'$L \cap H$', r'$C \cap L \cap H$',
#                                   r'$C \times L$', r'$C \times H$', r'$L \times H$'))
#
#
# plt.bar(0, c_entity[0],   label='CoreNLP'           )
# plt.bar(1, l_entity[0],   label='LTP'               )
# plt.bar(2, h_entity[0],   label='HanLP'             )
# plt.bar(3, cl_entity[0],  label=r'$C \cap L$'       )
# plt.bar(4, ch_entity[0],  label=r'$C \cap H$'       )
# plt.bar(5, lh_entity[0],  label=r'$L \cap H$'       )
# plt.bar(6, clh_entity[0], label=r'$C \cap L \cap H$')
#
# plt.bar(7, cl_overlapped[0], label=r'$C \times L$'   )
# plt.bar(8, ch_overlapped[0], label=r'$C \times H$'   )
# plt.bar(9, lh_overlapped[0], label=r'$L \times H$'   )
#
# #plt.legend()
#
# plt.subplot(122)
# # for organization
# plt.title("Organization")
# plt.xlabel(u"Category")
# plt.ylabel(u"Entity Num")
#
# plt.xticks((0,1,2,3,4,5,6,7,8,9),("CoreNLP", "LTP", "HanLP",
#                                   r'$C \cap L$', r'$C \cap H$', r'$L \cap H$', r'$C \cap L \cap H$',
#                                   r'$C \times L$', r'$C \times H$', r'$L \times H$'))
#
#
# plt.bar(0, c_entity[2],   label='CoreNLP'           )
# plt.bar(1, l_entity[2],   label='LTP'               )
# plt.bar(2, h_entity[2],   label='HanLP'             )
# plt.bar(3, cl_entity[2],  label=r'$C \cap L$'       )
# plt.bar(4, ch_entity[2],  label=r'$C \cap H$'       )
# plt.bar(5, lh_entity[2],  label=r'$L \cap H$'       )
# plt.bar(6, clh_entity[2], label=r'$C \cap L \cap H$')
#
# plt.bar(7, cl_overlapped[2], label=r'$C \times L$'   )
# plt.bar(8, ch_overlapped[2], label=r'$C \times H$'   )
# plt.bar(9, lh_overlapped[2], label=r'$L \times H$'   )
#
# #plt.legend()
#
# plt.show()



# 柱状图
plt.figure(figsize=(4,4))

plt.subplot(211)
# for person
plt.title("Person")
plt.xlabel("category")
plt.ylabel("entity num")

#x = [0,1,2,3,4,5,6,7,8,9]#,10,11,12,13,14,15]
x = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
xlabels = ["CoreNLP", "LTP", "HanLP", "FNLP", "Fool", "Boson",
#xlabels = [
            r'$B \cap C$', r'$B \cap L$', r'$B \cap H$', r'$B \cap F$', r'$B \cap O$',
            r'$B \times C$', r'$B \times L$', r'$B \times H$', r'$B \times F$', r'$B \times O$']

plt.xticks((0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15),("CoreNLP", "LTP", "HanLP", "FNLP", "Fool", "Boson"
                                  r'$B \cap C$', r'$B \cap L$', r'$B \cap H$', r'$B \cap F$', r'$B \cap O$',
                                  r'$B \times C$', r'$B \times L$', r'$B \times H$', r'$B \times F$', r'$B \times O$'), rotation='vertical')

plt.xticks(x, xlabels, rotation='vertical')

# plt.bar(0,       c_entity[0]) #,  label='CoreNLP'        )
# plt.bar(1,       l_entity[0]) #,  label='LTP'            )
# plt.bar(2,       h_entity[0]) #,  label='HanLP'          )
# plt.bar(3,       f_entity[0]) #,  label=r'FNLP'          )
# plt.bar(4,       o_entity[0]) #,  label=r'FOOL'          )
# plt.bar(5,       b_entity[0]) #,  label=r'BOSON'         )
# plt.bar(0,      bc_entity[0]) #,  label=r'$B \cap C$'    )
# plt.bar(1,      bl_entity[0]) #,  label=r'$B \cap L$'    )
# plt.bar(2,      bh_entity[0]) #,  label=r'$B \cap H$'    )
# plt.bar(3,      bf_entity[0]) #,  label=r'$B \cap F$'    )
# plt.bar(4,      bo_entity[0]) #,  label=r'$B \cap O$'    )
# plt.bar(5,  bc_overlapped[0]) #,  label=r'$B \times C$'  )
# plt.bar(6,  bl_overlapped[0]) #,  label=r'$B \times L$'  )
# plt.bar(7,  bh_overlapped[0]) #,  label=r'$B \times H$'  )
# plt.bar(8,  bf_overlapped[0]) #,  label=r'$B \times F$'  )
# plt.bar(9,  bo_overlapped[0]) #,  label=r'$B \times O$'  )

plt.bar(0,       c_entity[0]) #,  label='CoreNLP'        )
plt.bar(1,       l_entity[0]) #,  label='LTP'            )
plt.bar(2,       h_entity[0]) #,  label='HanLP'          )
plt.bar(3,       f_entity[0]) #,  label=r'FNLP'          )
plt.bar(4,       o_entity[0]) #,  label=r'FOOL'          )
plt.bar(5,       b_entity[0]) #,  label=r'BOSON'         )
plt.bar(6,      bc_entity[0]) #,  label=r'$B \cap C$'    )
plt.bar(7,      bl_entity[0]) #,  label=r'$B \cap L$'    )
plt.bar(8,      bh_entity[0]) #,  label=r'$B \cap H$'    )
plt.bar(9,      bf_entity[0]) #,  label=r'$B \cap F$'    )
plt.bar(10,     bo_entity[0]) #,  label=r'$B \cap O$'    )
plt.bar(11, bc_overlapped[0]) #,  label=r'$B \times C$'  )
plt.bar(12, bl_overlapped[0]) #,  label=r'$B \times L$'  )
plt.bar(13, bh_overlapped[0]) #,  label=r'$B \times H$'  )
plt.bar(14, bf_overlapped[0]) #,  label=r'$B \times F$'  )
plt.bar(15, bo_overlapped[0]) #,  label=r'$B \times O$'  )


#plt.legend()

plt.subplot(212)
# for organization
plt.title("Organization")
plt.xlabel(u"Category")
plt.ylabel(u"Entity Num")

# plt.xticks((0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15),("CoreNLP", "LTP", "HanLP", "FNLP", "Fool", "Boson",
#                                   r'$B \cap C$', r'$B \cap L$', r'$B \cap H$', r'$B \cap F$', r'$B \cap O$',
#                                   r'$B \times C$', r'$B \times L$', r'$B \times H$', r'$B \times F$', r'$B \times O$'), rotation='vertical')
plt.xticks(x, xlabels, rotation='vertical')

# plt.bar(0,       c_entity[2]) #,  label='CoreNLP'        )
# plt.bar(1,       l_entity[2]) #,  label='LTP'            )
# plt.bar(2,       h_entity[2]) #,  label='HanLP'          )
# plt.bar(3,       f_entity[2]) #,  label=r'FNLP'          )
# plt.bar(4,       o_entity[2]) #,  label=r'FOOL'          )
# plt.bar(5,       b_entity[2]) #,  label=r'BOSON'         )
# plt.bar(0,      bc_entity[2]) #,  label=r'$B \cap C$'    )
# plt.bar(1,      bl_entity[2]) #,  label=r'$B \cap L$'    )
# plt.bar(2,      bh_entity[2]) #,  label=r'$B \cap H$'    )
# plt.bar(3,      bf_entity[2]) #,  label=r'$B \cap F$'    )
# plt.bar(4,      bo_entity[2]) #,  label=r'$B \cap O$'    )
# plt.bar(5,  bc_overlapped[2]) #,  label=r'$B \times C$'  )
# plt.bar(6,  bl_overlapped[2]) #,  label=r'$B \times L$'  )
# plt.bar(7,  bh_overlapped[2]) #,  label=r'$B \times H$'  )
# plt.bar(8,  bf_overlapped[2]) #,  label=r'$B \times F$'  )
# plt.bar(9,  bo_overlapped[2]) #,  label=r'$B \times O$'  )
#
plt.bar(0,       c_entity[2]) #,  label='CoreNLP'        )
plt.bar(1,       l_entity[2]) #,  label='LTP'            )
plt.bar(2,       h_entity[2]) #,  label='HanLP'          )
plt.bar(3,       f_entity[2]) #,  label=r'FNLP'          )
plt.bar(4,       o_entity[2]) #,  label=r'FOOL'          )
plt.bar(5,       b_entity[2]) #,  label=r'BOSON'         )
plt.bar(6,      bc_entity[2]) #,  label=r'$B \cap C$'    )
plt.bar(7,      bl_entity[2]) #,  label=r'$B \cap L$'    )
plt.bar(8,      bh_entity[2]) #,  label=r'$B \cap H$'    )
plt.bar(9,      bf_entity[2]) #,  label=r'$B \cap F$'    )
plt.bar(10,     bo_entity[2]) #,  label=r'$B \cap O$'    )
plt.bar(11, bc_overlapped[2]) #,  label=r'$B \times C$'  )
plt.bar(12, bl_overlapped[2]) #,  label=r'$B \times L$'  )
plt.bar(13, bh_overlapped[2]) #,  label=r'$B \times H$'  )
plt.bar(14, bf_overlapped[2]) #,  label=r'$B \times F$'  )
plt.bar(15, bo_overlapped[2]) #,  label=r'$B \times O$'  )

#plt.legend()

plt.show()