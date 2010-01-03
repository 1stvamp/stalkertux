import Image, motion, pygame, sys, psyco, opencv
from pygame.locals import *
from opencv import highgui
from tuxisalive.api.sh import *

# Color threshold for motion detection, the higher the more strict (avg. 50 is ok)
COLOR_THRESHOLD = 20
# Resolution of the screen (and camera, but can be seperated), needs to be 4/3 (I think)
SIZE = 640,480
# Compressed size, needs to be 4/3 (widescreen hack?)
CSIZE = 160,120
# Division of the screen to count as "walking" motion to trigger tux
MOTION_BLOCK = SIZE[0] / 10
# Frames per second
FPS = 10.0

psyco.full()
pygame.init()
# Ratio of compression
ratio = SIZE[0] / CSIZE[0]

# Empty images for comparison
cci = Image.new("RGB", CSIZE, (255,255,255))
ni = Image.new("RGB", SIZE, (255,255,255))
oci = cci


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
def get_image():
    im = highgui.cvQueryFrame(camera)
    # Add the line below if you need it (Ubuntu 8.04+)
    #im = opencv.cvGetMat(im)
    # Convert Ipl image to PIL image
    return opencv.adaptors.Ipl2PIL(im)

last_x = None
pygame.init()
window = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Stalker Tux")
screen = pygame.display.get_surface()

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT or \
            (event.type == pygame.KEYDOWN
             and event.key == pygame.K_ESCAPE):

            sys.exit(0)

    im = get_image()
    pg_img = pygame.image.frombuffer(im.tostring(), im.size, im.mode)
    screen.blit(pg_img, (0,0))

    # Make the current compressed image the old one
    oci = cci
    # Compress the new image and make it the current one
    cci = im.resize(CSIZE, Image.BILINEAR)

    # Compare the images and get the array of pixels with difference
    motionArray = motion.getMotionArray(oci, cci, COLOR_THRESHOLD)
    if len(motionArray) < 1:
        continue
    # Calculate the avarage point
    motionPoint = motion.getMotionPoint(motionArray)
    if motionPoint[0] > 0 and motionPoint[1] > 0:
        # Multiply by compression ratio to get the position
        px = motionPoint[0] * ratio
        # Of the coordinate on the uncompressed image
        py = motionPoint[1] * ratio
        wp = (px,py)

    if last_x is not None:
        test_x = px - last_x
        if test_x < 0:
            if test_x <= (MOTION_BLOCK * -1):
                move_tux_left(int(test_x / MOTION_BLOCK) * -1)
        elif test_x > 0:
            if test_x >= MOTION_BLOCK:
                move_tux_right(int(test_x / MOTION_BLOCK))
    last_x = px

    # Draw everything
    pygame.draw.lines(screen, (0,255,0), 0, [[0,0], wp,])
    pygame.display.flip()
    pygame.time.delay(int(1000 * 1.0 / FPS))
