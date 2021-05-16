import math
import cv2 as cv
import numpy as np
from mask_finder import init_trackbars, get_mask_limits



def get_point_by_mask(mask):
    contours, hierarchy = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    max_area = 0
    max_cnt = None
    for cnt in contours:
        area = cv.contourArea(cnt)
        if area > max_area:
            max_area = area
            max_cnt = cnt
    # get the highest point of contour
    if max_area>100:
        ext_top = tuple(max_cnt[max_cnt[:, :, 1].argmin()][0])
        return ext_top
    return 0,0

def crop_and_warp(img, corners, width, height):
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    matrix = cv.getPerspectiveTransform(corners, pts2)
    return cv.warpPerspective(img, matrix, (width, height))

def show_area(img, corners):
    area_preview = img.copy()
    for pt in corners:
        cv.circle(area_preview, (int(pt[0]), int(pt[1])), 10, (0,0,0), -1)
    cv.imshow('Area limits', area_preview)

def init_camera():        
    capture = cv.VideoCapture(0)
    capture.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
    capture.set(cv.CAP_PROP_FRAME_HEIGHT, 720)
    capture.set(cv.CAP_PROP_BRIGHTNESS, 180)
    capture.set(cv.CAP_PROP_CONTRAST, 50)
    capture.set(cv.CAP_PROP_SATURATION, 200)
    capture.set(cv.CAP_PROP_GAIN, 200)
    return capture



if __name__ == "__main__":

    capture = init_camera()

    # limits for blue pen
    low_blue = np.array([90, 55, 0])
    up_blue = np.array([179, 255, 255])

    # canvas init
    width, height = 500, 350
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
        img = cv.flip(img, -1) 
        imgHSV = cv.cvtColor(img, cv.COLOR_BGR2HSV)

        # low, up = get_mask_limits()
        mask = cv.inRange(imgHSV, low_blue, up_blue)
        point = get_point_by_mask(mask)
        
        # visualisation on original but warped image
        img_masked = cv.bitwise_and(img, img, mask=mask)
        cv.circle(img_masked, point, 5, (0,0, 255), 1)
        cv.imshow('Masked with point', img_masked)

        # draw on canvas
        dist = math.dist(point, last_point)
        if dist > 2 and dist<20:
            x, y =int((point[0]+last_point[0])/2), int((point[1]+last_point[1])/2)
            cv.line(canvas, (x,y), last_point, (255,0,0), 5)
            last_point =(x,y)
        else:
            last_point = point

        cv.imshow('Canvas',canvas)    

        if cv.waitKey(1) & 0xFF == ord('d'):
            break

    capture.release()
    cv.destroyAllWindows()

# TODO
# check if pen touch paper
# precise drawing
# area auto detect
# ui
