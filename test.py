#encoding:utf-8

from PIL import Image, ImageFilter
import cv2

def change_color(image,color):
    pass

def show_image(image):
    pass


IMAGE_PATH = "/Users/kenkato/python/hometamon_twitter/image/hometamon.jpg"
image = cv2.imread(IMAGE_PATH,1)
cv2.imshow("image",image)

cv2.waitKey(0)
cv2.destroyAllWindows()
