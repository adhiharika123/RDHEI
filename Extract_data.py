
import numpy as np
from math import floor, ceil, log2
from Plane_sequence import Plane_sequence
from bin_to_dec import bin_to_dec
from Index_to_bm_bn import Index_to_bm_bn
from DecryptionString import DecryptionString

def Extract_data(Marked_img, t1, t2, Data_key):
    m, n = Marked_img.shape
    bm = m // t1
    bn = n // t2

    All_emb_info = []
    one_block = True
    first_block = Marked_img[0:t1, 0:t2]
    layer = 1

    first_plane_sequence = Plane_sequence(first_block, t1, t2, layer, t1 * t2)
    All_emb_info.extend(first_plane_sequence)

    index = 0
    block_index = 0
    NumbinLen = ceil(log2(bm * bn))

    for i in range(8, -1, -1):  # MATLAB 9:-1:1 corresponds to 8 to 0 in Python
        MSB_value = i

        if index + NumbinLen > len(All_emb_info) and one_block:
            layer += 1
            if layer > MSB_value:
                print("Block storage error")
                break
            All_emb_info.extend(Plane_sequence(first_block, t1, t2, layer, t1 * t2))

        MSB_Num = bin_to_dec(All_emb_info[index:index + NumbinLen], NumbinLen)
        index += NumbinLen

        if MSB_Num == 0:
            continue
        else:
            block_end_index = block_index + MSB_Num
            if one_block:
                for j in range(layer + 1, MSB_value + 1):
                    All_emb_info.extend(Plane_sequence(first_block, t1, t2, j, t1 * t2))
                one_block = False
                block_index += 1

            for j in range(block_index, block_end_index):
                bm1, bn1 = Index_to_bm_bn(j + 1, bm, bn)
                this_block = Marked_img[(bm1 - 1) * t1:bm1 * t1, (bn1 - 1) * t2:bn1 * t2]

                for M in range(1, MSB_value + 1):
                    All_emb_info.extend(Plane_sequence(this_block, t1, t2, M, t1 * t2))

            block_index = block_end_index

    if block_index != bm * bn:
        print("An error occurred in the previous operation")

    Aux_Len = 9 * NumbinLen

    bin_size = ceil(log2(m * n * 8))
    remain_auxInfo_size_bin = All_emb_info[Aux_Len:Aux_Len + bin_size]
    remain_auxInfo_size = bin_to_dec(remain_auxInfo_size_bin, bin_size)

    Aux_Len = Aux_Len + bin_size + remain_auxInfo_size
    data = All_emb_info[Aux_Len:]
    data = DecryptionString(data, Data_key)

    return data
