import cv2
import numpy as np

from PIL import Image


def match(target,template):
    target=Image.open(target).convert('RGB')
    target.save("./slide_code/target1.jpg")
    target="./slide_code/target1.jpg"
    template=Image.open(template).convert('RGB')
    template.save('./slide_code/template1.jpg')
    template='./slide_code/template1.jpg'
    img_rgb = cv2.imread(target)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    img_gray=abs(255-img_gray)
    template = cv2.imread(template,0)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    x, y = np.unravel_index(res.argmax(), res.shape)
    # cv2.rectangle(template, (y, x), (y+w, x+h), (7, 249, 151), 2)
    return y

def get_tracks(distance):
    print(distance)
    distance += 20
    v = 0
    t = 0.2
    forward_tracks = []
    current = 0
    mid = distance * 3 / 5
    while current < distance:
        if current < mid:
            a = 2
        else:
            a = -3
        s = v * t + 0.5 * a * (t ** 2)
        v = v + a * t
        current += s
        forward_tracks.append(round(s))

    back_tracks = [-3, -3, -2, -2, -2, -2, -2, -1, -1, -1]
    return {'forward_tracks': forward_tracks, 'back_tracks': back_tracks}
