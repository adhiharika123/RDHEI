# arithmetic_coding.py
from collections import Counter
from decimal import Decimal, getcontext
import numpy as np

getcontext().prec = 60  # High precision for fractional range arithmetic

def arithmetic_encode(symbols):
    """Return (encoded_value, freq_dict, total)"""
    freq = Counter(symbols)
    total = sum(freq.values())
    low, high = Decimal(0), Decimal(1)
    cum_low = {}
    cum_high = {}
    cum = Decimal(0)
    for s, f in sorted(freq.items()):
        p = Decimal(f) / Decimal(total)
        cum_low[s] = cum
        cum_high[s] = cum + p
        cum = cum_high[s]
    for s in symbols:
        width = high - low
        high = low + width * cum_high[s]
        low = low + width * cum_low[s]
    code = (low + high) / 2
    return code, freq, total

def arithmetic_decode(code, freq, total, n_symbols):
    low, high = Decimal(0), Decimal(1)
    cum_low = {}
    cum_high = {}
    cum = Decimal(0)
    for s, f in sorted(freq.items()):
        p = Decimal(f) / Decimal(total)
        cum_low[s] = cum
        cum_high[s] = cum + p
        cum = cum_high[s]

    out = []
    for _ in range(n_symbols):
        value = (code - low) / (high - low)
        for s in sorted(freq.keys()):
            if cum_low[s] <= value < cum_high[s]:
                out.append(s)
                width = high - low
                high = low + width * cum_high[s]
                low = low + width * cum_low[s]
                break
    return out
