# -*- coding: utf-8 -*-
""" Passive wifi monitor """
import os
import sys
from datetime import datetime, timedelta
from os import devnull

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
    cmd = cmd+"channel $var; echo 'Channel '$var; sleep 5; "
    cmd = cmd+"var=$((var%"+str(channels)+")); var=$((var+1)); done"
    print('\033[1;32m Run this command simultaneously: \033[1;m')
    print('\033[1;32m sudo su \033[1;m')
    print('\033[1;32m %s \033[1;m' % cmd)
    # from subprocess import Popen, PIPE
    # p = Popen(cmd, stdin=PIPE, shell=True, stdout=open(devnull, "w"))

    cmd = "tshark -i " + interface + " -n -l subtype probereq"
    timestamp = datetime.now() - timedelta(weeks=1040)
    device_dictionary = { # ff:ff:ff:ff:ff:ff
        "ff:ff:ff:ff:ff:ff": { "name": "DEVICE1", "seen": timestamp },
        "ff:ff:ff:ff:ff:ff": { "name": "DEVICE2", "seen": timestamp },
        "ff:ff:ff:ff:ff:ff": { "name": "DEVICE3", "seen": timestamp },
        }
    past = datetime(1980, 1, 1)
    print('\033[1;30m %s \033[1;m' % cmd)
    pipe = os.popen(cmd)
    while True:
        line = pipe.readline()
        if not line:
            break
        line_list = line.strip().split(" ")
        SSID = line_list[-1]
        device = line_list[2]
        station = line_list[4]
        timestamp = datetime.now()
        timestamp = datetime.strftime(timestamp, '%Y-%m-%d %H:%M:%S')
        obj = device_dictionary.get(device)
        if obj:
            seen = obj["seen"]
            device_dictionary[device]["seen"] = datetime.now()
            device = obj["name"]
            if seen > (datetime.now() - timedelta(minutes=5)):
                continue
            else:
                if seen < (datetime.now() - timedelta(weeks=520)):
                    seen = "never"
                else:
                    seen = datetime.strftime(seen, '%Y-%m-%d %H:%M:%S')
                info = "Device %s arrived, last seen %s" % (device, seen)
                print('\033[1;32m %s \033[1;m' % info)
        info = "%s: %s --> %s %s" % (timestamp, device, station, SSID)
        print('\033[1;32m %s \033[1;m' % info)
    p.terminate()

if __name__ == '__main__':
    main()
