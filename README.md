# Ultraheat
Script to read information from Landis+Gyr Ultraheat (UH50, T550)

With this script you can read a telegram from a Landis&Gyr Ultraheat 2WR5 'Stadsverwarming' meter. 
Most likely this also works for Ultraheat UH50 (T550).

This script sends the GJ and m3 values to Domoticz on the given IDX. 

## Installation and usage:
This script uses a optical probe (IEC 62056-21) on an USB port to read the telegrams from the meter.

Add a custom sensor with kJ and m3 Y-axis settings (Add through dummy sensor hardware). 
This is best done by adding a 'Counter' dummy sensor in Domoticz. Edit the device and select the 
'Counter' type. You will now also get 2 fields for 'Value quantity' and 'Value units'. A same type
of sensor can be added for the M3 value.

The script will send the values to Domoticz in kJ (1GJ = 1000kJ) and liters (not m3). This is to
make the graphs in Domoticz better. A usage of 0,11GJ compared with 0,12GJ will be on a very small 
scale, whereas 110kJ and 120kJ will give a better scale. 

## Warning:
It is said that every readout of the Ultraheat is shortening the livespan of the battery by 15 minutes. 
Usually these batteries last for many years, but please make sure you don't read the values too often. 
There is little added value in fetching the data very frequently. I fetch it a few times a day to get
an idea of the heat usage over a few parts of the day (every 6 hours). 

## Requirements:
- An optical probe (IEC 62056-21 standard) to place on the meter, for example: http://wiki.volkszaehler.org/hardware/controllers/ir-schreib-lesekopf-usb-ausgang
- Python3

## Source:
Original script from Magnat in https://gathering.tweakers.net/forum/list_messages/1535019
