#!/usr/bin/env python
# -*- coding: utf-8 -*-
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from periphery import SPI
import time
#if you are using RaspberryPi use 
from RPi import GPIO as io

#if you are using OrangePi use following library
#from pyA20.gpio import gpio as io
#from pyA20.gpio import port

#for RaspberryPi init GPIO and SPI
io.setmode(io.BOARD)
io.setup(26, io.OUT)
io.output(26, io.HIGH)

spi = SPI("/dev/spidev0.0", 0, 1000000)

#for Orange Pi init GPIO and SPI
#cs  = port.PA13                         # Chip select pin
#spi = SPI("/dev/spidev1.0", 0, 1000000) # Spi port
#io.init()                 # init GPIO
#io.setcfg(cs, io.OUTPUT)  # configure cs Pin as output pin.

RDCV    = 0x04   # Read cells
STCVAD  = 0x10   # Start all A/D's - poll status

address = 0x80   # as we are connecting only one IC the address is 0x80
                 # refer the datasheet for the details about addressing of LTC6802

# refer datasheet for more details about configuration.
Config = [0x01, 0x01, 0x00, 0x00, 0x00, 0x71, 0xAB]

def writeCfg():

   """
   Writes the configuration to IC.
   """
   io.output(cs, io.LOW)            # make CS low
   data_in = spi.transfer(Config)   # write the config to IC and read the OP
   io.output(cs, io.HIGH)           # make CS high
   
def readVoltage():

    """
    Returns a dictionary containing the voltages of 12 battries.
    """

    v = {}
    io.output(cs, io.LOW)            # make CS low
    data_out = [STCVAD]              
    data_in = spi.transfer(data_out) # start all A/D 
    time.sleep(0.02)
    io.output(cs, io.HIGH)           # make CS high
    io.output(cs, io.LOW)            # again make CS low
    spi.transfer([0x80])             # write the address 0x80 to SPI
    spi.transfer([RDCV])             # (command to) read cells

    data = []

    for i in range(18):                   # read 18 bytes from the IC
        data.append(spi.transfer([RDCV]))
    io.output(cs, io.HIGH)


    # refer the datasheet of LTC6802 for conversion of ADC value to Voltages.
    
    # here we are calculating voltages from ADC values of all 12 battries.

    v['0']  = ((data[0][0] & 0xFF) | (data[1][0] & 0x0F) << 8)*1.5*0.001
    v['1']  = ((data[1][0] & 0xF0) >> 4 | (data[2][0] & 0xFF) << 4)*1.5*0.001
    v['2']  = ((data[3][0] & 0xFF) | (data[4][0] & 0x0F) << 8)*1.5*0.001
    v['3']  = ((data[4][0] & 0xF0) >> 4 | (data[5][0] & 0xFF) << 4)*1.5*0.001

    v['4']  = ((data[6][0] & 0xFF) | (data[7][0] & 0x0F) << 8)*1.5*0.001
    v['5']  = ((data[7][0] & 0xF0) >> 4 | (data[8][0] & 0xFF) << 4)*1.5*0.001
    v['6']  = ((data[9][0] & 0xFF) | (data[10][0] & 0x0F) << 8)*1.5*0.001
    v['7']  = ((data[10][0] & 0xF0) >> 4 | (data[11][0] & 0xFF) << 4)*1.5*0.001

    v['8']  = ((data[12][0] & 0xFF) | (data[13][0] & 0x0F) << 8)*1.5*0.001
    v['9'] = ((data[13][0] & 0xF0) >> 4 | (data[14][0] & 0xFF) << 4)*1.5*0.001
    v['10'] = ((data[15][0] & 0xFF) | (data[16][0] & 0x0F) << 8)*1.5*0.001
    v['11'] = ((data[16][0] & 0xF0) >> 4 | (data[17][0] & 0xFF) << 4)*1.5*0.001
    
    return v

def readVal():

    while True:
        writeCfg()
        time.sleep(0.001)
        v = readVoltage()
        print(v)
        time.sleep(1)
        
if __name__ == '__main__':

    readVal()
