#!/usr/bin/python
# -*- coding:utf-8 -*-

# *************************
# ** Before running this **
# ** code ensure you've  **
# ** turned on SPI on    **
# ** your Raspberry Pi   **
# ** & installed the     **
# ** Waveshare library   **
# *************************

import os, time, sys, random 
from PIL import Image
import ffmpeg
from greg.IT8951.test.integration import *
from working_test_functions import *

def generate_frame(in_filename, out_filename, time, width, height):    
    (
        ffmpeg
        .input(in_filename, ss=time)
        .filter('scale', width, height, force_original_aspect_ratio=1)
        .filter('pad', width, height, -1, -1)
        .output(out_filename, vframes=1)              
        .overwrite_output()
        .run(capture_stdout=True, capture_stderr=True)
    )

from IT8951.display import AutoEPDDisplay

print('Initializing EPD...')

# here, spi_hz controls the rate of data transfer to the device, so a higher
# value means faster display refreshes. the documentation for the IT8951 device
# says the max is 24 MHz (24000000), but my device seems to still work as high as
# 80 MHz (80000000)
display = AutoEPDDisplay(vcom=-1.55, rotate=None, spi_hz=24000000)

print('VCOM set to', display.epd.get_vcom())

# Ensure this is the correct import for your particular screen 
#from waveshare_epd import epd7in5_V2

# Ensure this is the correct path to your video folder 
viddir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Videos/')

# Ensure this is the correct driver for your particular screen 
#epd = epd7in5_V2.EPD()

# Initialise and clear the screen 
#epd.init()
print_system_info(display)
clear_display(display)
#epd.Clear()    

while 1: 

    # Pick a random .mp4 video in your video directory 
    currentVideo = ""
    while not (currentVideo.endswith('.mp4')):
        videoCount = len(os.listdir(viddir))
        randomVideo = random.randint(0,videoCount-1)
        currentVideo = os.listdir(viddir)[randomVideo]
    inputVid = viddir + currentVideo
    print(inputVid)
    # Ensure this matches your particular screen 
    width = 1872
    height = 1404 
    
    # Check how many frames are in the movie 
    frameCount = int(ffmpeg.probe(inputVid)['streams'][0]['nb_frames'])

    # Pick a random frame 
    frame = random.randint(0,frameCount)

    # Convert that frame to Timecode 
    msTimecode = "%dms"%(frame*41.666666)
    
    # Use ffmpeg to extract a frame from the movie, crop it, letterbox it and save it as grab.jpg 
    generate_frame(inputVid, 'grab.jpg', msTimecode, width, height)
    
    # Open grab.jpg in PIL  
    pil_im = Image.open("grab.jpg")
    
    # Dither the image into a 1 bit bitmap (Just zeros and ones)
    pil_im = pil_im.convert(mode='1',dither=Image.FLOYDSTEINBERG)

    # display the image 
    epd.display(epd.getbuffer(pil_im))
    print('Diplaying frame %d of %s' %(frame,currentVideo))
    
    # Wait for 10 seconds 
    time.sleep(10)
    
# NB We should run sleep() while the display is resting more often, but there's a bug in the driver that's slightly fiddly to fix. Instead of just sleeping, it completely shuts down SPI communication 
epd.sleep()
epd7in5.epdconfig.module_exit()
exit()
