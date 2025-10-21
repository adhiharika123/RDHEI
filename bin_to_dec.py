
import numpy as np
def bin_to_dec(MSB_number_bin, size):
    """
    Convert a binary list/array to decimal integer.

    Args:
        MSB_number_bin (list or np.ndarray): Binary digits (0 or 1), length >= size.
        size (int): Number of bits to consider from MSB_number_bin.

    Returns:
        int: Decimal integer decoded from the binary input.
    """
    MSB_number_bin = np.array(MSB_number_bin).flatten()  # Flatten in case it's nested
    dec = 0
    for i in range(size):
        bit = int(MSB_number_bin[i])  # Now safe to convert to int
        dec += bit * 2 ** (size - i - 1)
    return dec
