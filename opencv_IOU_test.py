from matplotlib import pyplot as plt
import cv2
import numpy as np

def get_iou(bbox_ai, bbox_gt):
    iou_x = max(bbox_ai[0], bbox_gt[0]) # x
    iou_y = max(bbox_ai[1], bbox_gt[1]) # y
    iou_w = min(bbox_ai[2]+bbox_ai[0], bbox_gt[2]+bbox_gt[0]) - iou_x # w
    iou_w = max(iou_w, 0)
    print(f'{iou_w=}')
    iou_h = min(bbox_ai[3]+bbox_ai[1], bbox_gt[3]+bbox_gt[1]) - iou_y # h
    iou_h = max(iou_h, 0)
    print(f'{iou_h=}')

    iou_area = iou_w * iou_h
    print(f'{iou_area=}')
    all_area = bbox_ai[2]*bbox_ai[3] + bbox_gt[2]*bbox_gt[3] - iou_area
    print(f'{all_area=}')

    return max(iou_area/all_area, 0)

def show_img(img):
    image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(image_rgb)
    plt.show()

def draw_rectangle(img, bbox, color):
  left_up = (bbox[0], bbox[1])
  right_down =  (bbox[0]+bbox[2], bbox[1]+bbox[3])
  thickness = 1 # 寬度 (-1 表示填滿)
  cv2.rectangle(img, left_up, right_down, color, thickness)

  return img


shape = (100, 100, 3) # y, x, RGB

# 第一種方法，直接建立全白圖片 100*100
img = np.full(shape, 255).astype(np.uint8)

bbox_1 = [10, 20, 30, 40]
bbox_2 = [20, 30, 40, 50]

img = draw_rectangle(img, bbox_1, color=(0, 0, 255))
# show_img(img)
img = draw_rectangle(img, bbox_2, color=(0, 255, 0))
show_img(img)

print(get_iou(bbox_1, bbox_2))
