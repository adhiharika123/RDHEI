import numpy as np
from math import ceil, log2
from Pre_error_matrix import Pre_error_matrix
from Pre_aux_block import Pre_aux_block
from Sort_error_matrix import Sort_error_matrix
from dec_to_bin import dec_to_bin
from EncryptionImg import EncryptionImg
from EncryptionString import EncryptionString
from Embed_Aux_Img import Embed_Aux_Img
from rdh_arithmetic import arithmetic_encode


# --------------------------
# Owner function
# --------------------------
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
            r_start = i * t1
            c_start = j * t2
            error_block = error_matrix[r_start:r_start + t1, c_start:c_start + t2]

            same_MSB, LSB_label, LSB_aux_info = Pre_aux_block(error_block, t1, t2)

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

    # Arithmetic encode same_MSB_dec
    compressed_MSB_bytes = arithmetic_encode(same_MSB_dec, original_symbols=list(range(9)))

    # bit-plane swapping and block rearrangement
    sort_error_matrix = Sort_error_matrix(error_matrix, same_MSB_Array, LSB_label_cell, t1, t2)

    for i in range(8, -1, -1):
        oneBin = dec_to_bin(same_MSB_LSB_Num[i], ceil(log2(bm * bn)))
        same_All_Num_bin.extend(oneBin)

    # Image Encryption
    En_img = EncryptionImg(sort_error_matrix, Encryption_key)

    # Embed auxiliary information
    first_pixel = dec_to_bin(int(cover[0, 0]), 8)

    remain_auxInfo = list(LSB_label_Array) + list(LSB_aux_Array) + list(error_sign_label) + list(first_pixel)

    EncryptedAuxString = EncryptionString(remain_auxInfo, Encryption_key)
    remain_auxInfo_size_dec = len(remain_auxInfo)
    remain_auxInfo_size_bin = dec_to_bin(remain_auxInfo_size_dec, ceil(log2(m * n * 8)))

    Emb_aux_img = Embed_Aux_Img(En_img, t1, t2, same_All_Num_bin, remain_auxInfo_size_bin, EncryptedAuxString)
    Encrypted_img = Emb_aux_img

    # Return Encrypted image and compressed MSB bytes for decoding
    return np.array(Encrypted_img), compressed_MSB_bytes
