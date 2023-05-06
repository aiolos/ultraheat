##################################################################################################
# Script to read telegram from Landis&Gyr Ultraheat 2WR5 'Stadsverwarming'                       #
# Might also work for Ultraheat UH50 (T550)                                                      #
#                                                                                                #
# This script sends the MJ and m3 values to MATT on the given IP with user/pass                  #
# See ultraheat_ha_mqtt.yaml for an example for home assistant configuration                     #
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
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import ssl

conn = serial.Serial('/dev/serial/by-id/usb-Silicon_Labs_CP2104_USB_to_UART_Bridge_Controller_010658AC-if00-port0',
                     baudrate=300,
                     bytesize=serial.SEVENBITS,
                     parity=serial.PARITY_EVEN,
                     stopbits=serial.STOPBITS_TWO,
                     timeout=1,
                     xonxoff=0,
                     rtscts=0
                     )

auth = {
  'username':"esp",
  'password':"password"
}

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
            kjValue=round(float(matchObj.group(1)) * 1000)
            m3Value=round(float(matchObj.group(2)) * 1000)
            print("GJ : " + str(kjValue))
            print("m3: " + str(m3Value))

            publish.single("ultraheat/heat",
              payload=str(kjValue),
              hostname="192.168.38.79",
              client_id="ultraheat",
              auth=auth,
              port=1883,
              protocol=mqtt.MQTTv311)

            publish.single("ultraheat/volume",
              payload=str(m3Value),
              hostname="192.168.38.79",
              client_id="ultraheat",
              auth=auth,
              port=1883,
              protocol=mqtt.MQTTv311)
        counter = counter + 1
finally:
    conn.close()
