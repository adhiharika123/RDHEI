import numpy as np
from math import floor
from Index_to_bm_bn import Index_to_bm_bn
from block_plane_move import block_plane_move



def Sort_error_matrix(error_matrix, same_MSB_Array, LSB_label_cell, t1, t2):
    m, n = error_matrix.shape
    bm = m // t1
    bn = n // t2

    sort_error_matrix = error_matrix.copy()
    block_index = 1

    for i in range(8, -1, -1):  # from 9 down to 1 in MATLAB, so 8 down to 0 in Python
        for j in range(bm):
            for k in range(bn):
                if same_MSB_Array[j, k] == i:
                    LSB_label = LSB_label_cell[j][k]
                    bm1, bn1 = Index_to_bm_bn(block_index, bm, bn)

                    if np.sum(np.array(LSB_label) == 1) != 0:
                        r_start = j * t1
                        c_start = k * t2
                        block = error_matrix[r_start:r_start + t1, c_start:c_start + t2]
                        this_block = block_plane_move(block, LSB_label)
                    else:
                        r_start = j * t1
                        c_start = k * t2
                        this_block = error_matrix[r_start:r_start + t1, c_start:c_start + t2]

                    r_start_dst = (bm1 - 1) * t1
                    c_start_dst = (bn1 - 1) * t2
                    sort_error_matrix[r_start_dst:r_start_dst + t1, c_start_dst:c_start_dst + t2] = this_block
                    block_index += 1

    if block_index != bm * bn + 1:
        print("An error occurred while sorting error_matrix")

    return sort_error_matrix