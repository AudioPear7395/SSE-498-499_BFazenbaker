import time, os
# -*- coding:UTF-8 -*-

#--------------Driver Library-----------------#
#directory = /home/benjamin/OLEDscreen/RaspberryPi/python/OLED_Driver
import RPi.GPIO as GPIO
import OLED_Driver as OLED
#--------------Image Library---------------#
from PIL  import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageColor
#-------------Test Display Functions---------------#

def Test_Text(data):
    image = Image.new("RGB", (OLED.SSD1351_WIDTH, OLED.SSD1351_HEIGHT), "BLACK")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('cambriab.ttf',18)

    for txt in enumerate(data):
        draw.text((0, 20*txt[0]), units[txt[0]][0]+txt[1]+units[txt[0]][1], fill = "WHITE", font = font)
    OLED.Display_Image(image)

#Set the filename and open the file
filename = '/home/benjamin/decoderprogram/data.csv'
file = open(filename,'r')

#Find the size of the file and move to the end
st_results = os.stat(filename)
st_size = st_results[6]
file.seek(st_size)

data = []
units = [("TVOC: ","ppb"),("CO2: ","ppm"),("O2: ","%"),("Rad: ","Cpm"),("Temp: ","F"),("Parts: "," ")]

OLED.Device_Init()

while 1:
    where = file.tell()
    line = file.readline()
    if not line:
        time.sleep(1)
        file.seek(where)
    else:
       # print(line) 
        text=line
        csvalues=line.split(',')
        if csvalues[9] != "payload":
            data=csvalues[9].split(";")
            strdat=""
            for cha in data:
                strdat+=chr(int(cha))
            #print(strdat)
            data = strdat.split(',')
            print(data)
            Test_Text(data)
            #OLED.Delay(1000)
