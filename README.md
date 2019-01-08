# Ultraheat
Script to read information from Landis+Gyr Ultraheat (UH50, T550)

With this script you can read a telegram from a Landis&Gyr Ultraheat 2WR5 'Stadsverwarming' meter
Might also work for Ultraheat UH50 (T550)

This script sends the GJ and m3 values to Domoticz on the given IDX
Add a custom sensor with GJ and m3 Y-axis settings (Add through dummy sensor hardware)

## Installation and usage:
This script uses a optical probe (IEC 62056-21) on an USB port to read the telegrams from the meter. 

## Warning:
It is said that every readout of the ultraheat is shortening the livespan of the battery by 15 minutes. 
Usually these batteries last for many years, but please make sure you don't read the values too often. 
There is little added value in fetching the data very frequently. I fetch it a few times a day to get
an idea of the heat usage over a few parts of the day (every 6 hours). 

## Requirements:
- An optical probe (IEC 62056-21 standard) to place on the meter, for example: http://wiki.volkszaehler.org/hardware/controllers/ir-schreib-lesekopf-usb-ausgang
- Python3

## Source:
Original script from Magnat in https://gathering.tweakers.net/forum/list_messages/1535019
