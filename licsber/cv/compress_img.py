import cv2
import numpy as np


def comp_2d(image_2d, rate):
    height, width = image_2d.shape[:2]

    mean_array = np.mean(image_2d, axis=1)
    mean_array = mean_array[:, np.newaxis]
    mean_array = np.tile(mean_array, width)

    cov_mat = image_2d.astype(np.float64) - mean_array
    eig_val, eig_vec = np.linalg.eigh(np.cov(cov_mat))
    p = np.size(eig_vec, axis=1)
    idx = np.argsort(eig_val)
    idx = idx[::-1]
    eig_vec = eig_vec[:, idx]
    numpc = rate
    if numpc < p or numpc > 0:
        eig_vec = eig_vec[:, range(numpc)]
    score = np.dot(eig_vec.T, cov_mat)
    recon = np.dot(eig_vec, score) + mean_array
    recon_img_mat = np.uint8(np.absolute(recon))
    return recon_img_mat


def compress_img(content, rate=30):
    data = cv2.imdecode(np.frombuffer(content, np.uint8), cv2.IMREAD_COLOR)
    a_g = data[:, :, 0]
    a_b = data[:, :, 1]
    a_r = data[:, :, 2]
    g_recon, b_recon, r_recon = comp_2d(a_g, rate), comp_2d(a_b, rate), comp_2d(a_r, rate)
    result = cv2.merge([g_recon, b_recon, r_recon])
    return result.tobytes()
