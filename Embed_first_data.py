import numpy as np
from math import floor, ceil, log2

from Embed_plane_seq import Embed_plane_seq
def Embed_first_data(info_index, Aux_Len, All_emb_info, data, this_block, t1, t2, M, position):
    """
    Embed auxiliary data into the specified block layer considering auxiliary length and position.

    Args:
        info_index (int): Current info index.
        Aux_Len (int): Auxiliary information length.
        All_emb_info (list or np.ndarray): All embedded info bits.
        data (list or np.ndarray): Data bits to embed.
        this_block (np.ndarray): Current image block (2D numpy array).
        t1 (int): Block height.
        t2 (int): Block width.
        M (int): Bit-plane layer.
        position (int): Current position offset in data.

    Returns:
        new_block (np.ndarray): Block with embedded data.
        Embed_len (int): Number of bits embedded in this operation.
    """
    Embed_len = info_index - Aux_Len

    if Aux_Len == 0:
        block_data = data[position:position + Embed_len]
    else:
        start_index = Aux_Len - (t1 * t2 - Embed_len)
        block_data = list(All_emb_info[start_index:Aux_Len]) + list(data[position:position + Embed_len])

    new_block = Embed_plane_seq(this_block, t1, t2, M, t1 * t2, block_data)

    return new_block, Embed_len
