import random
import cv2 as cv
import numpy as np


# Experimental function - temp not used
# Looks for 2 largest contours(>100) canny, if exist: pen probalby touches paper - returns point of contact
def canny_contact_detect(img, height, width):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blured = cv.GaussianBlur(gray, (5,5), 0)
    canny  = cv.Canny(blured, 70, 190)
    cv.imshow('Canny Edges', canny)
    kernel = np.ones((3,3), np.uint8)
    dil_erode = cv.dilate(canny,kernel,iterations = 3)
    dil_erode = cv.erode(dil_erode,kernel,iterations = 2)
    cv.imshow("Dilate and eroded", dil_erode)
    blank = np.zeros((height,width,3), np.uint8)
    contours, hierarchy = cv.findContours(dil_erode, cv.RETR_CCOMP, cv.CHAIN_APPROX_NONE)

    # look for 2 largest contours and draw them
    max_area = 0
    max_cnt = None
    sec_max_area = 0
    sec_max_cnt = None
    for cnt in contours:
        area = cv.contourArea(cnt)
        cv.drawContours(blank, cnt,-1,(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 1)
        if area > max_area:
            sec_max_area= max_area
            sec_max_cnt = max_cnt
            max_area = area
            max_cnt = cnt
        elif area>sec_max_area:
            sec_max_area= area
            sec_max_cnt = cnt                               
    cv.imshow("Blank with contours", blank)

    # if 2 large contours exist
    if sec_max_area>100:
        ext_bot = tuple(max_cnt[max_cnt[:, :, 1].argmax()][0])
        sec_ext_bot = tuple(sec_max_cnt[sec_max_cnt[:, :, 1].argmax()][0])
        # point = tuple((int((ext_bot[0]+sec_ext_bot[0])/2), int((ext_bot[1]+sec_ext_bot[1])/2)))
        if ext_bot[1]<sec_ext_bot[1]:
            point = ext_bot
        else:
            point = sec_ext_bot
        return point
    return (0,0)