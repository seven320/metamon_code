#encoding utf-8
#褒めたもんの色を変化できる。
from PIL import Image
image = Image.open('metamon.jpeg')
image.show() #変更前のカビゴンの画像を表示
r, g, b = image.split() #Red, Green, Blueの三原色に分離させる。
print(type(r))
# r = 200
# b = 0
# g = 0
# convert_image = Image.merge("RGB", (b, g, r)) #r, g, b→b, g, rに変更。つまり青→赤に変更。
# convert_image.save('metamon01.png');
# convert_image.show() #変更後のカビゴンの画像を表示
