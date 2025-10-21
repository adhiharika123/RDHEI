import numpy as np

def Recover_error_matrix(error_matrix, error_sign_label):
    m, n = error_matrix.shape
    # Convert to int16 for safe arithmetic without overflow
    recoverImg = error_matrix.astype(np.int16).copy()
    index = 0

    for i in range(m):
        for j in range(n):
            if i == 0 and j == 0:
                continue
            error_sign = error_sign_label[index]
            error = np.int16(error_matrix[i, j])
            if error_sign == 1:
                error = -error

            if i == 0:
                recoverImg[i, j] = recoverImg[i, j - 1] - error
            elif j == 0:
                recoverImg[i, j] = recoverImg[i - 1, j] - error
            else:
                a = recoverImg[i - 1, j - 1]
                b = recoverImg[i - 1, j]
                c = recoverImg[i, j - 1]
                if a <= min(b, c):
                    predict_value = max(b, c)
                elif a >= max(b, c):
                    predict_value = min(b, c)
                else:
                    predict_value = b + c - a
                recoverImg[i, j] = predict_value - error

            index += 1

    # Clip to valid pixel range and convert back to uint8
    recoverImg = np.clip(recoverImg, 0, 255).astype(np.uint8)
    return recoverImg