# Arithmetic_decode.py
# Integer-based decoder matching Arithmetic_encode.py

def arithmetic_decode(encoded_bytes, num_symbols, original_symbols):
    """
    encoded_bytes: bytes produced by arithmetic_encode
    num_symbols: number of symbols encoded (len of original sequence)
    original_symbols: list of symbols in the same sorted order used for encoding
    Returns: list of decoded symbols
    """
    if len(encoded_bytes) < 8:
        raise ValueError("Encoded bytes too short")

    code_value = int.from_bytes(encoded_bytes[:8], 'big')
    freq_bytes = encoded_bytes[8:]
    # freq_bytes should be 4 * len(original_symbols)
    sym_count = len(original_symbols)
    if len(freq_bytes) < 4 * sym_count:
        raise ValueError("Frequency table length mismatch")

    freqs = []
    for i in range(sym_count):
        f = int.from_bytes(freq_bytes[4*i:4*i+4], 'big')
        freqs.append(f)

    total = sum(freqs)
    if total == 0:
        # nothing encoded -> return list of zeros? or empty list depending on convention.
        return [sorted(original_symbols)[0]] * num_symbols if num_symbols>0 else []

    # build cumulative
    cum = []
    running = 0
    for f in freqs:
        cum.append(running)
        running += f
    total = running

    low = 0
    high = (1 << 64) - 1
    value = code_value

    decoded = []
    sorted_syms = sorted(original_symbols)
    for _ in range(num_symbols):
        range_ = high - low + 1
        # scaled value in [0, total-1]
        scaled = ((value - low + 1) * total - 1) // range_
        # find symbol whose cum <= scaled < cum+freq
        # linear scan is fine for small alphabets (here 9 symbols)
        for idx, sym in enumerate(sorted_syms):
            if cum[idx] <= scaled < cum[idx] + freqs[idx]:
                decoded.append(sym)
                # update interval
                sym_low = cum[idx]
                sym_high = cum[idx] + freqs[idx]
                high = low + (range_ * sym_high) // total - 1
                low  = low + (range_ * sym_low)  // total
                break
        else:
            # shouldn't happen
            raise ValueError("Decoding failed to find symbol for scaled value")
    return decoded
