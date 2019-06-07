import smbus


class I2C:
    def __init__(self, address):
        self.channel = 1
        self.address = address
        self.bus = smbus.SMBus(self.channel)

    def write(self, register, msg):
        # self.bus.write_i2c_block_dat(self.address, register, msg)
        self.bus.write_byte_data(self.address, register, msg)

    def read(self, register):
        data = self.bus.read_byte_data(self.address, register)
        return data
