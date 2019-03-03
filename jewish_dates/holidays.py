import datetime
from pyluach.dates import GregorianDate


def _is_hag_or_shabbat(date, diaspora=False):
    if date.weekday() == 5:
        return 'Shabbat'

    # Returns the name of the Hag
    hebYear, hebMonth, hebDay = GregorianDate(date.year, date.month, date.day).to_heb().tuple()

    # Holidays in Nisan
    if hebDay == 15 and hebMonth == 1:
        return "Pesach"
    if hebDay == 21 and hebMonth == 1:
        return "Pesach"

    # Holidays in Sivan
    if hebDay == 6 and hebMonth == 3:
        return "Shavuot"

    # Holidays in Elul
    if hebDay == 1 and hebMonth == 7:
        return "Rosh Hashana I"
    if hebDay == 2 and hebMonth == 7:
        return "Rosh Hashana II"

    # Holidays in Tishri
    if hebDay == 10 and hebMonth == 7:
        return "Yom Kippur"
    if hebDay == 15 and hebMonth == 7:
        return "Sukkot"
    if hebDay == 22 and hebMonth == 7:
        return "Simchat Torah"


def is_erev_hag(date):
    # returns true if date is erev_heg or Friday
    tomorrow = date + datetime.timedelta(days=1)
    return _is_hag_or_shabbat(tomorrow) and not _is_hag_or_shabbat(date)


def is_hag(date):
    # returns true if date is heg or Shabbat, but not motzei
    return _is_hag_or_shabbat(date) and not is_motzei_hag(date)


def is_motzei_hag(date):
    # returns true if hag finishes tonight
    tomorrow = date + datetime.timedelta(days=1)
    return _is_hag_or_shabbat(date) and not _is_hag_or_shabbat(tomorrow)


def test_calculate_holiday(year):
    date = datetime.date(int(year), 1, 1)
    for i in range(1, 366):
        today = date + datetime.timedelta(days=i)
        if is_erev_hag(today):
            print(today, 'erev', '' if today.weekday()==4 else 'erev Hag')
        if is_hag(today):
            print(today, 'hag', '' if today.weekday()==5 else 'Hag')
        if is_motzei_hag(today):
            print(today, 'motszei', '' if today.weekday()==5 else 'Hag')
