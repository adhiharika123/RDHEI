
def dec_to_bin(dec, bit_num):
    """
    Convert a decimal number to a binary list of length bit_num.

    Args:
        dec (int): Decimal number to convert.
        bit_num (int): Number of bits in output binary list.

    Returns:
        list: Binary list representing the decimal number.
    """
    bin_list = []
    for i in range(bit_num):
        bit = (dec // (2 ** (bit_num - i - 1))) % 2
        bin_list.append(bit)
    return bin_list
