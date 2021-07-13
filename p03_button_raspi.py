from gpiozero import *
from time import sleep
from time import time

# Set GPIO19 as button input, Low voltage is active state
pin_key = Button(19, pull_up=None, active_state=False)

# Set GPIO20 as touch key input, High voltage is active state
pin_tou = Button(20, pull_up=None, active_state=True)

led_red = LED(17)  # Set GPIO17 as red LED
led_gre = LED(18)  # Set GPIO18 as green LED

key_pressed = 0
tou_pressed = 0


def key_poll_test():
    print('Polling Mode !')
    while True:
        if pin_key.is_pressed is True:  # KEY is pressed
            led_red.on()
            sleep(0.1)
            led_red.off()
            sleep(0.1)

        if pin_tou.is_pressed is True:  # TOUCH switch is pressed
            led_gre.on()
            sleep(0.1)
            led_gre.off()
            sleep(0.1)

        if pin_key.is_pressed & pin_tou.is_pressed:
            print('Polling test end !!!')
            return True

# def fun_end():
#    # detect if both KEY and TOUCH are pressed at the same time
#    if pin_key.is_pressed & pin_tou.is_pressed:
#        if time_buf == 0:
#            time_buf = time()
#        # if both bottons are held more than 3 Second, this function will end
#        elif time() > time_buf + 3:
#            time_buf = 0
#            return True
#    else:
#        time_buf = 0


def key_pressed_led():  # interrupt function when press KEY
    print('Key is pressed')
    led_red.on()
    sleep(0.1)
    led_red.off()

def tou_pressed_led():  # interrupt function when press TOUCH switch
    print('Touch switch is pressed')
    led_gre.on()
    sleep(0.1)
    led_gre.off()

def key_intr_test():
    print('Interrupt Mode !')

    # register interrupt function for KEY pressing
    # pin_key.when_pressed  = key_pressed_intr
    pin_key.when_pressed = key_pressed_led
    # register interrupt function for TOUCH switch pressing
    pin_tou.when_pressed = tou_pressed_led

    while True:  # poll status of two buttons
        sleep(0.1)
        if pin_key.is_pressed & pin_tou.is_pressed:
            led_gre.blink(n=1)  # green LED blink once to show hold test end
            print('Interrupt test end !!!')
            pin_key.when_pressed = None  # Remove interrupt function
            pin_tou.when_pressed = None  # Remove interrupt function
            return True


def key_hold_led():
    print('KEY is held')
    for i in range(3):
        sleep(0.1)
        led_red.on()
        sleep(0.1)
        led_red.off()

def key_hold_test():
    print('Hold test!!!')
    # register interrupt function for KEY holding
    pin_key.when_held = key_hold_led
    pin_key.hold_time = 1   # set hold seconds

    time_buf = 0
    while True:
        sleep(0.1)
        if pin_key.is_pressed & pin_tou.is_pressed:
            if time_buf == 0:
                time_buf = time()
            # if two bottons are held more than 1 Second, this function will end
            elif time() > time_buf + 2:
                time_buf = 0
                led_gre.blink(n=1)  # green LED blink once to show hold test end
                print('Hold test end !!!')
                pin_key.when_held = None
                pin_key.hold_repeat = False
                return True
        else:
            time_buf = 0

def key_double_click_test():
    print('Double click test!!!')
    time_buf = 0
    press_cnt = 0
    release_flag = 0
    led_red.blink()  # red LED blink
    while True:
        if pin_key.is_pressed:
            sleep(0.1)
            if release_flag == 1:
                release_flag = 0
                time_buf = time()
                press_cnt = press_cnt + 1
                if press_cnt == 2:  # double click
                    led_gre.blink(n=1)  # green LED blink once to show hold test end
                    print('Detected double click KEY!!!')
                if press_cnt == 3:  # Triple click to end this program
                    led_red.off()
                    print('Double-click test end!!!')
                    return True
        else:
            sleep(0.1)
            release_flag = 1
            if (time_buf != 0) & (time() > time_buf + 0.5):
                press_cnt = 0
                time_buf = 0


if __name__ == '__main__':  # These program only executed in this manuscript
    while True:
        print('Please input mode:')
        in_data = input()  # input data from keyboard
        if in_data == 'P':  # when 'P' is inputted
            key_poll_test()
        elif in_data == 'I':
            key_intr_test()
        elif in_data == 'H':
            key_hold_test()
#        elif in_data == 'D':
#            key_double_click_test()
        elif in_data == 'exit':
            break