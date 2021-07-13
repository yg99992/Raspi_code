from lcd1602 import *
from gpiozero import *
from time import sleep
from time import time
import threading

global pin_key
global lcd
pin_key = Button(19)
lcd = lcd1602(1)


def key_lcd():
    while True:
        sleep(0.01)
        if pin_key.is_pressed:
            while lcd.BUSY:
                sleep(0.001)
            lcd.show_string(1,0,'Key is Pressed!')
        else:
            while lcd.BUSY:
                sleep(0.001)
            lcd.show_string(1,0,'Key is Released!')

def lcd_move():
    global led_move
    string = 'University of Macau. '
    #for lcd_x in range(16):
    #    while lcd.BUSY:
    #        sleep(0.001)
    #    lcd.show_string(0, 15-lcd_x, string)
    #    sleep(0.4)

    inx = 0
    str_len = len(string)
    while True:
        for inx in range(str_len):
            if led_move_inverse:
                ptr = (str_len-inx) % str_len # first display position
            else:
                ptr = inx # first display position
            str_show = string[ptr:] + string[:ptr]

            while lcd.BUSY | (led_move != True):
                sleep(0.001)
            lcd.show_string(0, 0, str_show)
            sleep(0.4)

led_move_inverse = True   # determine if inverse movement
global led_move   # move or stop
led_move = True   # default is move
def led_move_control():
    global led_move
    pressed = 0
    while True:
        sleep(0.01)
        if pin_key.is_pressed:
            if pressed == 0:  # first enter into this case
                pressed = 1
                led_move = bool(1-led_move)  # negate led_move
        else:
            pressed = 0


#Muti-threads
threads=[]
t1 = threading.Thread(target=key_lcd)
threads.append(t1)

t2 = threading.Thread(target=lcd_move)
threads.append(t2)

t3 = threading.Thread(target=led_move_control)
threads.append(t3)

#lcd_move()
for t in threads:
    t.setDaemon(True)
    t.start()
t.join()