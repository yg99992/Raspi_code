from gpiozero import *
from time import sleep

gpio_red = 17   # define the gpio number controlling red LED
gpio_gre = 18   # define the gpio number controlling green LED

led_red = LED(gpio_red, active_high=True, initial_value=False)
led_gre = LED(gpio_gre, active_high=True, initial_value=False)

led_red.on()
sleep(0.5)
led_red.off()
sleep(0.5)
led_gre.on()
sleep(0.5)
led_gre.off()
sleep(0.5)

led_red.close()
led_gre.close()

# using gpio function
led_red = DigitalOutputDevice(gpio_red, active_high=True, initial_value=False)
led_gre = DigitalOutputDevice(gpio_gre, active_high=True, initial_value=False)

led_red.on()
sleep(0.5)
led_red.off()
sleep(0.5)
led_gre.on()
sleep(0.5)
led_gre.off()
sleep(0.5)

led_red.close()
led_gre.close()

# using PWM adjust lightness
PWM_led_red = PWMOutputDevice(gpio_red, frequency = 100)
PWM_led_gre = PWMOutputDevice(gpio_gre, frequency = 10)

PWM_led_red.value = 1.0
sleep(1)
PWM_led_red.value = 0.2
sleep(1)
PWM_led_red.off()

PWM_led_gre.value = 1.0
sleep(1)
PWM_led_gre.value = 0.2
sleep(1)
PWM_led_gre.off()


PWM_led_red.frequency = 100
PWM_led_gre.frequency = 100


for i in range(1000):
    PWM_led_red.value = i / 1000
    sleep(0.001)


PWM_led_red.off()
for j in range(5):
    for i in range(1000):
        PWM_led_red.value = i / 1000
        sleep(0.001)

    for i in range(1000):
        PWM_led_red.value = (999-i) / 1000
        sleep(0.001)

for j in range(5):
    for i in range(1000):
        PWM_led_gre.value = i / 1000
        sleep(0.0002)

    for i in range(1000):
        PWM_led_gre.value = (999-i) / 1000
        sleep(0.0002)

led_red.close()
led_gre.close()