import numpy as np
import cv2
from matplotlib import pyplot as plt


img = cv2.imread("../images/yosi_w_newtext.png")
img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
icon = cv2.imread("../images/icon.jpg")
icon = cv2.cvtColor(icon, cv2.COLOR_RGB2BGR)
icon_small = cv2.resize(icon, dsize=(100, 100), interpolation=cv2.INTER_CUBIC)

print(icon.shape, img.shape)

circle = np.zeros((100, 100, 3))
circle = cv2.circle(circle, (50, 50), 32, (1, 1, 1), thickness=-1)

circle = cv2.GaussianBlur(circle, (31, 31), 0)

for i in range(3):
    icon_small[:, :, i] = icon_small[:, :, i] * (
        np.sum(circle, axis=(2)) / 3
    ) + 255 * np.ones((100, 100)) * (1 - np.sum(circle, axis=(2)) / 3)


print(icon_small)
plt.imshow(icon_small)


plt.show()
