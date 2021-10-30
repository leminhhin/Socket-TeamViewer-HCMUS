import numpy as np
import cv2
from mss import mss
from PIL import Image

mon = {'left': 0, 'top': 0, 'width': 1440, 'height': 900}

SCREEN_SIZE = (1440, 900)
# define the codec
fourcc = cv2.VideoWriter_fourcc('X','2','6','4')
# create the video write object
out = cv2.VideoWriter("output.avi", fourcc, 20.0, (SCREEN_SIZE))

sct = mss()

while True:
    sct_img = sct.grab(mon)
    frame = np.array(sct_img)
    cv2.imshow('screen', frame)
    out.write(frame)
    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break

out.release()
cv2.destroyAllWindows()