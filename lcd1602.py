#!/usr/bin/python
#coding=utf-8

import smbus
import time

class lcd1602:
    def __init__(self, i2c_dev = 1, addr = 0x27):
        # Define some device parameters
        self.I2C_ADDR  = addr # I2C device address
        self.LCD_WIDTH = 16   # Maximum characters per line
        self.LCD_HIGH  = 2

        # Define some device constants
        self.LCD_CHR = 1 # Mode - Sending data
        self.LCD_CMD = 0 # Mode - Sending command

        self.LCD_BACKLIGHT  = 0x08  # On
        self.ENABLE = 0b00000100 # Enable bit

        # Timing constants
        self.PULSE = 0.0005
        self.DELAY = 0.0005

        # Command
        self.CLEAR = 0x01  # screen clear
        self.BUSY = False

        #Open I2C interface
        self.BUS = smbus.SMBus(i2c_dev) # Rev 2 Pi uses 1

        # Initialise display
        self.lcd_byte(0x33,self.LCD_CMD) # 110011 Initialise
        self.lcd_byte(0x32,self.LCD_CMD) # 110010 Initialise
        self.lcd_byte(0x06,self.LCD_CMD) # 000110 Cursor move direction
        self.lcd_byte(0x0C,self.LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
        self.lcd_byte(0x28,self.LCD_CMD) # 101000 (0x28) Data length, number of lines, font size
        self.lcd_byte(self.CLEAR,self.LCD_CMD) # 000001 Clear display
        time.sleep(self.DELAY)

    def lcd_byte(self, bits, mode):
        # bits = the data
        # mode = 1 for data
        #        0 for command

        bits_high = (bits & 0xF0)      | self.LCD_BACKLIGHT | mode
        bits_low  = ((bits<<4) & 0xF0) | self.LCD_BACKLIGHT | mode


        # High bits
        self.BUS.write_byte(self.I2C_ADDR, bits_high)
        self.lcd_toggle_enable(bits_high)

        # Low bits
        self.BUS.write_byte(self.I2C_ADDR, bits_low)
        self.lcd_toggle_enable(bits_low)

    def lcd_toggle_enable(self, bits):
        # Toggle enable
        time.sleep(self.DELAY)
        self.BUS.write_byte(self.I2C_ADDR, (bits | self.ENABLE))
        time.sleep(self.PULSE)
        self.BUS.write_byte(self.I2C_ADDR,(bits & ~self.ENABLE))
        time.sleep(self.DELAY)

    def show_string(self, lcd_y=0, lcd_x=0, message=''):
      # Send string to display

        message = message.ljust(self.LCD_WIDTH," ")
        if lcd_x < 0:
            lcd_x = 0
        if lcd_x >= self.LCD_WIDTH:
            lcd_x = self.LCD_WIDTH - 1

        if lcd_y <0:
            lcd_y = 0
        if lcd_y >= self.LCD_HIGH:
            lcd_y = self.LCD_HIGH - 1


        lcd_addr = 0x80 + 0x40 * lcd_y + lcd_x

        self.BUSY = True
        self.lcd_byte(lcd_addr, self.LCD_CMD)

        for i in range(len(message)):
            self.lcd_byte(ord(message[i]),self.LCD_CHR)
            #time.sleep(0.2)
        self.BUSY = False

    def clear_screen(self):
        self.lcd_byte(self.CLEAR, self.LCD_CMD)
        time.sleep(self.DELAY)

if __name__ == '__main__':

    lcd = lcd1602(1, 0x27)
    lcd.show_string(0, 5, "LCD1602")
    lcd.show_string(1, 3, "Hello World!")