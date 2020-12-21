import numpy as np
import cv2
import random
import os
import datetime
import string

SAVE_DIR = './static/images/'
ALL_SAVE_DIR = './static/images/all/'

class MyImage(object):

    # 画像を保存する
    def save(img):
        now = datetime.datetime.now()
        img_name = now.strftime('%Y%m%d_%H%M%S') + '.jpg'
        save_path = os.path.join(SAVE_DIR, img_name)
        cv2.imwrite(save_path, img)
        return save_path

    # 画像サイズを取得する
    def get_size(img):
        height, width, channels = img.shape[:3]
        return height, width, channels

    def mkdir_all_img():
        # ディレクトリを作成する
        now = datetime.datetime.now()
        dir_name = now.strftime('%Y%m%d_%H%M%S')
        dir_path = os.path.join(ALL_SAVE_DIR, dir_name)
        all_img_path = dir_path
        os.mkdir(dir_path)
        return all_img_path

    def all_save(img, all_img_path, index):
        img_name = index + '.jpg'
        save_path = os.path.join(all_img_path, img_name)
        cv2.imwrite(save_path, img)