import RPi.GPIO as gpio
from port import Port
from i2c import I2C
import time

class Raspberry:
    def __init__(self):
        """
        """
        # RELAY
        self.CON_PIN1_2 = 4
        self.CON_PIN3_4 = 17
        self.CON_PIN5_6 = 27
        self.CON_PIN7_8 = 22
        self.CON_PIN9_10 = 10
        self.CON_PIN11_12 = 9
        self.CON_PIN13_14 = 11
        self.CON_PIN15_16 = 5
        self.CON_PIN17_18 = 6
        self.CON_PIN19_20 = 13

        # LED
        self.GREEN_LED = 19
        self.STATUS_GREEN_LED = 0
        self.STATUS_RED_LED = 0

        # BUTTON
        self.START_BUTTON = 26

        # OPTO
        self.OPTO1 = 16
        self.OPTO2 = 12
        self.OPTO3 = 7
        self.OPTO4 = 8
        self.OPTOAUX = 20
        self.MOVE_IN = 21

        # ST-Link
        self.TCK = 25
        self.TMS = 24
        self.NRST = 23

        # Serial
        self.Port = Port()
        self.Port.open()

        # I2C
        self.I2C_ADC = I2C(0x36)
        self.I2C_PINS = I2C(0x20)

        self.I2C_PINS_Mascara = 0x00
        self.RED_LED = 0x01
        self.BTN1 = 0x02
        self.BTN2 = 0x04
        self.BTN3 = 0x08
        self.BTN4 = 0x10
        self.BTN5 = 0x20
        self.BTN6 = 0x40
        self.BTN7 = 0x80

        self.Status_OPTO = False
        self.Status_RELE = False
        self.Status_REGULADOR = False
        self.Status_ENERGIA = False
        self.Status_PRESSAO = False
        self.Status_XBEE = False
        self.Status_BTN = False

        self.PWM = None

    def config_pins(self):

        gpio.setmode(gpio.BCM)

        # Relay
        gpio.setup(self.CON_PIN1_2, gpio.IN, pull_up_down=gpio.PUD_DOWN)
        gpio.setup(self.CON_PIN3_4, gpio.IN, pull_up_down=gpio.PUD_DOWN)
        gpio.setup(self.CON_PIN5_6, gpio.IN, pull_up_down=gpio.PUD_DOWN)
        gpio.setup(self.CON_PIN7_8, gpio.IN, pull_up_down=gpio.PUD_DOWN)
        gpio.setup(self.CON_PIN9_10, gpio.IN, pull_up_down=gpio.PUD_DOWN)
        gpio.setup(self.CON_PIN11_12, gpio.IN, pull_up_down=gpio.PUD_DOWN)
        gpio.setup(self.CON_PIN13_14, gpio.IN, pull_up_down=gpio.PUD_DOWN)
        gpio.setup(self.CON_PIN15_16, gpio.IN, pull_up_down=gpio.PUD_DOWN)
        gpio.setup(self.CON_PIN17_18, gpio.IN, pull_up_down=gpio.PUD_DOWN)
        gpio.setup(self.CON_PIN19_20, gpio.IN, pull_up_down=gpio.PUD_DOWN)

        # LED
        gpio.setup(self.GREEN_LED, gpio.OUT)

        # BUTTON
        # gpio.add_event_detect(self.START_BUTTON, gpio.FALLING, callback=BUTTON_callback, bouncetime=300)
        gpio.setup(self.START_BUTTON, gpio.IN, pull_up_down=gpio.PUD_UP)

        # OPTO
        gpio.setup(self.OPTO1, gpio.OUT)
        gpio.setup(self.OPTO2, gpio.OUT)
        gpio.setup(self.OPTO3, gpio.OUT)
        gpio.setup(self.OPTO4, gpio.OUT)
        gpio.setup(self.OPTOAUX, gpio.OUT)
        gpio.setup(self.MOVE_IN, gpio.OUT)

        # PWM
        gpio.setup(18, gpio.OUT)
        self.PWM = gpio.PWM(18, 2343)
        self.PWM.start(50)
        print("PWM Ligado")
        time.sleep(20)

    def set_pin_HIGH(self, pin):
        gpio.output(pin, gpio.HIGH)

    def set_pin_LOW(self, pin):
        gpio.output(pin, gpio.LOW)

    def read_pin(self, pin):
        if gpio.input(pin) == 1:
            return 1
        else:
            return 0

    def write_I2C_PIN(self, pin, High_Low):
        if High_Low == 1:
            self.I2C_PINS_Mascara = self.I2C_PINS_Mascara | pin
            self.I2C_PINS.write(0x40, self.I2C_PINS_Mascara)
        else:
            self.I2C_PINS_Mascara = self.I2C_PINS_Mascara & (~pin)
            self.I2C_PINS.write(0x40, self.I2C_PINS_Mascara)



    def clean_pins(self):
        gpio.cleanup()
