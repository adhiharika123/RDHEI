
import numpy as np
from math import ceil, log2
from dec_to_bin import dec_to_bin


def Pre_aux_block(error_block, t1, t2):
    same_MSB = 0
    LSB_label = []
    LSB_aux_info = []

    # Find number of leading MSB planes with all zeros
    for i in range(1, 9):
        wg = 2 ** (8 - i)
        plane_block = np.floor_divide(error_block, wg)
        if np.any(plane_block == 1):
            break
        same_MSB += 1

    # Find threshold max_limit
    max_limit = 0
    for i in range(1, t1 * t2 + 1):
        all_acc_num = 1 + ceil(log2(i + 1)) + i * (ceil(log2(t1)) + ceil(log2(t2)))
        if all_acc_num >= t1 * t2:
            max_limit = i - 1
            break

    limit_bit_num = ceil(log2(max_limit + 1))

    for i in range(same_MSB + 1, 9):  # MATLAB range inclusive, Python exclusive on end hence 9
        wg = 2 ** (8 - i)
        plane_block = np.floor_divide(error_block, wg) % 2

        num0 = np.sum(plane_block == 0)
        num1 = np.sum(plane_block == 1)

        value = 0 if num0 < num1 else 1
        min_value = min(num0, num1)

        if min_value <= max_limit:
            LSB_label.append(1)
            # Append value (0 or 1)
            LSB_aux_info.append(value)

            # Append binary representation of min_value
            emb_bin = dec_to_bin(min_value, limit_bit_num)
            LSB_aux_info.extend(emb_bin)

            position_num1 = ceil(log2(t1))
            position_num2 = ceil(log2(t2))

            # Append positions of pixels equal to value in binary form
            for x in range(t1):
                for y in range(t2):
                    if plane_block[x, y] == value:
                        x_bin = dec_to_bin(x, position_num1)
                        y_bin = dec_to_bin(y, position_num2)
                        LSB_aux_info.extend(x_bin)
                        LSB_aux_info.extend(y_bin)
        else:
            LSB_label.append(0)

    return same_MSB, LSB_label, LSB_aux_info
