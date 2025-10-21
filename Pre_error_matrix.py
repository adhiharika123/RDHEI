# Pre_error_matrix.py (CNN-based version)
import numpy as np
import torch

# Define CNN model (same architecture used during training)
class PredictionCNN(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.net = torch.nn.Sequential(
            torch.nn.Conv2d(1, 32, 3, padding=1), torch.nn.ReLU(),
            torch.nn.Conv2d(32, 64, 3, padding=1), torch.nn.ReLU(),
            torch.nn.Conv2d(64, 32, 3, padding=1), torch.nn.ReLU(),
            torch.nn.Conv2d(32, 1, 1)
        )

    def forward(self, x):
        return self.net(x)

# Path to your trained model (relative to this file)
MODEL_PATH = "cnn_predictor.pth"
PATCH_SIZE = 7

def Pre_error_matrix(cover):
    """
    Input:  cover -> 2D numpy array (uint8)
    Output: error_matrix (absolute), error_sign_label (binary)
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    m, n = cover.shape
    pad = PATCH_SIZE // 2

    # Load trained model
    model = PredictionCNN().to(device)
    model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
    model.eval()

    # Normalize input
    img_norm = cover.astype(np.float32) / 255.0
    padded = np.pad(img_norm, pad, mode="reflect")

    pred_img = np.zeros_like(img_norm, dtype=np.float32)
    batch_patches = []
    batch_coords = []
    BATCH_SZ = 2048

    # Sliding window inference
    for i in range(pad, pad + m):
        for j in range(pad, pad + n):
            patch = padded[i - pad:i + pad + 1, j - pad:j + pad + 1]
            batch_patches.append(patch)
            batch_coords.append((i - pad, j - pad))
            if len(batch_patches) >= BATCH_SZ:
                _predict_batch(batch_patches, batch_coords, model, device, pred_img)
                batch_patches, batch_coords = [], []

    if batch_patches:
        _predict_batch(batch_patches, batch_coords, model, device, pred_img)

    pred_vals = np.clip(np.round(pred_img * 255.0), 0, 255).astype(np.int16)
    cover_int = cover.astype(np.int16)

    error_matrix = np.zeros((m, n), dtype=np.int16)
    error_sign_label = np.zeros(m * n - 1, dtype=np.int8)
    idx = 0

    for i in range(m):
        for j in range(n):
            if i == 0 and j == 0:
                error_matrix[0, 0] = 0
                continue
            pv = int(pred_vals[i, j])
            error = pv - int(cover_int[i, j])
            if error < 0:
                error_sign_label[idx] = 1
                error_matrix[i, j] = -error
            else:
                error_sign_label[idx] = 0
                error_matrix[i, j] = error
            idx += 1

    return error_matrix, error_sign_label


def _predict_batch(patches, coords, model, device, pred_img):
    X = np.stack(patches, axis=0).astype(np.float32)
    X = np.expand_dims(X, axis=1)
    with torch.no_grad():
        preds = model(torch.tensor(X).to(device)).cpu().numpy()
    c = X.shape[2] // 2
    for k, (r, cpos) in enumerate(coords):
        pred_img[r, cpos] = preds[k, 0, c, c]
