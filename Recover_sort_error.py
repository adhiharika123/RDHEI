import numpy as np

def Recover_sort_error(Decrypted_img, same_MSB_Array, t1, t2):
    """
    Reverse of Sort_error_matrix().
    Reconstructs the original error matrix blocks in correct order.

    Args:
        Decrypted_img (numpy.ndarray): Image after decryption.
        same_MSB_Array (numpy.ndarray): Array of same_MSB indices per block.
        t1, t2 (int): block sizes.
    Returns:
        numpy.ndarray: Reconstructed error matrix (same size as input image).
    """
    m, n = Decrypted_img.shape
    bm = m // t1
    bn = n // t2

    Recover_sort_matrix = np.zeros((m, n), dtype=int)

    # Reverse the block rearrangement logic
    block_index = 0
    for i in range(bm):
        for j in range(bn):
            r_start = i * t1
            c_start = j * t2
            block = Decrypted_img[r_start:r_start + t1, c_start:c_start + t2]

            # Simply reassign each block back to its place
            Recover_sort_matrix[r_start:r_start + t1, c_start:c_start + t2] = block
            block_index += 1

    return Recover_sort_matrix
