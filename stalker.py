import sys
import psyco
import opencv
import face
import getopt
from opencv import highgui
from tuxisalive.api.sh import *
from tuxisalive.api import SPV_VERYSLOW, SPV_SLOW, SPV_NORMAL, SPV_FAST, SPV_VERYFAST

# Division of the screen to count as "walking" motion to trigger tux
motion_block = 640 / 10
# Frames per second
fps = 10
last_x = None

psyco.full()

def move_tux_right(amount):
    # This probably won't be the right amount of turns, so will need some
    # tweaking
    duration = 0.2 * amount
    tux.spinning.rightOnDuringAsync(duration, SPV_FAST)
    print amount


def move_tux_left(amount):
    # This probably won't be the right amount of turns, so will need some
    # tweaking
    duration = 0.2 * amount
    tux.spinning.leftOnDuringAsync(duration, SPV_FAST)
    print amount

def main():
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
            highgui.cvDestroyWindow('Camera')
            sys.exit(0)

if __name__ == "__main__":
    main()
