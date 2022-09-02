# from typing import final
import cv2
import classes.camera as camera
import time
import utils.box_detection as box_detection
import utils.circle_detection as circle_detection

def process(snaps, img):
    path_img = 'images/'
    img_box, img_blob = box_detection.process(img, 120, 255, 3)
    img_circle,num_circles = circle_detection.process(img, 1, 20,
                                                     75, 28, 5, 30)
    # print(num_circles)
    if snaps:
        cv2.imwrite(path_img+'capture.jpeg', img)
        cv2.imwrite(path_img+'box_detected.jpeg', img_box)
        cv2.imwrite(path_img+'circle_detected.jpeg', img_circle)
    
    cv2.imshow('capture', img)
    cv2.imshow('capture_blob', img_blob)
    cv2.imshow('box_detected', img_box)
    cv2.imshow('circle_detected', img_circle)

def main(mode):
    try:
        # recipe : 30hz, 15hz, 6hz
        pipeline = camera.Camera(640, 480, 30)

        if mode == 'snap':
            time.sleep(2)
            img = pipeline.take_snap()
            process(True, img)
            cv2.waitKey(0)

        if mode == 'online':
            while True:
                img = pipeline.take_snap()
                process(False, img)
                cv2.waitKey(1)
    finally:
        pipeline.stop()


if __name__ == '__main__':
    main('snap')
