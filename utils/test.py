# import cv2
# import numpy as np
#
#
# def test(image, labels, color=0):
#     unique_labels = np.unique(labels)
#
#     for label in unique_labels:
#         mask = np.uint8(labels == label)
#         contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#         cv2.drawContours(image, contours, -1, (0, 0, 0), 1)
#     return image
