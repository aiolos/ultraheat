##################################################################################################
# Script to read telegram from Landis&Gyr Ultraheat 2WR5 'Stadsverwarming'                       #
# Might also work for Ultraheat UH50 (T550)                                                      #
#                                                                                                #
# This script sends the GJ and m3 values to Domoticz on the given IDX                            #
# Add a custom sensor with GJ and m3 Y-axis settings (Add through dummy sensor hardware)         #
#                                                                                                #
# Source:                                                                                        #
# Script from Magnat in https://gathering.tweakers.net/forum/list_messages/1535019               #
#                                                                                                #
# Requirement: Python3                                                                           #
##################################################################################################

import serial
import re
import requests
from time import sleep

conn = serial.Serial('/dev/ttyUSB1',
                     baudrate=300,
                     bytesize=serial.SEVENBITS,
                     parity=serial.PARITY_EVEN,
                     stopbits=serial.STOPBITS_TWO,
                     timeout=1,
                     xonxoff=0,
                     rtscts=0
                     )

# Wake up
conn.setRTS(False)
conn.setDTR(False)
sleep(5)
conn.setDTR(True)
conn.setRTS(True)

# send /?!
conn.write(str.encode("\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x2F\x3F\x21\x0D\x0A"))

# Read at 300 BAUD, typenr
print(conn.readline())
print(conn.readline())

# Read at 2400 BAUD, higher might be possible
conn.baudrate=2400

# Read 18 lines (the size of the telegram)
counter = 0
try:
    while counter < 18:
        line=conn.readline().decode('utf-8')
        print(line)

        # This will match on the first line of the telegram with GJ and m3 values.
        matchObj = re.match(r".+6\.8\(([0-9]{4}\.[0-9]{3})\*GJ\)6\.26\(([0-9]{5}\.[0-9]{2})\*m3\)9\.21\(([0-9]{8})\).+", line, re.I|re.S)
        if matchObj:
            print("GJ : ")
            print(matchObj.group(1))
            print("m3: ")
            print(matchObj.group(2))

            # IDX of the GJ sensor
            idx=str(3783)
            url="http://192.168.38.110:8080/json.htm?type=command&param=udevice&idx=" + idx + "&nvalue=0&svalue=" + str(float(matchObj.group(1)))
            print(url)
            requests.get(url)

            # IDX of the m3 sensor
            idx=str(3785)
            url="http://192.168.38.110:8080/json.htm?type=command&param=udevice&idx=" + idx + "&nvalue=0&svalue=" + str(float(matchObj.group(2)))
            print(url)
            requests.get(url)
        counter = counter + 1
finally:
    conn.close()
