import numpy as np

def DecryptionString(string, Encryption_key):
    """
    Decrypt a binary string using the given encryption key.

    Args:
        string (list or np.ndarray): Input binary string/list of 0s and 1s.
        Encryption_key (int): Key for the random seed.

    Returns:
        np.ndarray: Decrypted binary string as a NumPy array of 0s and 1s.
    """
    length = len(string)
    DecryptedString = np.array(string, dtype=np.uint8)

    np.random.seed(Encryption_key)
    E = np.round(np.random.rand(length)).astype(np.uint8)

    # Bitwise XOR between string and generated random binary vector E
    DecryptedString = np.bitwise_xor(DecryptedString, E)

    return DecryptedString
