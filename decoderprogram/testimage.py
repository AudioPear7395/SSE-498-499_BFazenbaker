# -*- coding:UTF-8 -*-

#--------------Driver Library-----------------#
import RPi.GPIO as GPIO
import OLED_Driver as OLED
#--------------Image Library---------------#
from PIL  import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageColor
#-------------Test Display Functions---------------#

def Test_Text():
    image = Image.new("RGB", (OLED.SSD1351_WIDTH, OLED.SSD1351_HEIGHT), "BLACK")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('cambriab.ttf',24)

    Ben_text = 'Benjamin'
    draw.text((0, 12), Ben_text, fill = "PURPLE", font = font)

    OLED.Display_Image(image)


def Test_Pattern(x):
    image = Image.new("RGB", (OLED.SSD1351_WIDTH, OLED.SSD1351_HEIGHT), "BLACK")
    draw = ImageDraw.Draw(image)
    
    draw.line([(0,64), (127,64)],   fill = "RED",    width = x)
    
    OLED.Display_Image(image)


def Test_Lines():
    image = Image.new("RGB", (OLED.SSD1351_WIDTH, OLED.SSD1351_HEIGHT), "BLACK")
    draw = ImageDraw.Draw(image)

    for x in range(0, int((OLED.SSD1351_WIDTH-1)/2), 6):
        draw.line([(0, 0), (x, OLED.SSD1351_HEIGHT - 1)], fill = "RED", width = 1)
        draw.line([(0, 0), ((OLED.SSD1351_WIDTH-1) - x, OLED.SSD1351_HEIGHT - 1)], fill = "RED", width = 1)
        draw.line([(0, 0), (OLED.SSD1351_WIDTH - 1, x)], fill = "RED", width = 1)
        draw.line([(0, 0), (OLED.SSD1351_WIDTH - 1, (OLED.SSD1351_HEIGHT-1) - x)], fill = "RED", width = 1)
        OLED.Display_Image(image)
    OLED.Delay(250)
    draw.rectangle([0, 0, OLED.SSD1351_WIDTH - 1, OLED.SSD1351_HEIGHT - 1], fill = "BLACK", outline = "BLACK")

    for x in range(0, int((OLED.SSD1351_WIDTH-1)/2), 6):
        draw.line([(OLED.SSD1351_WIDTH - 1, 0), (x, OLED.SSD1351_HEIGHT - 1)], fill = "YELLOW", width = 1)
        draw.line([(OLED.SSD1351_WIDTH - 1, 0), (x + int((OLED.SSD1351_WIDTH-1)/2), OLED.SSD1351_HEIGHT - 1)], fill = "YELLOW", width = 1)
        draw.line([(OLED.SSD1351_WIDTH - 1, 0), (0, x)], fill = "YELLOW", width = 1)
        draw.line([(OLED.SSD1351_WIDTH - 1, 0), (0, x + int((OLED.SSD1351_HEIGHT-1)/2))], fill = "YELLOW", width = 1)
        OLED.Display_Image(image)
    OLED.Delay(250)
    draw.rectangle([0, 0, OLED.SSD1351_WIDTH - 1, OLED.SSD1351_HEIGHT - 1], fill = "BLACK", outline = "BLACK")

    for x in range(0, int((OLED.SSD1351_WIDTH-1)/2), 6):
        draw.line([(0, OLED.SSD1351_HEIGHT - 1), (x, 0)], fill = "BLUE", width = 1)
        draw.line([(0, OLED.SSD1351_HEIGHT - 1), (x + int((OLED.SSD1351_WIDTH-1)/2), 0)], fill = "BLUE", width = 1)
        draw.line([(0, OLED.SSD1351_HEIGHT - 1), (OLED.SSD1351_WIDTH - 1, x)], fill = "BLUE", width = 1)
        draw.line([(0, OLED.SSD1351_HEIGHT - 1), (OLED.SSD1351_WIDTH - 1, x + (OLED.SSD1351_HEIGHT-1)/2)], fill = "BLUE", width = 1)
        OLED.Display_Image(image)
    draw.rectangle([0, 0, OLED.SSD1351_WIDTH - 1, OLED.SSD1351_HEIGHT - 1], fill = "BLACK", outline = "BLACK")
    OLED.Delay(250)
    
    for x in range(0, int((OLED.SSD1351_WIDTH-1)/2), 6):
        draw.line([(OLED.SSD1351_WIDTH - 1, OLED.SSD1351_HEIGHT - 1), (x, 0)], fill = "GREEN", width = 1)
        draw.line([(OLED.SSD1351_WIDTH - 1, OLED.SSD1351_HEIGHT - 1), (x + int((OLED.SSD1351_WIDTH-1)/2), 0)], fill = "GREEN", width = 1)
        draw.line([(OLED.SSD1351_WIDTH - 1, OLED.SSD1351_HEIGHT - 1), (0, x)], fill = "GREEN", width = 1)
        draw.line([(OLED.SSD1351_WIDTH - 1, OLED.SSD1351_HEIGHT - 1), (0, x + int((OLED.SSD1351_HEIGHT-1)/2))], fill = "GREEN", width = 1)
        OLED.Display_Image(image)
    draw.rectangle([0, 0, OLED.SSD1351_WIDTH - 1, OLED.SSD1351_HEIGHT - 1], fill = "BLACK")


