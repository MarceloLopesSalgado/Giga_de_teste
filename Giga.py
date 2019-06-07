from raspberry import Raspberry
import time
import os
import threading
from Queue import Queue
import signal
import sys
import log, logging

logger = logging.getLogger(__name__)

FILA = Queue(maxsize=0)

RASPBERRY = Raspberry()
RASPBERRY.config_pins()


def signal_handler(sig, frame):
    logger.info('You pressed Ctrl+C!')
    sys.exit(0)


def FILA_thread():
    while True:
        try:
            while not FILA.empty():
                frame = FILA.get()

                if frame[0] == '\x03':
                    if frame[2] is '\x20':
                        RASPBERRY.Status_OPTO = True
                        logger.info("Status OPTO True")
                    else:
                        RASPBERRY.Status_OPTO = False
                        logger.info("Status OPTO False")

                if frame[0] == '\x04':
                    Tensao = frame[2] + frame[3]
                    if (Tensao >= ('\x04' + '\xB0')) and (Tensao <= ('\x05' + '\x78')):
                        RASPBERRY.Status_ENERGIA = True
                        DATA = '\x04' + '\x01' + '\x04' + '\xF6' + '\x01' + '\x00' + '\x00' + '\x00'
                        RASPBERRY.Port.serial.write(DATA)
                        logger.info("Status ENERGIA True")
                    else:
                        RASPBERRY.Status_ENERGIA = False
                        DATA = '\x04' + '\x01' + '\x04' + '\xF6' + '\x00' + '\x00' + '\x00' + '\x00'
                        RASPBERRY.Port.serial.write(DATA)
                        logger.info("Status ENERGIA False")

                if frame[0] == '\x05':
                    if frame[1] == '\x01':
                        RASPBERRY.Status_XBEE = True
                        logger.info("Status XBEE True")
                    else:
                        RASPBERRY.Status_XBEE = False
                        logger.info("Status XBEE False")

                if frame[0] == '\x07':
                    Pressao = frame[2] + frame[3]
                    if (Pressao >= ('\x00' + '\x8C')) and (Pressao <= ('\x00' + '\xA0')):
                        RASPBERRY.Status_PRESSAO = True
                        DATA = '\x07' + '\x01' + '\x00' + '\x96' + '\x01' + '\x00' + '\x00' + '\x00'
                        RASPBERRY.Port.serial.write(DATA)
                        logger.info("Status PRESSAO True")
                    else:
                        RASPBERRY.Status_PRESSAO = False
                        DATA = '\x07' + '\x01' + '\x00' + '\x96' + '\x00' + '\x00' + '\x00' + '\x00'
                        RASPBERRY.Port.serial.write(DATA)
                        logger.info("Status PRESSAO False")

                if frame[0] == '\x08':
                    if frame[1] == '\x01':
                        RASPBERRY.Status_BTN = True
                        logger.info("Status BTN True")
                    else:
                        RASPBERRY.Status_BTN = False
                        logger.info("Status BTN False")
        except KeyboardInterrupt:
            t3.join(1)
            logger.info("Here 3")
            break

def read_thread():
    while True:
        try:
            data = RASPBERRY.Port.serial.read(8)
            if data is not None:
                FILA.put(data)
                logger.info("chegou: " + data)
        except KeyboardInterrupt:
            t1.join(1)
            print("Here 1")
            break


def led_green():
    while True:
        try:
            # GREEN LED
            if RASPBERRY.STATUS_GREEN_LED == 2:
                RASPBERRY.set_pin_HIGH(RASPBERRY.GREEN_LED)
                time.sleep(0.5)
                RASPBERRY.set_pin_LOW(RASPBERRY.GREEN_LED)
                time.sleep(0.5)
            else:
                if RASPBERRY.STATUS_GREEN_LED == 1:
                    RASPBERRY.set_pin_HIGH(RASPBERRY.GREEN_LED)
                    time.sleep(0.5)
                else:
                    RASPBERRY.set_pin_LOW(RASPBERRY.GREEN_LED)
                    time.sleep(0.5)
        except KeyboardInterrupt:
            t4.join(1)
            logger.info("Here 4")
            break


def led_red():
    while True:
        try:
            # RED LED
            if RASPBERRY.STATUS_RED_LED == 2:
                RASPBERRY.write_I2C_PIN(RASPBERRY.RED_LED, 1)
                time.sleep(0.5)
                RASPBERRY.write_I2C_PIN(RASPBERRY.RED_LED, 0)
                time.sleep(0.5)
            else:
                if RASPBERRY.STATUS_RED_LED == 1:
                    RASPBERRY.write_I2C_PIN(RASPBERRY.RED_LED, 1)
                    time.sleep(0.5)
                else:
                    RASPBERRY.write_I2C_PIN(RASPBERRY.RED_LED, 0)
                    time.sleep(0.5)
        except KeyboardInterrupt:
            t5.join(1)
            logger.info("Here 5")
            break



