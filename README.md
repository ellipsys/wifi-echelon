# wifi-echelon
Passive monitor for wifi-devices.

```sh
$ sudo su
$ python3 monitor.py wlan0
```

And simultaneously:

```sh
$ sudo su
$ var=13; while true; do iwconfig wlx801f02af45b3 channel $var; echo 'Channel '$var; sleep 5; var=$((var%13)); var=$((var+1)); done
```
