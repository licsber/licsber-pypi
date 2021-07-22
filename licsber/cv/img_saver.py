import os
import time
import uuid

import cv2


def take_and_save(save_path: str):
    def save(img):
        uid3 = uuid.uuid3(uuid.NAMESPACE_OID, str(time.time()))
        filename = f"{uid3}.jpg"
        filepath = os.path.join(save_path, filename)
        print(f"保存: {filepath}")
        cv2.imwrite(filepath, img)

    cap = cv2.VideoCapture(1)
    while True:
        _, bgr = cap.read()
        cv2.imshow('bgr', bgr)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('k'):
            key = cv2.waitKey(0)
            if key == ord('k'):
                save(bgr)
