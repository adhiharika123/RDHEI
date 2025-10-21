
import numpy as np

def psnr(ImageA, ImageB):
    """
    Calculate the PSNR (Peak Signal-to-Noise Ratio) between two images.

    Args:
        ImageA (np.ndarray): First image array.
        ImageB (np.ndarray): Second image array.

    Returns:
        float: PSNR value in decibels (dB).
    """
    if ImageA.shape != ImageB.shape:
        raise ValueError("ImageA and ImageB must have the same dimensions.")

    M, N = ImageA.shape
    ImageA = ImageA.astype(np.float64)
    ImageB = ImageB.astype(np.float64)

    mse = np.sum((ImageA - ImageB) ** 2)
    mse /= (M * N)

    if mse == 0:
        return float('inf')  # Images are identical

    max_pixel = 255.0
    psnr_value = 10 * np.log10((max_pixel ** 2) / mse)

    return psnr_value
