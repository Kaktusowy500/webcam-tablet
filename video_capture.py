import cv2 as cv
import numpy as np

def empty():
    pass

capture = cv.VideoCapture(0)

capture.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
capture.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

cv.namedWindow('TrackBars')
cv.resizeWindow('TrackBars', 640, 240)
cv.createTrackbar('Hue Min', 'TrackBars', 0, 179, empty)
cv.createTrackbar('Hue Max', 'TrackBars', 179, 179, empty)
cv.createTrackbar('Sat Min', 'TrackBars', 0, 255, empty)
cv.createTrackbar('Sat Max', 'TrackBars', 255, 255, empty)
cv.createTrackbar('Val Min', 'TrackBars', 0, 255, empty)
cv.createTrackbar('Val Max', 'TrackBars', 255, 255, empty)

while True:
    isTrue, img = capture.read()
    imgHSV = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    #changing params by trackballs, name of track and window must be the same
    h_min= cv.getTrackbarPos('Hue Min', 'TrackBars')
    h_max= cv.getTrackbarPos('Hue Max', 'TrackBars')
    s_min= cv.getTrackbarPos('Sat Min', 'TrackBars')
    s_max= cv.getTrackbarPos('Sat Max', 'TrackBars')
    v_min= cv.getTrackbarPos('Val Min', 'TrackBars')
    v_max= cv.getTrackbarPos('Val Max', 'TrackBars')
    #print(h_min, h_max, s_min, s_max, v_min, v_max)
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])

    #mask with limits
    mask = cv.inRange(imgHSV, lower, upper)
    #result on original
    imgRes = cv.bitwise_and(img, img, mask =mask)
    cv.imshow('Org', img)
    cv.imshow('HSV', imgHSV)
    cv.imshow('Mask', mask)
    cv.imshow('Result', imgRes)
    print(img.shape)
    pts1 = np.float32([[115,190],[520,188],[23, 239], [630,235]])

    #params for new cropped part
    width, height = 250, 200
    #new points
    pts2 = np.float32([[0,0], [width, 0], [0, height], [width, height]])
    #matrix for transform
    matrix = cv.getPerspectiveTransform(pts1, pts2)
    img_out = cv.warpPerspective(img, matrix, (width, height))

    cv.imshow('Output', img_out)#Title, img

    # gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # faces = face_cascade.detectMultiScale(gray,1.1, 4)
    # img_face = img.copy()
    # for(x,y,w,h) in faces:
    #     cv.rectangle(img_face, (x,y), (x+w, y+h), (255, 0, 0), 2)

    # cv.imshow('Face Result', img_face)
    if cv.waitKey(20) & 0xFF ==ord('d'): # if d is pressed
        break
capture.release()
cv.destroyAllWindows()