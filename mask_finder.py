import cv2 as cv
import numpy as np

def empty():
    pass

def init_trackbars():
    cv.namedWindow('TrackBars')
    cv.resizeWindow('TrackBars', 640, 240)
    cv.createTrackbar('Hue Min', 'TrackBars', 0, 179, empty)
    cv.createTrackbar('Hue Max', 'TrackBars', 179, 179, empty)
    cv.createTrackbar('Sat Min', 'TrackBars', 0, 255, empty)
    cv.createTrackbar('Sat Max', 'TrackBars', 255, 255, empty)
    cv.createTrackbar('Val Min', 'TrackBars', 0, 255, empty)
    cv.createTrackbar('Val Max', 'TrackBars', 255, 255, empty)

def get_mask_limits():
    # changing params by trackballs, name of track and window must be the same
    h_min = cv.getTrackbarPos('Hue Min', 'TrackBars')
    h_max = cv.getTrackbarPos('Hue Max', 'TrackBars')
    s_min = cv.getTrackbarPos('Sat Min', 'TrackBars')
    s_max = cv.getTrackbarPos('Sat Max', 'TrackBars')
    v_min = cv.getTrackbarPos('Val Min', 'TrackBars')
    v_max = cv.getTrackbarPos('Val Max', 'TrackBars')
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])

    return lower, upper