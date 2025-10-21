import numpy as np
from math import floor, ceil, log2
from Pre_error_matrix import Pre_error_matrix
from Pre_aux_block import Pre_aux_block
from Sort_error_matrix import Sort_error_matrix
from dec_to_bin import dec_to_bin
from huffman_define import huffman_define
from EncryptionImg import EncryptionImg
from EncryptionString import EncryptionString
from Embed_Aux_Img import Embed_Aux_Img


def owner(cover, t1, t2, Encryption_key):
    m, n = cover.shape
    bm = m // t1
    bn = n // t2

    same_MSB_Num = np.zeros(9, dtype=int)
    same_MSB_dec = []
    same_MSB_Array = np.ones((bm, bn), dtype=int)
    same_MSB_LSB_Num = np.zeros(9, dtype=int)
    same_All_Num_bin = []
    same_MSB_bin = []
    LSB_label_Array = []
    LSB_label_cell = [[[] for _ in range(bn)] for _ in range(bm)]
    LSB_aux_Array = []

    # Get APE image and sign map
    error_matrix, error_sign_label = Pre_error_matrix(cover)

    # Process each individual divided block
    for i in range(bm):
        for j in range(bn):
            # Extract error block
            r_start = i * t1
            c_start = j * t2
            error_block = error_matrix[r_start:r_start + t1, c_start:c_start + t2]

            # Analyze each APE block and get same_MSB, LSB_label, LSB_aux_info
            same_MSB, LSB_label, LSB_aux_info = Pre_aux_block(error_block, t1, t2)

            # Count the number of blocks with different same_MSB
            same_MSB_Num[same_MSB] += 1
            same_MSB_dec.append(same_MSB)
            LSB_label_Array.extend(LSB_label)
            LSB_label_cell[i][j] = LSB_label
            LSB_aux_Array.extend(LSB_aux_info)

            same_MSB_LSB_Num[same_MSB + sum(np.array(LSB_label) == 1)] += 1
            same_MSB_Array[i, j] = same_MSB + sum(np.array(LSB_label) == 1)

    numBit = 0
    for i in range(9):
        numBit += same_MSB_LSB_Num[i] * i * t1 * t2

    # Formulate Huffman coding rules
    huffman_rule = huffman_define(same_MSB_Num)
    rule = []
    # Huffman encoding
    for MSB_value in same_MSB_dec:
        same_MSB_bin.extend(huffman_rule[MSB_value])

    for i in range(9):
        rule.extend(huffman_rule[i])

    same_MSB_bin = rule + same_MSB_bin

    # bit-plane swapping and block rearrangement
    sort_error_matrix = Sort_error_matrix(error_matrix, same_MSB_Array, LSB_label_cell, t1, t2)

    for i in range(8, -1, -1):
        oneBin = dec_to_bin(same_MSB_LSB_Num[i], ceil(log2(bm * bn)))
        same_All_Num_bin.extend(oneBin)

    # Image Encryption
    En_img = EncryptionImg(sort_error_matrix, Encryption_key)

    # Embed auxiliary information into the encrypted image
    first_pixel = dec_to_bin(int(cover[0, 0]), 8)

    # Ensure all components are lists for concatenation
    same_MSB_bin_list = list(same_MSB_bin) if not isinstance(same_MSB_bin, list) else same_MSB_bin
    LSB_label_list = list(LSB_label_Array) if not isinstance(LSB_label_Array, list) else LSB_label_Array
    LSB_aux_list = list(LSB_aux_Array) if not isinstance(LSB_aux_Array, list) else LSB_aux_Array
    error_sign_list = list(error_sign_label) if not isinstance(error_sign_label, list) else error_sign_label
    first_pixel_list = list(first_pixel) if not isinstance(first_pixel, list) else first_pixel

    remain_auxInfo = same_MSB_bin_list + LSB_label_list + LSB_aux_list + error_sign_list + first_pixel_list

    # Encrypt auxiliary information
    EncryptedAuxString = EncryptionString(remain_auxInfo, Encryption_key)

    remain_auxInfo_size_dec = len(remain_auxInfo)
    remain_auxInfo_size_bin = dec_to_bin(remain_auxInfo_size_dec, ceil(log2(m * n * 8)))

    Emb_aux_img = Embed_Aux_Img(En_img, t1, t2, same_All_Num_bin, remain_auxInfo_size_bin, EncryptedAuxString)

    Encrypted_img = Emb_aux_img

    return np.array(Encrypted_img)