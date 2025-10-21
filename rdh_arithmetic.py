# Arithmetic_encode.py
# Integer-based lossless arithmetic encoder (compatible with Arithmetic_decode.py)

from collections import Counter

def arithmetic_encode(symbols, original_symbols):
    """
    symbols: list of integer symbols (e.g., 0..8)
    original_symbols: list of all possible symbols in sorted order (e.g., list(range(9)))
    Returns: bytes = 8-byte code_value || (4 bytes per symbol) frequency table
    """
    # Build frequency table in order of original_symbols
    freqs_counter = Counter(symbols)
    freqs = [int(freqs_counter.get(s, 0)) for s in sorted(original_symbols)]
    total = sum(freqs)
    if total == 0:
        # nothing encoded - return empty frequencies (still must be decodable)
        freq_bytes = b''.join((0).to_bytes(4, 'big') for _ in freqs)
        code_bytes = (0).to_bytes(8, 'big')
        return code_bytes + freq_bytes

    # cumulative freq for each symbol
    cum = []
    running = 0
    for f in freqs:
        cum.append(running)
        running += f
    total = running  # total count
    # integer range coder parameters
    low = 0
    high = (1 << 64) - 1  # 64-bit precision

    for sym in symbols:
        # index of sym in sorted(original_symbols)
        idx = sorted(original_symbols).index(sym)
        range_ = high - low + 1
        sym_low = cum[idx]
        sym_high = cum[idx] + freqs[idx]
        # update interval
        high = low + (range_ * sym_high) // total - 1
        low  = low + (range_ * sym_low)  // total

    code_value = (low + high) // 2
    code_bytes = int(code_value).to_bytes(8, 'big')
    # pack freq table as 4-byte unsigned ints in the same order
    freq_bytes = b''.join(int(f).to_bytes(4, 'big') for f in freqs)
    return code_bytes + freq_bytes
