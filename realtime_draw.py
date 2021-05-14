import cv2 as cv
import numpy as np
import math
from mask_finder import init_trackbars, get_mask_limits


def get_point(img):
    contours, hierarchy = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    max_area = 0
    max_cnt = None
    for cnt in contours:
        area = cv.contourArea(cnt)
        if area > max_area:
            max_area = area
            max_cnt = cnt
    if max_area>100:
        extBot = tuple(max_cnt[max_cnt[:, :, 1].argmax()][0])
        return extBot
    return 0,0


def crop_and_warp(img, corners, width, height):
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    matrix = cv.getPerspectiveTransform(corners, pts2)
    return cv.warpPerspective(img, matrix, (width, height))

def show_area(img, corners):
    area_preview = img.copy()
    for pt in corners:
        cv.circle(area_preview, (pt[0], pt[1]), 10, (0,0,0), -1)
    cv.imshow('Area limits', area_preview)

            

capture = cv.VideoCapture(0)

capture.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
capture.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

width, height = 500, 400

# limits for blue pen
low_blue = np.array([80, 110, 0])
up_blue = np.array([179, 255, 255])

canvas = np.zeros((height,width,3), np.uint8)
canvas[:,:]=(255,255,255)

# init_trackbars()
last_point = (0,0)

while True:
    isTrue, frame = capture.read()
    frame = cv.flip(frame, 1)
    # points for crop and warp 
    corners = np.float32([[352, 336], [1062, 336], [146, 438], [1166, 447]])
    
    show_area(frame, corners)
    img = crop_and_warp(frame, corners, width, height)
   
    imgHSV = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    # low, up = get_mask_limits()
    mask = cv.inRange(imgHSV, low_blue, up_blue)
    point = get_point(mask)

    # result on original warped image
    img_masked = cv.bitwise_and(img, img, mask=mask)
    cv.circle(img_masked, point, 5, (0,0, 255), 1)
    cv.imshow('Masked with point', img_masked)

    # draw on canvas
    if math.dist(point, last_point)<20:
        cv.line(canvas, point, last_point, (0,0,0), 5)
    last_point = point

    cv.imshow('Canvas', cv.flip(canvas, -1))
    cv.imshow('Mask', mask)
    

    if cv.waitKey(1) & 0xFF == ord('d'):
        break

capture.release()
cv.destroyAllWindows()

# TODO
# check if pen touch paper
# precise drawing
# area auto detect
# ui
