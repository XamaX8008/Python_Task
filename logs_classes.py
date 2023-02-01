import datetime
import re
import statistics
import unittest
from collections import defaultdict, OrderedDict


def convert_month(month):
    map_months = {"Jan": 1, "Feb": 2,
                  "Mar": 3, "Apr": 4,
                  "May": 5, "Jun": 6,
                  "Jul": 7, "Aug": 8,
                  "Sep": 9, "Oct": 10,
                  "Nov": 11, "Dec": 12}

    return map_months[month]


def get_last_item(dictionary, value):
    last_item = None

    for i in dictionary:
        if dictionary[i] == value:
            last_item = i

    return last_item


def get_smallest_lexicographically(dictionary, value):
    smallest_lexicographically_item = None

    for i in dictionary:
        if dictionary[i] == value:
            if not smallest_lexicographically_item:
                smallest_lexicographically_item = i
            elif i < smallest_lexicographically_item:
                smallest_lexicographically_item = i

    return smallest_lexicographically_item


class Statistic:
    def __init__(self):
        self.time_processing = defaultdict(list)
        self.max_time_processing = defaultdict(int)
        self.min_time_processing = defaultdict(int)
        self.average_time_processing = defaultdict(float)
        self.most_active_user_day = defaultdict(lambda: defaultdict(int))
        self.users_activity = defaultdict(int)
        self.table_browsers = defaultdict(int)
        self.table_pages = defaultdict(int)

        self.slowest_page = ""
        self.average_slowest_page = ""
        self.fastest_page = ""
        self.most_popular_page = ""
        self.most_active_user = ""
        self.most_active_user_in_day = ""
        self.most_popular_browser = ""

    def add_line(self, line):
        data = re.findall(
            r'(.*?) - - \[(.*?)/(.*?)/(.*?):.*?]'
            r' \"(?:GET|PUT|POST|HEAD|'
            r'OPTIONS|DELETE) (.*?) .*?\" \d* '
            r'\d* \".*?\" \"(.*?)\" ?(\d*)',
            line
        )

        if data:
            self.statistics_update(data[0])

    def statistics_update(self, data):
        self.users_activity[data[0]] += 1
        self.most_active_user_day[
            datetime.date(
                int(data[3])
                , int(convert_month(data[2]))
                , int(data[1]))][data[0]] += 1
        self.table_pages[data[4]] += 1
        self.table_browsers[data[5]] += 1

        if data[6]:
            self.time_processing[data[4]].append(int(data[6]))

    def active_user_day(self):
        active_user = {}

        self.most_active_user_day = OrderedDict(
            sorted(self.most_active_user_day.items()))

        for i in self.most_active_user_day:
            maximum_quantity = max(self.most_active_user_day[i].values())

            active_user[i] = get_smallest_lexicographically(
                self.most_active_user_day[i],
                maximum_quantity)

        return active_user

    def get_time(self):
        for i in self.time_processing:
            self.max_time_processing[i] = max(self.time_processing[i])
            self.min_time_processing[i] = min(self.time_processing[i])
            self.average_time_processing[i] = int(statistics.mean(
                self.time_processing[i]))

    def results(self):
        self.get_time()

        if self.time_processing:
            self.slowest_page = get_last_item(
                self.max_time_processing,
                max(self.max_time_processing.values())
            )

            self.average_slowest_page = \
                max(self.average_time_processing,
                    key=self.average_time_processing.get)

            self.fastest_page = get_last_item(
                self.min_time_processing,
                min(self.min_time_processing.values())
            )

        if self.table_browsers:
            self.most_popular_page = get_smallest_lexicographically(
                self.table_pages, max(self.table_pages.values()))

            self.most_popular_browser = get_smallest_lexicographically(
                self.table_browsers, max(self.table_browsers.values()))

            self.most_active_user = get_smallest_lexicographically(
                self.users_activity, max(self.users_activity.values()))

        return {"FastestPage": self.fastest_page,
                "MostActiveClient": self.most_active_user,
                "MostActiveClientByDay": self.active_user_day(),
                "MostPopularBrowser": self.most_popular_browser,
                "MostPopularPage": self.most_popular_page,
                "SlowestAveragePage": self.average_slowest_page,
                "SlowestPage": self.slowest_page}


class MyTests(unittest.TestCase):
    def test_empty(self) -> None:
        statistic = Statistic()

        expected = {
            'FastestPage': '',
            'MostActiveClient': '',
            'MostActiveClientByDay': {},
            'MostPopularBrowser': '',
            'MostPopularPage': '',
            'SlowestAveragePage': '',
            'SlowestPage': ''
        }

        self.assertDictEqual(expected, statistic.results())

    def test_incorrect_lines(self) -> None:
        statistic = Statistic()

        statistic.add_line('chinazes')
        statistic.add_line('ultrasanchizes')

        expected = {
            'FastestPage': '',
            'MostActiveClient': '',
            'MostActiveClientByDay': {},
            'MostPopularBrowser': '',
            'MostPopularPage': '',
            'SlowestAveragePage': '',
            'SlowestPage': ''
        }

        self.assertDictEqual(expected, statistic.results())

    def test_correct_and_incorrect_lines(self) -> None:
        statistic = Statistic()

        statistic.add_line('chinazes')
        statistic.add_line('ultrasanchizes')

        statistic.add_line(('192.168.74.151 - - [12/Mar/2022:11:22:22 +0100]'
                            ' "GET site HTTP/1.1" 200 432'
                            ' "http://callider.kontur/pause/index"'
                            ' "Tor'
                            ' Gecko/20100101 Firefox/18.0" 10'))

        statistic.add_line(('192.168.74.101 - - [22/Feb/2022:11:11:11 +0100]'
                            ' "GET /index/page HTTP/1.1" 200 432'
                            ' "http://callider.kontur/pause/index"'
                            ' "Opera" 1'))

        expected = {
            'FastestPage': '/index/page',
            'MostActiveClient': '192.168.74.101',
            'MostActiveClientByDay': {
                datetime.date(2022, 2, 22): '192.168.74.101',
                datetime.date(2022, 3, 12): '192.168.74.151'},

            'MostPopularBrowser': 'Opera',
            'MostPopularPage': '/index/page',
            'SlowestAveragePage': 'site',
            'SlowestPage': 'site'
        }

        self.assertDictEqual(expected, statistic.results())

    def test_lines_no_time(self) -> None:
        statistic = Statistic()

        statistic.add_line(('192.168.74.151 - - [12/Mar/2022:11:22:22 +0100]'
                            ' "GET site HTTP/1.1" 200 432'
                            ' "http://callider.kontur/pause/index"'
                            ' "Tor'
                            ' Gecko/20100101 Firefox/18.0" 10'))

        statistic.add_line(('192.168.74.101 - - [22/Feb/2022:11:11:11 +0100]'
                            ' "GET /index/page HTTP/1.1" 200 432'
                            ' "http://callider.kontur/pause/index"'
                            ' "Opera" 1'))

        expected = {
            'FastestPage': '/index/page',
            'MostActiveClient': '192.168.74.101',
            'MostActiveClientByDay': {
                datetime.date(2022, 2, 22): '192.168.74.101',
                datetime.date(2022, 3, 12): '192.168.74.151'},

            'MostPopularBrowser': 'Opera',
            'MostPopularPage': '/index/page',
            'SlowestAveragePage': 'site',
            'SlowestPage': 'site'
        }

        self.assertDictEqual(expected, statistic.results())


def make_stat() -> Statistic:
    statistic = Statistic()
    return statistic
