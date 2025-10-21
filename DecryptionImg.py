import numpy as np

def DecryptionImg(Img, Encryption_key):
    """
    Decrypt the image 'Img' using the Encryption_key.

    Args:
        Img (np.ndarray): Encrypted image as 2D numpy array (dtype uint8).
        Encryption_key (int): Key used for random number generation.

    Returns:
        np.ndarray: Decrypted image as 2D numpy array.
    """
    m, n = Img.shape
    De_Img = Img.copy()

    np.random.seed(Encryption_key)
    E = np.round(np.random.rand(m, n) * 255).astype(np.uint8)

    # Bitwise XOR between Img and random matrix E
    De_Img = np.bitwise_xor(Img, E)

    return De_Img
