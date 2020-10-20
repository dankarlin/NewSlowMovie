
from time import sleep
import argparse
import os
from working_test_functions import *

def parse_args():
    p = argparse.ArgumentParser(description='Test EPD functionality')
    p.add_argument( '-f', '--file', default='/home/pi/Images/sleeping_penguin.png', 
                  help='file to display')
    p.add_argument('-r', '--rotate', default=None, choices=['CW', 'CCW', 'flip'],
                   help='run the tests with the display rotated by the specified value')

    return p.parse_args()

def main():

    args = parse_args()
    if os.path.exists(args.file):
           print("File exists")
           file_path = args.file
    else:
           print("Reverting to default image")
           file_path = '/home/pi/Images/sleeping_penguin.png'

    from IT8951.display import AutoEPDDisplay

    print('Initializing EPD...')

    # here, spi_hz controls the rate of data transfer to the device, so a higher
    # value means faster display refreshes. the documentation for the IT8951 device
    # says the max is 24 MHz (24000000), but my device seems to still work as high as
    # 80 MHz (80000000)
    display = AutoEPDDisplay(vcom=-1.55, rotate=None, spi_hz=24000000)

    print('VCOM set to', display.epd.get_vcom())

    display_image_8bpp(display, file_path)

    print('Done!')

if __name__ == '__main__':
    main()
