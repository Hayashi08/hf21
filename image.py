import numpy as np
import cv2
import random
import os
import datetime
import string

SAVE_DIR = './static/images/'

class MyImage(object):
    # 画像を保存する
    def save(img):
        now = datetime.datetime.now()
        img_name = now.strftime('%Y%m%d_%H%M%S') + '.jpg'
        save_path = os.path.join(SAVE_DIR, img_name)
        cv2.imwrite(save_path, img)
        return save_path

    def get_size(img):
        height, width, channels = img.shape[:3]
        return height, width, channels