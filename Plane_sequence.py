
from Index_to_bm_bn import Index_to_bm_bn
def Plane_sequence(block, t1, t2, layer, num):
    """
    Extract bits from a specific bit-plane 'layer' of the block sequentially.

    Args:
        block (np.ndarray): 2D numpy array representing the image block.
        t1 (int): block height.
        t2 (int): block width.
        layer (int): bit-plane layer (1 to 8).
        num (int): number of bits to extract.

    Returns:
        list: Extracted bit sequence from the specified bit-plane.
    """
    first_plane_sequence = []
    newBlock = (block // 2**(9 - layer - 1)) % 2

    for index in range(1, num + 1):
        i, j = Index_to_bm_bn(index, t1, t2)
        first_plane_sequence.append(newBlock[i - 1, j - 1])  # Adjust for zero-based indexing

    return first_plane_sequence
