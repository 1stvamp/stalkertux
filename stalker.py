import Image, ImageDraw, motion, time, pygame, sys, random, psyco
from pygame.locals import *
import opencv
#this is important for capturing/displaying images
from opencv import highgui

COLORTHRESHOLD = 50 #color threshold for motion detection, the higher the more strict (avg. 50 is ok)
SIZE = 640,480 # resolution of the screen (and camera, but can be seperated), needs to be 4/3 (I think)
CSIZE = 160,120 #compressed size, needs to be 4/3 (widescreen hack?)

#init vars
##########
psyco.full() #PSYCO speeds up python
pygame.init() #We need to initialize pygame early on, so that certain stuff works (loading sound..)
ratio = SIZE[0]/CSIZE[0] #ratio of compression

#new empty images, we will be using them in the main loop
#ni = newest image
#nci = newest compressed image
#oci = older compressed image
cci = Image.new("RGB",CSIZE,(255,255,255))
ni = Image.new("RGB",SIZE,(255,255,255))
oci = cci


camera = highgui.cvCreateCameraCapture(0)
def get_image():
    im = highgui.cvQueryFrame(camera)
    # Add the line below if you need it (Ubuntu 8.04+)
    #im = opencv.cvGetMat(im)
    #convert Ipl image to PIL image
    return opencv.adaptors.Ipl2PIL(im)

fps = 30.0
pygame.init()
window = pygame.display.set_mode(SIZE)
pygame.display.set_caption("WebCam Demo")
screen = pygame.display.get_surface()

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT or event.type == KEYDOWN:
            sys.exit(0)
    im = get_image()
    pg_img = pygame.image.frombuffer(im.tostring(), im.size, im.mode)
    screen.blit(pg_img, (0,0))

    #Get the images
    ###############
    #oci and nci are used for motion detection, they don't show up on screen
    #if you want to show something use ni
    oci = cci #make the current compressed image the old one
    ni = im #get new image for compression
    #ni = ni.transpose(Image.FLIP_LEFT_RIGHT) #Flip image for mirror movement, this way topleft == (0,0)
    cci = ni.resize(CSIZE,Image.BILINEAR) #compress the new image and make it the current one

    #Get motion from images
    #######################
    motionArray = motion.getMotionArray(oci,cci,COLORTHRESHOLD) #compare the images and get the array of pixels with difference
    if len(motionArray) < 1:
        continue
    motionPoint = motion.getMotionPoint(motionArray) #calculate the avarage point
    if motionPoint[0] > 0 and motionPoint[1] > 0: #chek X and Y values
        #if a real avarage point of motion has been returned
        wp = motionPoint
        px = wp[0]*ratio #multiply by compression ratio to get the position
        py = wp[1]*ratio #of the coordinate on the uncompressed image
        wp = (px,py)

    #Draw everything
    #################
    pygame.draw.lines(screen, (0,255,0), 0, [[0,0], wp,])
    pygame.display.flip()
    pygame.time.delay(int(1000 * 1.0/fps))


