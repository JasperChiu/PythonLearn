import logging

import cv2
import numpy as np
from model.img_preprocessing import ImgPreprocessing
from model.img_noise_remove import ImgNoiseRemove
from model.draw_frame_line import DrawFrameLine

class ImgProcess:
    def img_process(self, imgs, resize_ratio, filter_size, dilate_iter, min_area_size, indent):
        for x in imgs:
            origin_img = x
            img, contours = ImgPreprocessing().img_preprocessing(origin_img, resize_ratio, filter_size, dilate_iter)
            contours_list = ImgNoiseRemove().img_noise_remove(img, contours, min_area_size, indent)

            mask = np.zeros(img.shape, np.uint8)  # 先建立全黑的遮罩(也可以全白啦，思路相同)
            for i in contours_list:
                mask = cv2.drawContours(mask, contours, i, (255, 255, 255), -1)
            # dst = cv2.drawContours(img, contours, -1, (255, 0, 0), 3)
            mask_reverse = (np.ones(img.shape, dtype=np.uint8) * 255) - mask
            mask_reverse = cv2.resize(mask_reverse, (origin_img.shape[1], origin_img.shape[0]))  # 遮罩resize回原圖尺寸大小
            img_add = cv2.add(origin_img, mask_reverse)
        return img_add

