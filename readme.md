# ShabbatCron
Schedules script executions relative to Shabbat and Hag in and out times.

* `start.sh` is executed at Shabbat start.
* `end.sh` is executed at Shabbat end.

Jewish Holidays are taken into account.

> Times are within close range to [chabbad.org](https://www.chabad.org/calendar/candlelighting_cdo/aid/6226/locationid/531/locationtype/1/save/1/jewish/Shabbat-Candle-Lighting-Times.htm)

# Installation
## Project
1. Download the files to `/home/pi/ShabbatCron/` 
1. Run `pip install -r requirements.txt`
> It is suggested to use a python virtual environment
## Service
```
sudo ln -s /home/pi/ShabbatCron/shabbat-cron.service /etc/systemd/system/shabbat-cron.service
sudo systemctl enable shabbat-cron.service
```
The service will automatically start at system boot.
* To manually start:
`sudo service shabbat-cron start`
* To manually stop:
`sudo service shabbat-cron stop`

## Settings
1. Adjust your physical location by adding an entry to `settings.ASTRAL_LOCATION_INFO`, and setting `settings.LOCATION`
1. Adjust the `START_DELTA` and `END_DELTA` variables to controls how many minutes before/after Shabbat/Hag the relay should be activated/deactivated
1. Adjust the `start.sh` and `stop.sh` scripts with your specific logic

## Note
`/home/pi/ShabbatCron/` is assumed as the projet directory, and `/usr/bin/python3` for python.<BR>
Adjust `shabbat-ron.service` for your specific setup.

# Acknowledgments
## usbrelay
Many thanks to Darryl Bond for providing the fantastic relay driver: https://github.com/darrylb123/usbrelay
<BR>Darryl's `usbrelay` is used in the sample bash scripts to turn on and off relays.

### Driver Installation
```
sudo apt-get install usbrelay
sudo nano /etc/udev/rules.d/50-dct-tech-usb-relay-2.rules
    SUBSYSTEM=="usb", ATTR{idVendor}=="16c0",ATTR{idProduct}=="05df", MODE="0666"
    KERNEL=="hidraw*", ATTRS{busnum}=="1", ATTRS{idVendor}=="16c0", ATTRS{idProduct}=="05df", MODE="0666"
```
Test:
```
sudo usbrelay X0L7N_1=1
sudo usbrelay X0L7N_2=1
```
