
import numpy as np
from Index_to_bm_bn import Index_to_bm_bn

def Embed_plane_seq(block, t1, t2, layer, num, data):
    """
    Embed bits (data) sequentially into a specified bit-plane layer of the given block.

    Args:
        block (np.ndarray): 2D numpy array of the image block.
        t1 (int): block height.
        t2 (int): block width.
        layer (int): bit-plane layer (1 is MSB).
        num (int): number of bits to embed.
        data (list or np.ndarray): binary data bits to embed.

    Returns:
        np.ndarray: new block with embedded data.
    """

    new_block = block.copy()
    for i in range(num):
        bm1, bn1 = Index_to_bm_bn(i + 1, t1, t2)  # MATLAB 1-based indexing

        # Extract the bit value at the specified bit-plane layer
        # Layer counting from MSB: 8-layer in bits numbering (bit 7 is highest)
        bit_val = (new_block[bm1 - 1, bn1 - 1] // 2**(8 - layer)) % 2

        if bit_val != data[i]:
            if data[i] == 1:
                new_block[bm1 - 1, bn1 - 1] += 2**(8 - layer)
            else:
                new_block[bm1 - 1, bn1 - 1] -= 2**(8 - layer)

    return new_block
