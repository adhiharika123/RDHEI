import numpy as np
from math import floor, ceil, log2
from bin_to_dec import bin_to_dec
from Embed_first_data import Embed_first_data
from Plane_sequence import Plane_sequence
from EncryptionString import EncryptionString
from Index_to_bm_bn import Index_to_bm_bn


def Embed_data(Encrypted_img, t1, t2, data, Data_key):
    m, n = Encrypted_img.shape
    bm = m // t1
    bn = n // t2

    Marked_img = Encrypted_img.copy()
    All_emb_info = []
    one_block = True

    # first block
    first_block = Encrypted_img[0:t1, 0:t2]
    layer = 1
    first_plane_sequence = Plane_sequence(first_block, t1, t2, layer, t1 * t2)
    All_emb_info.extend(first_plane_sequence)

    index = 0
    block_index = 0
    same_MSB_Num = []

    NumbinLen = ceil(log2(bm * bn))

    Encrypted_data = EncryptionString(data, Data_key)

    for i in range(8, -1, -1):  # 9 down to 1
        MSB_value = i

        if index + NumbinLen > len(All_emb_info) and one_block:
            layer += 1
            if layer > MSB_value:
                print("Block storage error")
                break
            All_emb_info.extend(Plane_sequence(first_block, t1, t2, layer, t1 * t2))

        MSB_Num = bin_to_dec(All_emb_info[index:index + NumbinLen], NumbinLen)
        same_MSB_Num.append(MSB_Num)
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
                this_block = Encrypted_img[(bm1-1)*t1:bm1*t1, (bn1-1)*t2:bn1*t2]

                for M in range(1, MSB_value + 1):
                    All_emb_info.extend(Plane_sequence(this_block, t1, t2, M, t1 * t2))
            block_index = block_end_index

    if block_index != bm * bn:
        print("An error occurred in the previous operation")

    Aux_Len = 9 * NumbinLen
    bin_size = ceil(log2(m * n * 8))
    remain_auxInfo_size_bin = All_emb_info[Aux_Len: Aux_Len + bin_size]
    remain_auxInfo_size = bin_to_dec(remain_auxInfo_size_bin, bin_size)

    Aux_Len = Aux_Len + bin_size + remain_auxInfo_size

    flag = True
    Info_index = 0
    data_index = 0
    block_index = 0

    for i in range(1, 10):  # 1 to 9 inclusive
        MSB_value = 9 - i
        MSB_Num = same_MSB_Num[i - 1]
        for j in range(MSB_Num):
            block_index += 1
            bm1, bn1 = Index_to_bm_bn(block_index, bm, bn)
            for m_i in range(1, MSB_value + 1):
                this_block = Marked_img[(bm1 - 1)*t1:bm1*t1, (bn1 - 1)*t2:bn1*t2]
                Info_index += t1 * t2
                if not flag:
                    new_block, Embed_len = Embed_first_data(t1*t2, 0, All_emb_info, Encrypted_data, this_block, t1, t2, m_i, data_index)
                    data_index += Embed_len
                    Marked_img[(bm1 - 1)*t1:bm1*t1, (bn1 - 1)*t2:bn1*t2] = new_block
                if Info_index > Aux_Len and flag:
                    new_block, Embed_len = Embed_first_data(Info_index, Aux_Len, All_emb_info, Encrypted_data, this_block, t1, t2, m_i, 0)
                    data_index += Embed_len
                    flag = False
                    Marked_img[(bm1 - 1)*t1:bm1*t1, (bn1 - 1)*t2:bn1*t2] = new_block

    return Marked_img, data_index
