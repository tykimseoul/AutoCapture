from PIL import ImageGrab, Image
import numpy as np
import cv2
import time
import os


def is_different(imageA, imageB):
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    print(err)
    return err > 1000


def save_into_pdf():
    frames_path = './frames/'
    images = [Image.open(frames_path + image) for image in os.listdir(frames_path)]
    images[0].save('./result.pdf', save_all=True, append_images=images[1:])
    for image in os.listdir(frames_path):
        os.remove(frames_path + image)


def start():
    frame_number = -1
    prev_frame = None
    screen_size = ImageGrab.grab().size
    try:
        while True:
            img = ImageGrab.grab(bbox=(100, 10, screen_size[0], screen_size[1]))
            frame = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
            if frame_number == -1:
                prev_frame = frame
                frame_number += 1
            if is_different(frame, prev_frame):
                cv2.imwrite('./frames/frame_{}.jpg'.format(frame_number), frame)
                frame_number += 1
                prev_frame = frame
            time.sleep(1)
    except KeyboardInterrupt:
        save_into_pdf()


start()
