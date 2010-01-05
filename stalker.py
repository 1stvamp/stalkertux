#!/usr/bin/python
import sys
import psyco
import opencv
import face
import getopt
from opencv import highgui
from tuxisalive.api.sh import *
from tuxisalive.api import SPV_VERYSLOW, SPV_SLOW, SPV_NORMAL, SPV_FAST, SPV_VERYFAST

psyco.full()

def move_tux_right(amount):
    # This probably won't be the right amount of turns, so will need some
    # tweaking
    duration = 0.1 * amount
    # Moving right we need to move slightly faster because the actuator is slower
    tux.spinning.rightOnDuring(duration, SPV_SLOW)
    print amount


def move_tux_left(amount):
    # This probably won't be the right amount of turns, so will need some
    # tweaking
    duration = 0.1 * amount
    tux.spinning.leftOnDuring(duration, SPV_VERYSLOW)
    print amount

def main(argv):
    # Division of the screen to count as "walking" motion to trigger tux
    motion_block = 640 / 10
    # Frames per second
    fps = 10
    tux_pos = 0
    tux_pos_min = -5
    tux_pos_max = 5

    try:
        opts, args = getopt.getopt(argv, "mb:fps", ["motionblock=", "framerate=",])
    except getopt.GetoptError:
            sys.exit(2)

    for opt, arg in opts:
            if opt in ("-mb", "--motionblock"):
                    motion_block = arg
            if opt in ("-fps", "--framerate"):
                fps = arg

    camera = highgui.cvCreateCameraCapture(0)

    while True:
        highgui.cvNamedWindow('Camera', 1)
        im = highgui.cvQueryFrame(camera)
        if im is None:
            break
        # mirror
        opencv.cv.cvFlip(im, None, 1)

        positions = face.detect(im, 'haarcascade_data/haarcascade_profileface.xml')

        # display webcam image
        highgui.cvShowImage('Camera', im)

        if positions:
            pos = tux_pos_min + int(positions[0][0] / motion_block)
            if tux_pos > pos:
                move_tux_right(pos)
            elif tux_pos < pos:
                move_tux_left(pos)
            tux_pos = pos

        if highgui.cvWaitKey(fps) >= 0:
            highgui.cvDestroyWindow('Camera')
            sys.exit(0)

if __name__ == "__main__":
    main(sys.argv[1:])
