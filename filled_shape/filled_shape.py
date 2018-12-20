import cv2 as cv
import numpy as np


class FilledShape:
    def __init__(self, img):
        self.img = img

    def detect(self, contour, debug):
        shape = "undefined"
        epsilon = 0.03 * cv.arcLength(contour, True)
        approx = cv.approxPolyDP(contour, epsilon, True)
        x, y, w, h = cv.boundingRect(contour)
        cv.rectangle(self.img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv.rectangle(self.img, (x, y-10), (x + w, y + 10), (0, 0, 255), -1)
        font = cv.FONT_HERSHEY_SIMPLEX
        number = ""
        if debug:
            cv.drawContours(self.img, [contour], 0, (0, 255, 0), 2)

            for pt in approx:
                cv.circle(self.img, (pt[0][0], pt[0][1]), 5, (255, 0, 0), -1)
            number = str(len(approx)) + " "
        if len(approx) == 3:
            shape = "triangle"
        elif len(approx) == 4:
            # print(w, h, w / h)
            if 0.95 < w / h < 1.05:
                shape = "Square"
            else:
                shape = "Rectangle"
        elif len(approx) == 5:
            shape = "Pentagon"
        else:
            shape = "Circle"
        cv.putText(self.img, number + shape, (x, y), font, 0.4, (255, 255, 255), 1, cv.LINE_AA)

    def preprocessing_image(self):
        img_gray = cv.cvtColor(self.img, cv.COLOR_BGR2GRAY)
        _, threshold = cv.threshold(img_gray, 127, 255, 0)
        kernel = np.ones((5, 5), np.uint8)
        cv.dilate(threshold, kernel, iterations=1)
        threshold = cv.GaussianBlur(threshold, (15, 15), 0)
        img_contour, contours, _ = cv.findContours(threshold, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        return threshold, contours


def capture(frame, debug=False):
    img_object = FilledShape(frame)
    threshold, contours = img_object.preprocessing_image()
    for contour in contours:
        img_object.detect(contour, debug)
    cv.imshow('Threshold', threshold)
    cv.imshow('Original', frame)
