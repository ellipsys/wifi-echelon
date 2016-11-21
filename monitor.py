# -*- coding: utf-8 -*-
""" Passive wifi monitor """
import os
import sys
from os import devnull
from subprocess import Popen, PIPE

def printErrorAndQuit():
    """Printing the usage information"""
    print("Passive wifi monitor.\n")
    print("Usage: python3 monitor.py interface")
    print("Example: python3 monitor.py wlan0\n")
    sys.exit()

def main():
    # Read command line arguments
    try:
        if len(sys.argv) == 2 and len(str(sys.argv[1])) >= 4:
            interface = str(sys.argv[1])
            monitor(interface)
        else:
            printErrorAndQuit()
    except Exception as e:
        print( str(e) )
        printErrorAndQuit()

def monitor(interface):
    """ Passive wifi monitor """
    print('\033[1;30m Testing to monitor interface %s \033[1;m' % interface)
    cmd = "iwconfig "+interface
    print('\033[1;30m %s \033[1;m' % cmd)
    out = os.popen(cmd).read()
    print(out)
    if not "ESSID" in out and not "IEEE" in out:
        print('\033[1;31m No such device \033[1;m')
        sys.exit()
    else:
        print('\033[1;32m Interface %s is available. \033[1;m' % interface)

    cmd = 'iw phy | grep -A 10 "Supported interface modes" | grep monitor'
    print('\033[1;30m %s \033[1;m' % cmd)
    out = os.popen(cmd).read()
    if not "monitor" in out:
        print('\033[1;31m Device does not support monitoring. \033[1;m')
        sys.exit()
    else:
        print('\033[1;32m Device supports monitoring. \033[1;m')

    cmd = "ifconfig wlx801f02af45b3 down"
    print('\033[1;30m %s \033[1;m' % cmd)
    out = os.popen(cmd).read()

    cmd = "iwconfig wlx801f02af45b3 mode monitor"
    print('\033[1;30m %s \033[1;m' % cmd)
    out = os.popen(cmd).read()

    cmd = "ifconfig wlx801f02af45b3 up"
    print('\033[1;30m %s \033[1;m' % cmd)
    out = os.popen(cmd).read()

    cmd = "iwlist wlx801f02af45b3 freq | grep -v Current | grep -c Channel"
    print('\033[1;30m %s \033[1;m' % cmd)
    channels = int(os.popen(cmd).read())

    cmd = "var="+str(channels)+"; while true; do iwconfig "+interface+" "
    cmd = cmd+"channel $var; sleep 5; var=$((var%"+str(channels)+"));"
    cmd = cmd+" var=$((var+1)); done"
    print('\033[1;30m %s \033[1;m' % cmd)
    p = Popen(cmd, stdin=PIPE, shell=True, stdout=open(devnull, "w"))

    cmd = "tshark -i " + interface + " -n -l subtype probereq"
    print('\033[1;30m %s \033[1;m' % cmd)
    pipe = os.popen(cmd)
    ssids = []
    devices = []
    device_dictionary = {
        "ff:ff:ff:ff:ff:ff": "mylaptop",
        "ff:ff:ff:ff:ff:ff": "myphone",
        }
    while True:
        line = pipe.readline()
        if not line:
            break
        line_list = line.strip().split(" ")
        SSID = line_list[-1]
        device = line_list[2]
        station = line_list[4]
        if SSID in ssids and device in devices:
            continue
        devices.append(device)
        ssids.append(SSID)
        name = device_dictionary.get(device)
        if name:
            device = name
        print('\033[1;32m %s --> %s %s \033[1;m' % (device, station, SSID))
    p.terminate()

if __name__ == '__main__':
    main()
