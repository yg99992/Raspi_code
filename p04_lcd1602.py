from lcd1602 import *
from gpiozero import *
from time import sleep
import time
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
    string = 'University of Macau. '

    inx = 0
    str_len = len(string)
    while True:
        for inx in range(str_len):
            while lcd.BUSY:
                sleep(0.001)
            str_show = string[inx:] + string[:inx]
            lcd.show_string(0, 0, str_show)
            sleep(0.4)

if __name__ == '__main__':
    try:
        # test key_lcd()
        # key_lcd()

        # test lcd_move()
        # lcd_move()

        #Muti-threads
        threads=[]
        t1 = threading.Thread(target=key_lcd)
        threads.append(t1)
        t2 = threading.Thread(target=lcd_move)
        threads.append(t2)

        #lcd_move()
        for t in threads:
            #t.setDaemon(True)
            t.start()
        t.join()
    except KeyboardInterrupt:
        lcd.clear_screen()
        lcd.BUS.close() # close i2c
        print('exit')
        pass
