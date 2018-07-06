import csv
import pandas
import urllib2

#Find closing dates (every month --> 3rd week --> wednesday)

cboe_calendar = pandas_market_calendars.calendar_utils.get_calendar('CME')
