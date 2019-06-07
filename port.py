import serial, logging
from time import sleep

logger = logging.getLogger(__name__)

PORT = "/dev/ttyAMA0"
BAUD_RATE = 9600

class Port():
    def __init__(self):
        self.serial = serial.Serial()

    def open(self):
        """
        Funcao que abre a porta serial
        """
        t = False
        while not self.serial.is_open:
            try:
                self.serial.port = PORT
                self.serial.baudrate = BAUD_RATE
                self.serial.open()
                break
            except Exception:
                if not t:
                    logger.info("Error open serial: " + str(PORT) + ': ' + str(BAUD_RATE))
                    t = True
                sleep(5)
            except KeyboardInterrupt:
                break
        logger.info("Conected PORT: " + str(self.serial.port) + " - " + str(self.serial.baudrate))

    def get_serial(self):
        return self.serial