def Test_HV_Lines():
    image = Image.new("RGB", (OLED.SSD1351_WIDTH, OLED.SSD1351_HEIGHT), "BLACK")
    draw = ImageDraw.Draw(image)
    
    for y in range(0, OLED.SSD1351_HEIGHT - 1, 5):
        draw.line([(0, y), (OLED.SSD1351_WIDTH - 1, y)], fill = "WHITE", width = 1)
    OLED.Display_Image(image)
    OLED.Delay(250)
    for x in range(0, OLED.SSD1351_WIDTH - 1, 5):
        draw.line([(x, 0), (x, OLED.SSD1351_HEIGHT - 1)], fill = "WHITE", width = 1)
    OLED.Display_Image(image)


def Test_Rects():
    image = Image.new("RGB", (OLED.SSD1351_WIDTH, OLED.SSD1351_HEIGHT), "BLACK")
    draw = ImageDraw.Draw(image)
    
    for x in range(0, int((OLED.SSD1351_WIDTH-1)/2), 6):
        draw.rectangle([(x, x), (OLED.SSD1351_WIDTH- 1 - x, OLED.SSD1351_HEIGHT-1 - x)], fill = None, outline = "WHITE")
    OLED.Display_Image(image)


def Test_FillRects(): 
    image = Image.new("RGB", (OLED.SSD1351_WIDTH, OLED.SSD1351_HEIGHT), "BLACK")
    draw = ImageDraw.Draw(image)
    
    for x in range(OLED.SSD1351_HEIGHT-1, int((OLED.SSD1351_HEIGHT-1)/2), -6):
        draw.rectangle([(x, x), ((OLED.SSD1351_WIDTH-1) - x, (OLED.SSD1351_HEIGHT-1) - x)], fill = "BLUE", outline = "BLUE")
        draw.rectangle([(x, x), ((OLED.SSD1351_WIDTH-1) - x, (OLED.SSD1351_HEIGHT-1) - x)], fill = None, outline = "YELLOW")
    OLED.Display_Image(image)


def Test_Circles():
    image = Image.new("RGB", (OLED.SSD1351_WIDTH, OLED.SSD1351_HEIGHT), "BLACK")
    draw = ImageDraw.Draw(image)

    draw.ellipse([(0, 0), (OLED.SSD1351_WIDTH - 1, OLED.SSD1351_HEIGHT - 1)], fill = "BLUE", outline = "BLUE")
    OLED.Display_Image(image)
    OLED.Delay(500)
    for r in range(0, int(OLED.SSD1351_WIDTH/2) + 4, 4):
        draw.ellipse([(r, r), ((OLED.SSD1351_WIDTH-1) - r, (OLED.SSD1351_HEIGHT-1) - r)], fill = None, outline = "YELLOW")
    OLED.Display_Image(image)


def Test_Triangles():
    image = Image.new("RGB", (OLED.SSD1351_WIDTH, OLED.SSD1351_HEIGHT), "BLACK")
    draw = ImageDraw.Draw(image)
    
    for i in range(0, int(OLED.SSD1351_WIDTH/2), 4):
        draw.line([(i, OLED.SSD1351_HEIGHT - 1 - i), (OLED.SSD1351_WIDTH/2, i)], fill = (255 - i*4, i*4, 255 - i*4), width = 1)
        draw.line([(i, OLED.SSD1351_HEIGHT - 1 - i), (OLED.SSD1351_WIDTH - 1 - i, OLED.SSD1351_HEIGHT - 1 - i)], fill = (i*4, i*4 ,255 - i*4), width = 1)
        draw.line([(OLED.SSD1351_WIDTH - 1 - i, OLED.SSD1351_HEIGHT - 1 - i), (OLED.SSD1351_WIDTH/2, i)], fill = (i*4, 255 - i*4, i*4), width = 1)
        OLED.Display_Image(image)


def Display_Picture(File_Name):
    image = Image.open(File_Name)
    OLED.Display_Image(image)

#----------------------MAIN-------------------------#
try:

    def main():
    
        #-------------OLED Init------------#
        OLED.Device_Init()

        #-------------Draw Pictures------------#
        Test_Text()
        OLED.Delay(1000)


    if __name__ == '__main__':
        main()

except:
    print("\r\nEnd")
    OLED.Clear_Screen()
    GPIO.cleanup()