def main_thread():
    while True:
        try:
            if RASPBERRY.read_pin(RASPBERRY.START_BUTTON) == 0:
                # PISCA LEDS
                RASPBERRY.STATUS_GREEN_LED = 2
                RASPBERRY.STATUS_RED_LED = 2

                # grava o firmware
                logger.info("Gravando Firmware")
                time1 = time.time()
                os.system('cd .. && cd bootloader && timeout -s9 30s sudo openocd')
                os.system('sudo kill -9 $(sudo lsof -t -i:6666)')
                time2 = time.time()

                if (time2 - time1) >= 30:
                    logger.info("Erro ao gravar firmware")
                    RASPBERRY.STATUS_GREEN_LED = 0
                    RASPBERRY.STATUS_RED_LED = 1
                else:
                    RASPBERRY.STATUS_GREEN_LED = 1
                    RASPBERRY.STATUS_RED_LED = 2
                    time.sleep(5)
                    # Send Start
                    logger.info("Send START")
                    DATA = '\x01' + '\x01' + '\x00' + '\x00' + '\x00' + '\x00' + '\x00' + '\x00'
                    RASPBERRY.Port.serial.write(DATA)

                    time.sleep(1)

                    # Manda ligar os reles
                    logger.info(" ")
                    logger.info("Manda ligar os reles ")
                    DATA = '\x02' + '\x01' + '\x00' + '\x00' + '\x00' + '\x00' + '\x00' + '\x00'
                    RASPBERRY.Port.serial.write(DATA)

                    time.sleep(4)

                    R1 = RASPBERRY.read_pin(RASPBERRY.CON_PIN1_2)
                    R2 = RASPBERRY.read_pin(RASPBERRY.CON_PIN3_4)
                    R3 = RASPBERRY.read_pin(RASPBERRY.CON_PIN5_6)
                    R4 = RASPBERRY.read_pin(RASPBERRY.CON_PIN7_8)
                    R5 = RASPBERRY.read_pin(RASPBERRY.CON_PIN9_10)
                    R6 = RASPBERRY.read_pin(RASPBERRY.CON_PIN11_12)
                    R7 = RASPBERRY.read_pin(RASPBERRY.CON_PIN13_14)
                    R8 = RASPBERRY.read_pin(RASPBERRY.CON_PIN15_16)
                    R9 = RASPBERRY.read_pin(RASPBERRY.CON_PIN17_18)
                    R10 = RASPBERRY.read_pin(RASPBERRY.CON_PIN19_20)

                    if R1 == 0:
                        logger.info("Rele 1 com erro")
                    if R2 == 0:
                        logger.info("Rele 2 com erro")
                    if R3 == 0:
                        logger.info("Rele 3 com erro")
                    if R4 == 0:
                        logger.info("Rele 4 com erro")
                    if R5 == 0:
                        logger.info("Rele 5 com erro")
                    if R6 == 0:
                        logger.info("Rele 6 com erro")
                    if R7 == 0:
                        logger.info("Rele 7 com erro")
                    if R8 == 0:
                        logger.info("Rele 8 com erro")
                    if R9 == 0:
                        logger.info("Rele 9 com erro")
                    if R10 == 0:
                        logger.info("Rele 10 com erro")

                    if R1 and R2 and R3 and R4 and R5 and R6 and R7 and R8 and R9 and R10:
                        logger.info("Send rele OK")
                        DATA = '\x02' + '\x00' + '\x01' + '\x00' + '\x00' + '\x00' + '\x00' + '\x00'
                        RASPBERRY.Port.serial.write(DATA)
                        RASPBERRY.Status_RELE = True
                    else:
                        print("Send rele NAO OK")
                        DATA = '\x02' + '\x00' + '\x00' + '\x00' + '\x00' + '\x00' + '\x00' + '\x00'
                        RASPBERRY.Port.serial.write(DATA)
                        RASPBERRY.Status_RELE = False

                    # Aciona os optos
                    RASPBERRY.set_pin_LOW(RASPBERRY.OPTO1)
                    RASPBERRY.set_pin_LOW(RASPBERRY.OPTO2)
                    RASPBERRY.set_pin_LOW(RASPBERRY.OPTO3)
                    RASPBERRY.set_pin_LOW(RASPBERRY.OPTO4)
                    RASPBERRY.set_pin_LOW(RASPBERRY.OPTOAUX)
                    RASPBERRY.set_pin_HIGH(RASPBERRY.MOVE_IN)

                    time.sleep(1)

                    # Manda ler os OPTOS
                    logger.info(" ")
                    logger.info("Send LER OPTOS")
                    DATA = '\x03' + '\x01' + '\x00' + '\x00' + '\x00' + '\x00' + '\x00' + '\x00'
                    RASPBERRY.Port.serial.write(DATA)

                    time.sleep(2)

                    # I2C
                    logger.info("acionando BTN")

                    RASPBERRY.write_I2C_PIN(RASPBERRY.BTN1, 1)
                    RASPBERRY.write_I2C_PIN(RASPBERRY.BTN2, 1)
                    RASPBERRY.write_I2C_PIN(RASPBERRY.BTN3, 1)
                    RASPBERRY.write_I2C_PIN(RASPBERRY.BTN4, 1)
                    RASPBERRY.write_I2C_PIN(RASPBERRY.BTN5, 1)
                    RASPBERRY.write_I2C_PIN(RASPBERRY.BTN6, 1)
                    RASPBERRY.write_I2C_PIN(RASPBERRY.BTN7, 1)

                    time.sleep(1)

                    logger.info(" ")
                    logger.info("Send LER BTN")
                    DATA = '\x08' + '\x00' + '\x00' + '\x00' + '\x00' + '\x00' + '\x00' + '\x00'
                    RASPBERRY.Port.serial.write(DATA)

                    time.sleep(2)
                    # Ler reguladores e enviar para o controlador
                    logger.info(" ")
                    logger.info("Reguladores OK")
                    DATA = '\x06' + '\x01' + '\x00' + '\x00' + '\x00' + '\x00' + '\x00' + '\x00'
                    RASPBERRY.Port.serial.write(DATA)
                    RASPBERRY.Status_REGULADOR = True

                    time.sleep(5)

                    if RASPBERRY.Status_PRESSAO and RASPBERRY.Status_XBEE and RASPBERRY.Status_ENERGIA and \
                            RASPBERRY.Status_OPTO and RASPBERRY.Status_RELE and RASPBERRY.Status_REGULADOR and \
                            RASPBERRY.Status_BTN:

                        logger.info(" ")
                        logger.info("Finalizado com SUCESSO")
                        DATA = '\x08' + '\x01' + '\x00' + '\x00' + '\x00' + '\x00' + '\x00' + '\x00'
                        RASPBERRY.Port.serial.write(DATA)
                        RASPBERRY.STATUS_GREEN_LED = 1
                        RASPBERRY.STATUS_RED_LED = 0
                    else:
                        logger.info(" ")
                        logger.info("Finalizado com ERRO")
                        if RASPBERRY.Status_PRESSAO == 0:
                            logger.info(" ERRO na Pressao")
                        if RASPBERRY.Status_XBEE == 0:
                            logger.info(" ERRO no XBee")
                        if RASPBERRY.Status_ENERGIA == 0:
                            logger.info(" ERRO na Energia")
                        if RASPBERRY.Status_OPTO == 0:
                            logger.info(" ERRO no OPTO")
                        if RASPBERRY.Status_RELE == 0:
                            logger.info(" ERRO no rele")
                        if RASPBERRY.Status_REGULADOR == 0:
                            logger.info(" ERRO no regulador")
                        DATA = '\x08' + '\x00' + '\x00' + '\x00' + '\x00' + '\x00' + '\x00' + '\x00'
                        RASPBERRY.Port.serial.write(DATA)
                        RASPBERRY.STATUS_GREEN_LED = 0
                        RASPBERRY.STATUS_RED_LED = 1

                    # Reseta Status
                    RASPBERRY.Status_OPTO = False
                    RASPBERRY.Status_RELE = False
                    RASPBERRY.Status_REGULADOR = False
                    RASPBERRY.Status_ENERGIA = False
                    RASPBERRY.Status_PRESSAO = False
                    RASPBERRY.Status_XBEE = False

                    RASPBERRY.write_I2C_PIN(RASPBERRY.BTN1, 0)
                    RASPBERRY.write_I2C_PIN(RASPBERRY.BTN2, 0)
                    RASPBERRY.write_I2C_PIN(RASPBERRY.BTN3, 0)
                    RASPBERRY.write_I2C_PIN(RASPBERRY.BTN4, 0)
                    RASPBERRY.write_I2C_PIN(RASPBERRY.BTN5, 0)
                    RASPBERRY.write_I2C_PIN(RASPBERRY.BTN6, 0)
                    RASPBERRY.write_I2C_PIN(RASPBERRY.BTN7, 0)

                    RASPBERRY.set_pin_HIGH(RASPBERRY.OPTO1)
                    RASPBERRY.set_pin_HIGH(RASPBERRY.OPTO2)
                    RASPBERRY.set_pin_HIGH(RASPBERRY.OPTO3)
                    RASPBERRY.set_pin_HIGH(RASPBERRY.OPTO4)
                    RASPBERRY.set_pin_HIGH(RASPBERRY.OPTOAUX)
                    RASPBERRY.set_pin_LOW(RASPBERRY.MOVE_IN)
        except KeyboardInterrupt:
            t2.join()
            logger.info("here 2")
            break


signal.signal(signal.SIGINT, signal_handler)

t1 = threading.Thread(target=read_thread)
t2 = threading.Thread(target=main_thread)
t3 = threading.Thread(target=FILA_thread)
t4 = threading.Thread(target=led_green)
t5 = threading.Thread(target=led_red)

t1.start()
t2.start()
t3.start()
t4.start()
t5.start()

t1.join()
t2.join()
t3.join()
t4.join()
t5.join()

RASPBERRY.clean_pins()

logger.info("Thread Finish")

