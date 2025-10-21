
import numpy as np
from Index_to_bm_bn import Index_to_bm_bn

def Recover_position(decryptedImg, same_MSB_Num, MSB_LSB_num_cell, t1, t2):
    m, n = decryptedImg.shape
    bm = m // t1
    bn = n // t2

    re_pos_Img = decryptedImg.copy()
    same_MSB_Num_index = [0] * 9

    for i in range(bm):
        for j in range(bn):
            block_index = 0
            MSB_LSB_value = MSB_LSB_num_cell[i][j]

            same_MSB_Num_index[MSB_LSB_value] += 1

            for k in range(8 - MSB_LSB_value):
                block_index += same_MSB_Num[k]

            block_index += same_MSB_Num_index[MSB_LSB_value]

            bm1, bn1 = Index_to_bm_bn(block_index, bm, bn)

            r_start_i = i * t1
            c_start_j = j * t2
            r_start_bm1 = (bm1 - 1) * t1
            c_start_bn1 = (bn1 - 1) * t2

            re_pos_Img[r_start_i:r_start_i + t1, c_start_j:c_start_j + t2] = decryptedImg[r_start_bm1:r_start_bm1 + t1, c_start_bn1:c_start_bn1 + t2]

    return re_pos_Img
