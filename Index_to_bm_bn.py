def Index_to_bm_bn(index, bm, bn):
    """
    Convert a linear block index to block row (bm1) and column (bn1) indices.

    Args:
        index (int): Linear block index (1-based).
        bm (int): Number of block rows.
        bn (int): Number of block columns.

    Returns:
        tuple: (bm1, bn1) block row and column indices (1-based).
    """
    if index % bn == 0:
        bm1 = index // bn
    else:
        bm1 = index // bn + 1
    bn1 = index - (bm1 - 1) * bn
    return bm1, bn1
