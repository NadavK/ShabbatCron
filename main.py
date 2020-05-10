#!/usr/bin/python3

from apscheduler.schedulers.background import BackgroundScheduler
import asyncio
import datetime
import getopt
import logging
import os
import signal
import subprocess
import sys
from tzlocal import get_localzone

from jewish_dates import jtimes
from jewish_dates.holidays import is_hag, is_erev_hag, is_motzei_hag
import settings


class Scheduler:

    def __init__(self):
        self.loop = None
        self.scheduler = None

    def run_start_script(self):
        logging.debug('Running start script')
        self.run_script(settings.START_SCRIPT)

    def run_end_script(self):
        logging.debug('Running end script')
        self.run_script(settings.END_SCRIPT)

    def run_script(self, script):
        try:
            proc = subprocess.run(['bash', script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            logging.debug(proc.stdout.decode('utf-8'))
            logging.debug(proc.stderr.decode('utf-8'))
        except Exception:
            logging.exception('ERROR: set_relay')

    @staticmethod
    def get_times(date=None):
        if not date:
            date = datetime.date.today()

        start_time = jtimes.shabbat_start(date) + datetime.timedelta(minutes=settings.START_DELTA)
        end_time = jtimes.shabbat_end(date) + datetime.timedelta(minutes=settings.END_DELTA)
        return start_time, end_time

    def schedule_logic(self):
        start_time, end_time = self.get_times()
        today = datetime.datetime.now(get_localzone())

        if is_hag(today):
            logging.debug('Today is hag - start')
            self.run_start_script()
        elif is_erev_hag(today):
            if today > start_time:
                logging.debug('Erev has passed - start')
                self.run_start_script()
            else:
                logging.debug('Not yet Erev - end, and schedule job')
                self.run_end_script()

                logging.debug('Scheduling start for: {0}'.format(start_time))
                self.scheduler.add_job(self.run_start_script, 'date', run_date=start_time, misfire_grace_time=5, args=[])
                self.scheduler.print_jobs()
        elif is_motzei_hag(today):
            if today > end_time:
                logging.debug('Motzei has passed - end')
                self.run_end_script()
            else:
                logging.debug('Not yet Motzei - start, and schedule job')
                self.run_start_script()

                logging.debug('Scheduling end for: {0}'.format(end_time))
                self.scheduler.add_job(self.run_end_script, 'date', run_date=end_time, misfire_grace_time=2, args=[])
                self.scheduler.print_jobs()
        else:
            logging.debug('Today is not hag - end')
            self.run_end_script()

    def main(self):
        self.loop = asyncio.get_event_loop()
        self.scheduler = BackgroundScheduler(timezone=get_localzone(), standalone=False)
        signal.signal(signal.SIGINT, self.handler_stop_signals)
        signal.signal(signal.SIGTERM, self.handler_stop_signals)

        try:
            # ensure single instance process
            logging.info('=================== ShabbatCron Starting ===================')
            print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

            # Daily job
            self.scheduler.add_job(self.schedule_logic, 'cron', hour='3', minute='0', args=[])      # 3am is after summer/winter time change
            self.scheduler.start()
            self.scheduler.print_jobs()
            self.schedule_logic()  # and run it now

            logging.debug('waiting...')
            self.loop.run_forever()
        except SystemExit:
            logging.debug('System Exiting')
        except Exception:
            logging.exception('unhandled exception')

        try:
            self.loop.close()
            self.scheduler.shutdown(wait=False)
        except Exception:
            pass
        logging.info('=================== ShabbatCron Stopped ===================')

    def handler_stop_signals(self, signum, frame):
        print('Received stop signal', signum)
        logging.info('Received stop signal ' + str(signum))
        print('Stopping')
        logging.info('Stopping')
        self.loop.shutdown_asyncgens()
        self.loop.stop()
        exit()

    def print_times(self):
        start, end = self.get_times()
        logging.info('Open: %s, Close: %s' % (start.strftime('%X'), end.strftime('%X')))
        sunrise, sunset, shaa_zmanit, day_hours, night_hours = jtimes.get_day_times()
        logging.info('sunrise: %s, sunset: %s, stars: %s, shaa zmanit: %s, daka zmanit: %s, day hours: %s, night hours: %s' %
                     (sunrise.strftime('%X'), sunset.strftime('%X'), jtimes.stars_out().strftime('%X'), shaa_zmanit, shaa_zmanit / 60, day_hours, night_hours))

    def test(self, year):
        print('Testing, year=' + year)
        date = datetime.date(int(year), 1, 1)
        for i in range(1, 366):
            today = date + datetime.timedelta(days=i)
            if is_erev_hag(today):
                print(today, ' erev', '        ' if today.weekday() == 4 else '-Hag    ', self.get_times(today)[0], sep='')
            if is_hag(today):
                print(today, 'Hag (all-day)')
            if is_motzei_hag(today):
                print(today, ' motszei', '     ' if today.weekday() == 5 else '-Hag ', self.get_times(today)[1], sep='')


if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ht:i:oc", ["test=", "times", "open", "close"])
    except getopt.GetoptError as e:
        print(e)
        print('options: -test=<year> --times --open --close')
        sys.exit(2)
    for opt, arg in opts:
        scheduler = Scheduler()
        if opt == '-h':
            print('options: -test=<year> --times --open --close')
        elif opt in ("-t", "-test", "--test"):
            scheduler.test(arg)
        elif opt in ("-i", "-times", "--times"):
            scheduler.print_times()
        elif opt in ("-n", "-open", "--open"):
            print('Opening gate')
            scheduler.run_start_script()
        elif opt in ("-f", "-close", "--close"):
            print('Closing gate')
            scheduler.run_end_script()
        exit()

    try:
        logging.info('Starting main')
        scheduler = Scheduler()
        scheduler.main()
    except Exception:
        logging.exception('main exception caught')
    logging.info('Exiting main')
