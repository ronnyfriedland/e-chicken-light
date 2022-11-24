import datetime
import os
import argparse

from suntime import Sun, SunTimeException

from _cron import *

parser = argparse.ArgumentParser(description="Job arguments",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-a", "--latitude", default=float(os.getenv('LAT', 0.0)), help="latitute")
parser.add_argument("-b", "--longitude", default=float(os.getenv('LNG', 0.0)), help="longitude")
parser.add_argument("-v", "--verbose", action="store_true", help="increase verbosity")
args = parser.parse_args()
config = vars(args)


sun = Sun(float(config["latitude"]), float(config["longitude"]))

now = datetime.datetime.now()


# Get today's sunrise and sunset in UTC
try:
    if config["verbose"] is True:
        print("latitude: {}".format(config["latitude"]))
        print("longitude: {}".format(config["longitude"]))

    today_sr = sun.get_sunrise_time()
    today_ss = sun.get_sunset_time()
    today_sunshine = today_ss - today_sr

    if config["verbose"] is True:
        print("sunrise: {}".format(today_sr))
        print("sunset: {}".format(today_ss))
        print("sunshine: {}".format(today_sunshine))

    if today_sunshine < datetime.timedelta(hours=10):
      today_duration = datetime.timedelta(hours=10) - today_sunshine

      if config["verbose"] is True:
        print("start: {}".format(today_ss))
        print("duration: {}".format(today_duration))

      # turn on the lights
      create_cron("e-chicken-light-job", "/usr/local/bin/python /usr/src/app/light.py --duration {duration}".format(duration = today_duration.seconds), start=today_ss)
    else:
      print('On {} at {} / {} the sunrise was at {} and the sunset was at {}.'.
          format(now, config["latitude"], config["longitude"], today_sr.strftime('%H:%M'), today_ss.strftime('%H:%M')))
except SunTimeException as e:
    print("Error: {0}.".format(e))
