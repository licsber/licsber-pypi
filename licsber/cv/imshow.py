import matplotlib.pyplot as plt


def imshow(img):
    if img.shape[2] != 3:
        plt.imshow(img)
        return

    b, g, r = cv2.split(img)
    rgb = cv2.merge([r, g, b])
    plt.imshow(rgb)
