"""
Check if light sould be turned on
"""
import datetime
import os
import argparse

from suntime import Sun, SunTimeException

from _cron import create_cron

parser = argparse.ArgumentParser(description="Job arguments",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-a", "--latitude", default=float(os.getenv('LAT', '0.0')), help="latitute")
parser.add_argument("-b", "--longitude", default=float(os.getenv('LNG', '0.0')), help="longitude")
parser.add_argument("-v", "--verbose", action="store_true", help="increase verbosity")
args = parser.parse_args()
config = vars(args)


sun = Sun(float(config["latitude"]), float(config["longitude"]))

now = datetime.datetime.now()


# Get today's sunrise and sunset in UTC
try:
    if config["verbose"] is True:
        print(f"latitude: {config['latitude']}")
        print(f"longitude: {config['longitude']}")

    today_sr = sun.get_sunrise_time()
    today_ss = sun.get_sunset_time()
    today_sunshine = today_ss - today_sr

    if config["verbose"] is True:
        print(f"sunrise: {today_sr}")
        print(f"sunset: {today_ss}")
        print(f"sunshine: {today_sunshine}")

    if today_sunshine < datetime.timedelta(hours=10):
        today_duration = datetime.timedelta(hours=10) - today_sunshine

        if config["verbose"] is True:
            print(f"start: {today_ss}")
            print(f"duration: {today_duration}")

        # turn on the lights
        create_cron("e-chicken-light-job",
            f"/usr/local/bin/python /usr/src/app/light.py --duration {today_duration.seconds}", start=today_ss)
    else:
        print(f"On {now} at {config['latitude']} / {config['longitude']} the sunrise was at {today_sr.strftime('%H:%M')} and the sunset was at {today_ss.strftime('%H:%M')}.")
except SunTimeException as e:
    print(f"Error: {e}.")
