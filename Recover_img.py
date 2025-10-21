import numpy as np
from math import ceil, log2
from Plane_sequence import Plane_sequence
from bin_to_dec import bin_to_dec
from DecryptionString import DecryptionString
from Recover_position import Recover_position
from Recover_error_block import Recover_error_block
from Recover_error_matrix import Recover_error_matrix
from Index_to_bm_bn import Index_to_bm_bn
from DecryptionImg import DecryptionImg



def Recover_img(Marked_img, t1, t2, Encryption_key):
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
    same_MSB_Num = []

    NumbinLen = ceil(log2(bm * bn))

    for i in range(8, -1, -1):  # MATLAB 9:-1:1 to Python 8 down to 0
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
    Aux_Len += bin_size

    en_remain_auxInfo = All_emb_info[Aux_Len:Aux_Len + remain_auxInfo_size]
    remain_auxInfo = DecryptionString(en_remain_auxInfo, Encryption_key)
    index = 0

    # Recover rules
    rule_cell = [None] * 9
    for i in range(9):
        num1, num0 = 0, 0
        rule_bin = []
        while num1 == 0 or num0 == 0:
            rule_bin.append(remain_auxInfo[index])
            if remain_auxInfo[index] == 1:
                num1 = 1
            else:
                num0 = 1
            index += 1
        rule_cell[i] = rule_bin

    # Recover MSB_num_cell
    MSB_num_cell = [[0] * bn for _ in range(bm)]
    MSB_All_num = 0
    for i in range(bm):
        for j in range(bn):
            num1, num0 = 0, 0
            MSB_bin = []
            while num1 == 0 or num0 == 0:
                MSB_bin.append(remain_auxInfo[index])
                if remain_auxInfo[index] == 1:
                    num1 = 1
                else:
                    num0 = 1
                index += 1
            for k in range(9):
                if MSB_bin == rule_cell[k]:
                    MSB_num_cell[i][j] = k
                    MSB_All_num += k
                    break

    LSB_label_Array = remain_auxInfo[index:index + (bm * bn * 8 - MSB_All_num)]
    index += (bm * bn * 8 - MSB_All_num)

    now_index = index
    sum_LSB_ones = sum(1 for bit in LSB_label_Array if bit == 1)
    for _ in range(sum_LSB_ones):
        index += 1
        num = bin_to_dec(remain_auxInfo[index:index + 2], 2)
        index += 2 + num * (ceil(log2(t1)) + ceil(log2(t2)))

    LSB_aux_Array = remain_auxInfo[now_index:index]
    error_sign_label = remain_auxInfo[index:index + m * n - 1]
    index += m * n - 1

    first_pixel = remain_auxInfo[index:index + 8]

    # Image Processing
    decryptedImg = DecryptionImg(Marked_img, Encryption_key)

    MSB_LSB_num_cell = [[0] * bn for _ in range(bm)]
    LSB_index = 0

    for i in range(bm):
        for j in range(bn):
            MSB_value = MSB_num_cell[i][j]
            LSB_all_value = 8 - MSB_value
            LSB_value = sum(1 for bit in LSB_label_Array[LSB_index:LSB_index + LSB_all_value] if bit == 1)
            MSB_LSB_num_cell[i][j] = MSB_value + LSB_value
            LSB_index += LSB_all_value

    # Restore image block positions
    re_pos_Img = Recover_position(decryptedImg, same_MSB_Num, MSB_LSB_num_cell, t1, t2)

    # Recover bit planes in each block
    error_matrix = Recover_error_block(re_pos_Img, MSB_num_cell, LSB_label_Array, LSB_aux_Array, t1, t2)

    error_matrix[0, 0] = bin_to_dec(first_pixel, 8)

    recoverImg = Recover_error_matrix(error_matrix, error_sign_label)

    return recoverImg, error_matrix
