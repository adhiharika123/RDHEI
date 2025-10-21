
import numpy as np


def EncryptionImg(Img, Encryption_key):
    """
    Encrypt the image using bitwise XOR with a pseudo-random byte matrix based on the encryption key.

    Args:
        Img (np.ndarray): Input grayscale image (2D numpy array).
        Encryption_key (int): Key used to seed the random number generator.

    Returns:
        np.ndarray: Encrypted image (2D numpy array, uint8).
    """
    m, n = Img.shape
    En_Img = Img.copy()

    # Convert to uint8 if not already
    En_Img = En_Img.astype(np.uint8)

    np.random.seed(Encryption_key)
    E = np.round(np.random.rand(m, n) * 255).astype(np.uint8)

    En_Img = np.bitwise_xor(En_Img, E)

    return En_Img

