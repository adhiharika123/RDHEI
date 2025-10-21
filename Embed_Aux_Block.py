
import numpy as np
from Embed_plane_seq import Embed_plane_seq

def Embed_Aux_Block(block, t, MSB_value, block_LSB_label, data):
    """
    Embed auxiliary data into specified bit-planes of a block.

    Args:
        block (np.ndarray): Input image block (2D array).
        t (int): block size (height and width).
        MSB_value (int): Number of most significant bit planes to embed data.
        block_LSB_label (list or np.ndarray): Binary labels for LSB planes (length 8).
        data (list or np.ndarray): Binary data to embed.

    Returns:
        np.ndarray: Block with embedded auxiliary data.
    """
    embed_aux_block = block.copy()
    dataLen = len(data)
    index = 0
    flag = False

    Embed_Index_Array = np.concatenate((np.ones(MSB_value, dtype=int), np.array(block_LSB_label, dtype=int)))

    for i in range(8):
        if Embed_Index_Array[i] == 1:
            layer = i + 1  # MATLAB is 1-based, Python index +1
            if index + t*t > dataLen:
                plane_data = data[index:dataLen]
                num = dataLen - index
                flag = True
            else:
                plane_data = data[index:index + t*t]
                num = t*t

            index += t*t

            # Embed data into the specified bit-plane 'layer' of the block
            new_block = Embed_plane_seq(embed_aux_block, t, layer, num, plane_data)
            embed_aux_block = new_block

            if flag:
                break

    return embed_aux_block
