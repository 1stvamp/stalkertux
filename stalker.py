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
    if amount > 0:
        duration = 0.1 * amount
        # Moving right we need to move slightly faster because the actuator is slower
        tux.spinning.rightOnDuring(duration, SPV_VERYSLOW)
        print "right, amount: %d, duration: %f" % (amount, duration)


def move_tux_left(amount):
    if amount > 0:
        duration = 0.08 * amount
        tux.spinning.leftOnDuring(duration, SPV_VERYSLOW)
        print "left, amount: %d, duration: %f" % (amount, duration)

def main(argv):
    # Frames per second
    fps = 20
    tux_pos = 5
    tux_pos_min = 0.0
    tux_pos_max = 9.0

    try:
        opts, args = getopt.getopt(argv, "fps", ["framerate=",])
    except getopt.GetoptError:
            sys.exit(2)

    for opt, arg in opts:
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

#        positions = face.detect(im, 'haarcascade_data/haarcascade_profileface.xml')
        positions = face.detect(im, 'haarcascade_data/haarcascade_frontalface_alt2.xml')
#        if not positions:
#            positions = face.detect(im, 'haarcascade_data/haarcascade_frontalface_alt2.xml')

        # display webcam image
        highgui.cvShowImage('Camera', im)

        # Division of the screen to count as "walking" motion to trigger tux
        image_size = opencv.cvGetSize(im)
        motion_block = image_size.width / 9

        if positions:
            mp = None
            for position in positions:
                if not mp or mp['width'] > position['width']:
                    mp = position
            pos = (mp['x'] + (mp['width'] / 2)) / motion_block
            print "tux pos: %f" % tux_pos
            print "pos: %f" % pos

            if pos != tux_pos:
                if tux_pos > pos:
                    move_tux_right(tux_pos - pos)
                elif tux_pos < pos:
                    move_tux_left(pos - tux_pos)
                tux_pos = pos

        if highgui.cvWaitKey(fps) >= 0:
            highgui.cvDestroyWindow('Camera')
            sys.exit(0)

if __name__ == "__main__":
    main(sys.argv[1:])
