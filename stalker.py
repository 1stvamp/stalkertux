import Image, motion, pygame, sys, psyco, opencv
from pygame.locals import *
from opencv import highgui

# Color threshold for motion detection, the higher the more strict (avg. 50 is ok)
COLOR_THRESHOLD = 50
# Resolution of the screen (and camera, but can be seperated), needs to be 4/3 (I think)
SIZE = 640,480
# Compressed size, needs to be 4/3 (widescreen hack?)
CSIZE = 160,120

psyco.full()
pygame.init()
# Ratio of compression
ratio = SIZE[0] / CSIZE[0]

# Empty images for comparison
cci = Image.new("RGB", CSIZE, (255,255,255))
ni = Image.new("RGB", SIZE, (255,255,255))
oci = cci


camera = highgui.cvCreateCameraCapture(0)
def get_image():
    im = highgui.cvQueryFrame(camera)
    # Add the line below if you need it (Ubuntu 8.04+)
    #im = opencv.cvGetMat(im)
    # Convert Ipl image to PIL image
    return opencv.adaptors.Ipl2PIL(im)

fps = 30.0
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

    # Draw everything
    pygame.draw.lines(screen, (0,255,0), 0, [[0,0], wp,])
    pygame.display.flip()
    pygame.time.delay(int(1000 * 1.0 / fps))
