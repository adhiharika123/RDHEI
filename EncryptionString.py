
import numpy as np

def EncryptionString(string, Encryption_key):
    """
    Encrypt a binary string using a pseudo-random binary mask seeded by the encryption key.

    Args:
        string (list or np.ndarray): Input binary string/list of 0s and 1s.
        Encryption_key (int): Key to seed the random number generator.

    Returns:
        np.ndarray: Encrypted binary string as a numpy array.
    """
    length = len(string)
    EncryptedString = np.array(string, dtype=np.uint8)

    np.random.seed(Encryption_key)
    E = np.round(np.random.rand(length)).astype(np.uint8)

    EncryptedString = np.bitwise_xor(EncryptedString, E)

    return EncryptedString
