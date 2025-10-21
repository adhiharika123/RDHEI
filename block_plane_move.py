
import numpy as np

def block_plane_move(block, LSB_label):
    """
    Reorder bit planes in the block based on LSB_label during the sorting process.

    Args:
        block (np.ndarray): 2D numpy array of the image block.
        LSB_label (list or np.ndarray): Binary label list for bit planes.

    Returns:
        np.ndarray: Modified block after bit-plane moves.
    """
    LSB_label = LSB_label.copy()
    length = len(LSB_label)
    for i in range(length):
        flag = False
        MSB1 = length - i
        if LSB_label[i] == 1:
            continue
        for j in range(i + 1, length):
            MSB2 = length - j
            if LSB_label[j] == 1:
                a = (block // 2 ** (MSB1 - 1)) % 2
                b = (block // 2 ** (MSB2 - 1)) % 2
                block = block - a * 2 ** (MSB1 - 1) - b * 2 ** (MSB2 - 1) + a * 2 ** (MSB2 - 1) + b * 2 ** (MSB1 - 1)
                LSB_label[j] = 0
                LSB_label[i] = 1
                flag = True
                break
        if not flag:
            break
    return block
