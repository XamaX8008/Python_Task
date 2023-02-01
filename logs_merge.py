#!/usr/bin/env python3

import unittest
import re
import datetime
from collections import OrderedDict


def merge(*iterables, key=lambda x: x):
    """Функция склеивает упорядоченные по ключу `key` и порядку «меньше»
    коллекции из `iterables`.

    Результат — итератор на упорядоченные данные.
    В случае равенства данных следует их упорядочить в порядке следования
    коллекций"""

    iterators = OrderedDict()

    for i in iterables:
        iterator = iter(i)

        try:
            iterators[iterator] = next(iterator)
        except StopIteration:
            pass

    ordered_data = []

    while iterators:
        min_line = min(iterators.items(), key=lambda x: key(x[1]))
        ordered_data.append(min_line[1])

        try:
            iterators[min_line[0]] = next(min_line[0])
        except StopIteration:
            del iterators[min_line[0]]

    return iter(ordered_data)


def log_key(s):
    """Функция по строке лога возвращает ключ для её сравнения по времени"""

    time = re.findall(r".*?\[(.*?) .*?", s)

    if time:
        return datetime.datetime.strptime(time[0], '%d/%b/%Y:%H:%M:%S')

    return datetime.datetime(2023, 1, 1, 0, 0, 0)


class TestTest(unittest.TestCase):
    def test_log_right(self):
        test_string = '--[11/Jan/2011:01:11:11 +0600]'
        self.assertEqual(datetime.datetime(2011, 1, 11, 1, 11, 11),
                         log_key(test_string))

    def test_log_line(self):
        test_string = ('192.168.12.205 - - [19/Feb/2013:16:40:25 +0600] '
                       '"GET /pause/ajaxPause?pauseConfigId=&admin=0 HTTP/1.1"'
                       ' 200 1470 "http://callider/pause/index" "Mozilla/4.0 '
                       '(compatible; MSIE 7.0; Windows NT 6.1; WOW64; '
                       'Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET '
                       'CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC '
                       '6.0; InfoPath.3; .NET4.0C; .NET4.0E)" 17268')
        self.assertEqual(datetime.datetime(2013, 2, 19, 16, 40, 25),
                         log_key(test_string))

    def test_log_wrong_line(self):
        test_string = 'bcjkscjsnkjvnkuednjk'
        self.assertEqual(datetime.datetime(2023, 1, 1, 0, 0, 0),
                         log_key(test_string))

    def test_merge_two_iterables(self):
        iterable_1 = [
            '192.168.74.78 - - [17/Feb/2013:07:47:39 +0600] "GET /pause/ajax'
            'Pause?pauseConfigId=&admin=0 HTTP/1.1" 200 986 "http://callider'
            '/pause/index" "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1;'
            ' WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; '
            '.NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0;'
            ' InfoPath.3; .NET4.0C; MS-RTC LM 8; .NET4.0E)" 26794'
        ]
        iterable_2 = [
            '192.168.12.61 - - [17/Feb/2013:07:47:37 +0600] "GET /pause/ajax'
            'Pause?pauseConfigId=&admin=0 HTTP/1.1" 200 985 "http://callider'
            '/pause/index" "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1;'
            ' Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET'
            ' CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; '
            '.NET4.0E)" 19841'
        ]
        expected_result = [
            '192.168.12.61 - - [17/Feb/2013:07:47:37 +0600] "GET /pause/ajax'
            'Pause?pauseConfigId=&admin=0 HTTP/1.1" 200 985 "http://callider'
            '/pause/index" "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1;'
            ' Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET'
            ' CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; '
            '.NET4.0E)" 19841',
            '192.168.74.78 - - [17/Feb/2013:07:47:39 +0600] "GET /pause/ajax'
            'Pause?pauseConfigId=&admin=0 HTTP/1.1" 200 986 "http://callider'
            '/pause/index" "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1;'
            ' WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; '
            '.NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0;'
            ' InfoPath.3; .NET4.0C; MS-RTC LM 8; .NET4.0E)" 26794'
        ]

        count = 0
        for i in merge(iterable_1, iterable_2, key=log_key):
            self.assertEqual(expected_result[count], i)
            count += 1

    def test_two_complex_iterables(self):
        iterable_1 = [
            '192.168.12.61 - - [17/Feb/2013:07:47:37 +0600] "GET /pause/ajax'
            'Pause?pauseConfigId=&admin=0 HTTP/1.1" 200 985 "http://callider'
            '/pause/index" "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1;'
            ' Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET'
            ' CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; '
            '.NET4.0E)" 19841',
            '192.168.74.78 - - [17/Feb/2013:07:47:39 +0600] "GET /pause/ajax'
            'Pause?pauseConfigId=&admin=0 HTTP/1.1" 200 986 "http://callider'
            '/pause/index" "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1;'
            ' WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; '
            '.NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0;'
            ' InfoPath.3; .NET4.0C; MS-RTC LM 8; .NET4.0E)" 26794'
        ]
        iterable_2 = [
            '192.168.12.54 - - [16/Feb/2013:16:40:26 +0600] "GET /pause/ajax'
            'Pause?pauseConfigId=&admin=0 HTTP/1.1" 200 1040 "http://callider'
            '/pause/index" "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1;'
            ' WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; '
            '.NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; '
            'InfoPath.3; .NET4.0C; .NET4.0E)" 16048']
        expected_result = [
            '192.168.12.54 - - [16/Feb/2013:16:40:26 +0600] "GET /pause/ajax'
            'Pause?pauseConfigId=&admin=0 HTTP/1.1" 200 1040 "http://callider'
            '/pause/index" "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1;'
            ' WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; '
            '.NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; '
            'InfoPath.3; .NET4.0C; .NET4.0E)" 16048',
            '192.168.12.61 - - [17/Feb/2013:07:47:37 +0600] "GET /pause/ajax'
            'Pause?pauseConfigId=&admin=0 HTTP/1.1" 200 985 "http://callider'

            '/pause/index" "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1;'
            ' Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET'
            ' CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; '
            '.NET4.0E)" 19841',
            '192.168.74.78 - - [17/Feb/2013:07:47:39 +0600] "GET /pause/ajax'
            'Pause?pauseConfigId=&admin=0 HTTP/1.1" 200 986 "http://callider'
            '/pause/index" "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1;'
            ' WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET '
            'CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; '
            'InfoPath.3; .NET4.0C; MS-RTC LM 8; .NET4.0E)" 26794'
        ]

        count = 0
        for i in merge(iterable_1, iterable_2, key=log_key):
            self.assertEqual(expected_result[count], i)
            count += 1


if __name__ == '__main__':
    unittest.main()
