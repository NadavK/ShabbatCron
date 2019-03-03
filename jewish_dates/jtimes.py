import astral
import datetime
from settings import LOCATION, ASTRAL_LOCATION_INFO

CANDLELIGHT_DELTA = 20
astral._LOCATION_INFO = ASTRAL_LOCATION_INFO

def __sunrise_sunset_astral(date):
    # local False for UTC
    geo = astral.Astral(astral.AstralGeocoder).geocoder[LOCATION]
    return geo.sun(local=True, date=date)


def sunrise_sunset(date):
    if not date:
        date = datetime.datetime.now()
    sun = __sunrise_sunset_astral(date=date)
    return sun['sunrise'], sun['sunset']


def stars_out(date=None, degrees=None):
    if not date:
        date = datetime.datetime.now()
    geo = astral.Astral(astral.AstralGeocoder).geocoder[LOCATION]
    if degrees is not None:
        geo.solar_depression = degrees
    dusk = geo.dusk(local=True, date=date)
    return dusk


def shaa_zmanit(sunrise, sunset):
    sr = sunrise.hour * 60 + sunrise.minute
    ss = sunset.hour * 60 + sunset.minute
    return round((ss - sr) / 0.12) / 100        #round to two decimal places


def day_hours(sunrise, sunset):
    sr = sunrise.hour * 60 + sunrise.minute
    ss = sunset.hour * 60 + sunset.minute
    return round((ss - sr) / 0.6) / 100         #round to two decimal places


def night_hours(sunrise, sunset):
    return 24 - day_hours(sunrise, sunset)


def get_day_times(date=None):
    '''Returns sunrise, sunset, shaa_zmanit, day_hours, night_hours, tz_offset'''
    #tz_offset = -time.altzone / 60 / 60

    if not date:
        #from dateutil.tz import tzlocal
        #date = datetime.datetime.now(tzlocal())
        date = datetime.datetime.now()

    #https://stackoverflow.com/questions/3168096/getting-computers-utc-offset-in-python
    #tz_offset = date.tzinfo.utcoffset(date).seconds//60//60

    sunrise, sunset = sunrise_sunset(date)
    shaazmanit = shaa_zmanit(sunrise, sunset)
    dayhours = day_hours(sunrise, sunset)
    nighthours = night_hours(sunrise, sunset)
    #print('sunrise: %s, sunset: %s, shaa-zmanit: %s, day-hours: %s, night-hours: %s, tz_offset: %s' % (sunrise, sunset, shaazmanit, dayhours, nighthours, tz_offset))
    return sunrise, sunset, shaazmanit, dayhours, nighthours#, tz_offset


def shabbat_start(date):
    return sunrise_sunset(date)[1] - datetime.timedelta(minutes=CANDLELIGHT_DELTA)


def shabbat_end(date=None):
    if not date:
        date = datetime.datetime.now()
    #sunrise, sunset = sunrise_sunset(date)
    #minutes = 18 / 60 * shaa_zmanit(sunrise, sunset)
    return stars_out(date, 8.5) #+ datetime.timedelta(minutes=minutes)


def shabbat_times(num):
    def next_friday(date):
        # returns closest fri, or next fri if today is fri
        # http://stackoverflow.com/questions/8801084/how-to-calculate-next-friday-in-python
        friday = 4  # 0 based, starting from Monday
        return date + datetime.timedelta(((friday - 1) - date.weekday()) % 7 + 1)

    # returns the next <num> shabbat times

    # a = astral.Astral(astral.AstralGeocoder)
    # geo = a.geocoder

    times = []

    fri = datetime.datetime.today()
    for i in range(1, num):
        fri = next_friday(fri)
        # print ('raanana_wiki  ', sunrise_sunset_jd(locations['raanana_wiki'], fri)[1] - datetime.timedelta(minutes=candlelight))
        # print ('raanana_google', sunrise_sunset_jd(locations['raanana_google'], fri)[1] - datetime.timedelta(minutes=candlelight))
        # print ('*Raanana_wiki  ', sunrise_sunset_astral(geo['Raanana_wiki'], fri)['sunset'] - datetime.timedelta(minutes=candlelight))
        # print ('Raanana_google', sunrise_sunset_astral(geo['Raanana_google'], fri)['sunset'] - datetime.timedelta(minutes=candlelight))
        # times.append(sunrise_sunset(fri)[1] - datetime.timedelta(minutes=candlelight))
        times.append(shabbat_start(fri, CANDLELIGHT_DELTA))
    return times
