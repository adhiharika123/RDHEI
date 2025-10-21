
import numpy as np

def block_plane_recover(block, LSB_Label):
    """
    Recover the original bit-plane order within a block using the LSB label.

    Args:
        block (np.ndarray): 2D numpy array of the image block.
        LSB_Label (list or np.ndarray): Binary label list for bit planes.

    Returns:
        np.ndarray: Block with recovered bit-plane order.
    """
    this_block = block.copy()
    LSB_Len = len(LSB_Label)
    index_Array = list(range(1, LSB_Len + 1))  # 1-based indexing as in MATLAB

    LSB_Label = LSB_Label.copy()  # To avoid modifying original

    for i in range(LSB_Len):
        flag = False
        if LSB_Label[i] == 1:
            continue
        for j in range(i + 1, LSB_Len):
            if LSB_Label[j] == 1:
                a = index_Array[i]
                b = index_Array[j]
                index_Array[i] = b
                index_Array[j] = a
                LSB_Label[j] = 0
                LSB_Label[i] = 1
                flag = True
                break
        if not flag:
            break

    for i in range(LSB_Len):
        plane_index = index_Array[i]
        this_plane = (block // 2**(LSB_Len - i - 1)) % 2
        current_plane = (block // 2**(LSB_Len - plane_index)) % 2
        this_block = this_block - current_plane * 2**(LSB_Len - plane_index) + this_plane * 2**(LSB_Len - plane_index)

    return this_block
