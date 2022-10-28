import re
import sys


def file_open(name):
    file = open(name, 'r', encoding="cp1251", errors="ignore")
    return file


def most_popular_resource(name):
    file = file_open(name)
    stat = {}

    while True:
        line = file.readline()

        if not line:
            break

        resource = re.findall(r'\, (/.*?)\,', line)

        if resource[0] in stat.keys():
            stat[resource[0]] += 1
        else:
            stat[resource[0]] = 1

    number_most_popular_resource = max(stat.values())

    for key, value in stat.items():
        if value == number_most_popular_resource:
            file.close()
            return key


print(most_popular_resource("W3SVC6.log"))
def most_active_client(name):
    file = file_open(name)
    stat = {}

    while True:
        line = file.readline()

        if not line:
            break

        resource = re.findall(r'^(\d*?\.\d*?\.\d*?\.\d*?),', line)

        if resource[0] in stat.keys():
            stat[resource[0]] += 1
        else:
            stat[resource[0]] = 1

    number_most_popular_resource = max(stat.values())

    for key, value in stat.items():
        if value == number_most_popular_resource:
            file.close()
            return key

print(most_active_client("W3SVC6.log"))

def main():
    args = sys.argv


if __name__ == '__main__':
    main()
