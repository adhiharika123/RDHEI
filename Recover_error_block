
import numpy as np
from math import floor, ceil, log2
from Index_to_bm_bn import Index_to_bm_bn
from block_plane_recover import block_plane_recover
from bin_to_dec import bin_to_dec

def Recover_error_block(re_pos_Img, MSB_num_cell, LSB_label_Array, LSB_aux_Array, t1, t2):
    m, n = re_pos_Img.shape
    bm = m // t1
    bn = n // t2

    error_matrix = re_pos_Img.copy()
    block_index = 0
    LSB_index = 0
    LSB_aux_index = 0

    for i in range(bm):
        for j in range(bn):
            block_index += 1
            bm1, bn1 = Index_to_bm_bn(block_index, bm, bn)

            r_start = (bm1 - 1) * t1
            c_start = (bn1 - 1) * t2
            block = error_matrix[r_start:r_start + t1, c_start:c_start + t2]

            MSB_value = MSB_num_cell[i][j]
            LSB_Len = 8 - MSB_value

            # Remove MSB planes contribution
            for k in range(1, MSB_value + 1):
                block = block - ((block // 2**(8 - k)) % 2) * 2**(8 - k)

            # LSB processing
            LSB_Label = LSB_label_Array[LSB_index:LSB_index + LSB_Len]
            LSB_index += LSB_Len

            block = block_plane_recover(block, LSB_Label)

            # Process auxiliary LSB info
            for k in range(LSB_Len):
                if LSB_Label[k] == 1:
                    value = LSB_aux_Array[LSB_aux_index]
                    LSB_aux_index += 1

                    num = bin_to_dec(LSB_aux_Array[LSB_aux_index:LSB_aux_index + 2], 2)
                    LSB_aux_index += 2

                    if num == 0:
                        block = block - ((block // 2**(LSB_Len - k - 1)) % 2) * 2**(LSB_Len - k - 1)
                        block += (1 - value) * 2**(LSB_Len - k - 1)
                    else:
                        plane = np.ones((t1, t2), dtype=int) * (1 - value)
                        pos_bin_x = ceil(log2(t1))
                        pos_bin_y = ceil(log2(t2))
                        for x in range(num):
                            x_Pos = bin_to_dec(LSB_aux_Array[LSB_aux_index:LSB_aux_index + pos_bin_x], pos_bin_x)  # zero-based in Python
                            LSB_aux_index += pos_bin_x
                            y_Pos = bin_to_dec(LSB_aux_Array[LSB_aux_index:LSB_aux_index + pos_bin_y], pos_bin_y)
                            LSB_aux_index += pos_bin_y
                            plane[x_Pos, y_Pos] = value

                        block = block - ((block // 2**(LSB_Len - k - 1)) % 2) * 2**(LSB_Len - k - 1)
                        block = block + plane * 2**(LSB_Len - k - 1)

            error_matrix[r_start:r_start + t1, c_start:c_start + t2] = block

    return error_matrix
