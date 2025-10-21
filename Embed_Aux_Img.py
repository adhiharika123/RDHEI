import numpy as np
from math import floor, ceil, log2
from bin_to_dec import bin_to_dec
from Embed_plane_seq import Embed_plane_seq
from Index_to_bm_bn import Index_to_bm_bn

def Embed_Aux_Img(En_img, t1, t2, same_All_Num_bin, remain_auxInfo_size, EncryptedAuxString):
    Emb_aux_img = En_img.copy()
    m, n = En_img.shape
    bm = m // t1
    bn = n // t2

    # All auxiliary information to embed
    AllInfo = np.concatenate((same_All_Num_bin, remain_auxInfo_size, EncryptedAuxString))
    InfoLen = len(AllInfo)

    index = 0
    block_index = 0
    data_index = 0
    flag = False
    NumbinLen = ceil(log2(bm * bn))

    for i in range(8, -1, -1):  # from 9 down to 1 (i in MATLAB)
        MSB_value = i  # i-1 in MATLAB corresponds to i in 0-based Python

        # Extract MSB_number bits from same_All_Num_bin
        MSB_number_bin = AllInfo[index:index + NumbinLen]
        MSB_number = bin_to_dec(MSB_number_bin, NumbinLen)

        if MSB_number != 0:
            index += NumbinLen
            for j in range(block_index, block_index + MSB_number):
                bm1, bn1 = Index_to_bm_bn(j + 1, bm, bn)  # Adjust 1-based indexing
                for M in range(1, MSB_value + 1):
                    r_start = (bm1 - 1) * t1
                    c_start = (bn1 - 1) * t2
                    block = Emb_aux_img[r_start:r_start + t1, c_start:c_start + t2]

                    if data_index + t1 * t2 > InfoLen:
                        data = AllInfo[data_index:InfoLen]
                        num = InfoLen - data_index
                    else:
                        data = AllInfo[data_index:data_index + t1 * t2]
                        num = t1 * t2

                    new_block = Embed_plane_seq(block, t1, t2, M, num, data)
                    Emb_aux_img[r_start:r_start + t1, c_start:c_start + t2] = new_block

                    data_index += t1 * t2
                    if data_index >= InfoLen:
                        flag = True
                        break
                if flag:
                    break
            block_index += MSB_number
        else:
            index += NumbinLen

        if flag:
            break

    return Emb_aux_img
