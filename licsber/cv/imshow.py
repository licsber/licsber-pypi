import cv2
import matplotlib.pyplot as plt


def imshow(img):
    """
    转换奇怪的bgr和rgb
    :param img: numpy array
    """
    if len(img.shape) != 3:
        plt.imshow(img)
        return

    b, g, r = cv2.split(img)
    rgb = cv2.merge([r, g, b])
    plt.imshow(rgb)
