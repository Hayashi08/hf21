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
        img_name = now.strftime('%Y%m%d_%H%M%S') + '.jpeg'
        save_path = os.path.join(SAVE_DIR, img_name)
        cv2.imwrite(save_path, img)
        return img_name