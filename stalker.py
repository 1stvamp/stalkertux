import Image, pygame, sys, psyco, opencv, face
from pygame.locals import *
from opencv import highgui
from tuxisalive.api.sh import *

# Resolution of the screen (and camera, but can be seperated), needs to be 4/3 (I think)
size = 640,480
# Division of the screen to count as "walking" motion to trigger tux
motion_block = size[0] / 10
# Frames per second
fps = 10

psyco.full()


def move_tux_right(amount):
    # This probably won't be the right amount of turns, so will need some
    # tweaking
    tux.spinning.rightOn(1.0)
    print amount


def move_tux_left(amount):
    # This probably won't be the right amount of turns, so will need some
    # tweaking
    tux.spinning.leftOn(1.0)
    print amount

camera = highgui.cvCreateCameraCapture(0)

last_x = None

while True:
    highgui.cvNamedWindow('Camera', 1)
    im = highgui.cvQueryFrame(camera)
    if im is None:
        break
    # mirror
    opencv.cv.cvFlip(im, None, 1)

    faces = face.detect(im, 'haarcascade_profileface.xml')

    # display webcam image
    highgui.cvShowImage('Camera', im)


    if last_x is not None:
        test_x = px - last_x
        if test_x < 0:
            if test_x <= (MOTION_BLOCK * -1):
                move_tux_left(int(test_x / MOTION_BLOCK) * -1)
        elif test_x > 0:
            if test_x >= MOTION_BLOCK:
                move_tux_right(int(test_x / MOTION_BLOCK))
    last_x = None

    if highgui.cvWaitKey(fps) >= 0:
        break;
highgui.cvDestroyWindow('Camera')
