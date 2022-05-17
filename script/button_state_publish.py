#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pigpio
import rospy
from std_msgs.msg import Bool

from simple_push_button.srv import Buttonblink

from time import sleep

PIN_SWITCH_SIGNAL = 23 # 16pin
PIN_SWITCH_LED = 25    # 22pin

rospy.init_node('push_buttun',anonymous=True)

publisher = rospy.Publisher("buttun_pushed", Bool, queue_size=5)

pi = pigpio.pi()

switch_pin = PIN_SWITCH_SIGNAL
led_pin = PIN_SWITCH_LED 

pi.write(PIN_SWITCH_LED,pigpio.LOW)

def cb_button_released(gpio, level, tick):
    publisher.publish(False)
    pi.write(PIN_SWITCH_LED,pigpio.LOW)
    rospy.loginfo("released")

def cb_button_pushed( gpio, level, tick):
    publisher.publish(True)
    pi.write(PIN_SWITCH_LED,pigpio.HIGH)
    rospy.loginfo("pushed")

def cb_button_led_blink(req):
    pi.write(PIN_SWITCH_LED,pigpio.HIGH)
    sleep(0.3)
    pi.write(PIN_SWITCH_LED,pigpio.LOW)
    sleep(0.3)
    pi.write(PIN_SWITCH_LED,pigpio.HIGH)
    sleep(0.3)
    pi.write(PIN_SWITCH_LED,pigpio.LOW)

    return True

rospy.Service('buttun_led_blink', Buttonblink, cb_button_led_blink)


if __name__ == '__main__':

    pi.set_mode( switch_pin, pigpio.INPUT) 
    pi.set_pull_up_down( switch_pin, pigpio.PUD_UP )

    pi.set_mode( led_pin, pigpio.OUTPUT)

    pi.callback( switch_pin, pigpio.RISING_EDGE, cb_button_released)
    pi.callback( switch_pin, pigpio.FALLING_EDGE, cb_button_pushed)

    rate = rospy.Rate(50)


    try:
        while not rospy.is_shutdown():
            #for now 
            rate.sleep()

        pi.write(PIN_SWITCH_LED,pigpio.LOW)
    except KeyboardInterrupt:
        pi.write(PIN_SWITCH_LED,pigpio.LOW)
        pass
    finally:
        pi.write(PIN_SWITCH_LED,pigpio.LOW)
        pass


