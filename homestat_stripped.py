#!/usr/bin/env python3


def make_stat(filename):
    male_exception_names = ('Илья', 'Никита', 'Лёва')
    female_exception_name = ('Любовь')
    tmp_year = 0
    statistics_for_boys = {}
    statistics_for_girls = {}

    with open(filename, 'r', encoding="cp1251") as file:
        for string in file:
            first_pointer_name = string.find('/>')
            second_pointer_name = string.find("</a>")

            full_name = ''

            if first_pointer_name != -1 and second_pointer_name != -1:
                full_name = string[first_pointer_name + 3:second_pointer_name]

            first_pointer_year = string.find("<h3>")
            second_pointer_year = string.find("</h3>")

            year = ''

            if first_pointer_year != -1 and second_pointer_year != -1:
                year = string[first_pointer_year + 4:second_pointer_year]

            if year != '':
                tmp_year = year

            if full_name != '':
                name = full_name.split()[1]
                if name[-1] == 'а' or name[-1] == 'я' or (
                        name in female_exception_name):
                    if name in male_exception_names:
                        if tmp_year in statistics_for_boys.keys():
                            if name in statistics_for_boys[tmp_year].keys():
                                statistics_for_boys[tmp_year][name] += 1
                            else:
                                statistics_for_boys[tmp_year][name] = 1
                        else:
                            statistics_for_boys[tmp_year] = {name: 1}

                    else:
                        if tmp_year in statistics_for_girls.keys():
                            if name in statistics_for_girls[tmp_year].keys():
                                statistics_for_girls[tmp_year][name] += 1
                            else:
                                statistics_for_girls[tmp_year][name] = 1
                        else:
                            statistics_for_girls[tmp_year] = {name: 1}

                else:
                    if tmp_year in statistics_for_boys.keys():
                        if name in statistics_for_boys[tmp_year].keys():
                            statistics_for_boys[tmp_year][name] += 1
                        else:
                            statistics_for_boys[tmp_year][name] = 1
                    else:
                        statistics_for_boys[tmp_year] = {name: 1}
        return {'statistics_for_girls': statistics_for_girls,
                'statistics_for_boys': statistics_for_boys}


def extract_years(stat):
    years = sorted(list(stat['statistics_for_girls'].keys()))
    return years


def extract_general(stat):
    answer = []
    statistics_for_girls = {}
    statistics_for_boys = {}

    girls_dict = stat['statistics_for_girls']
    boys_dict = stat['statistics_for_boys']

    for key in extract_years(stat):
        for i in girls_dict[key].keys():
            if i in statistics_for_girls.keys():
                statistics_for_girls[i] += girls_dict[key][i]
            else:
                statistics_for_girls[i] = girls_dict[key][i]

        for i in boys_dict[key].keys():
            if i in statistics_for_boys.keys():
                statistics_for_boys[i] += boys_dict[key][i]
            else:
                statistics_for_boys[i] = boys_dict[key][i]

    for key in statistics_for_girls:
        answer.append((key, statistics_for_girls[key]))

    for key in statistics_for_boys:
        answer.append((key, statistics_for_boys[key]))

    return sorted(answer, key=lambda x: x[1], reverse=True)


def extract_general_male(stat):
    answer = []
    statistics_for_boys = {}
    boys_dict = stat['statistics_for_boys']

    for key in extract_years(stat):
        for i in boys_dict[key].keys():
            if i in statistics_for_boys.keys():
                statistics_for_boys[i] += boys_dict[key][i]
            else:
                statistics_for_boys[i] = boys_dict[key][i]

    for key in statistics_for_boys:
        answer.append((key, statistics_for_boys[key]))

    return sorted(answer, key=lambda x: x[1], reverse=True)


def extract_general_female(stat):
    answer = []
    statistics_for_girls = {}
    girls_dict = stat['statistics_for_girls']

    for key in extract_years(stat):
        for i in girls_dict[key].keys():
            if i in statistics_for_girls.keys():
                statistics_for_girls[i] += girls_dict[key][i]
            else:
                statistics_for_girls[i] = girls_dict[key][i]

    for key in statistics_for_girls:
        answer.append((key, statistics_for_girls[key]))

    return sorted(answer, key=lambda x: x[1], reverse=True)


def extract_year(stat, year):
    answer = []
    statistics_for_girls = {}
    statistics_for_boys = {}

    girls_dict = stat['statistics_for_girls']
    boys_dict = stat['statistics_for_boys']

    for i in girls_dict[year].keys():
        if i in statistics_for_girls.keys():
            statistics_for_girls[i] += girls_dict[year][i]
        else:
            statistics_for_girls[i] = girls_dict[year][i]

    for i in boys_dict[year].keys():
        if i in statistics_for_boys.keys():
            statistics_for_boys[i] += boys_dict[year][i]
        else:
            statistics_for_boys[i] = boys_dict[year][i]

    for year in statistics_for_girls:
        answer.append((year, statistics_for_girls[year]))

    for year in statistics_for_boys:
        answer.append((year, statistics_for_boys[year]))

    return sorted(answer, key=lambda x: x[1], reverse=True)


def extract_year_male(stat, year):
    answer = []
    statistics_for_boys = {}
    boys_dict = stat['statistics_for_boys']

    for i in boys_dict[year].keys():
        if i in statistics_for_boys.keys():
            statistics_for_boys[i] += boys_dict[year][i]
        else:
            statistics_for_boys[i] = boys_dict[year][i]

    for year in statistics_for_boys:
        answer.append((year, statistics_for_boys[year]))

    return sorted(answer, key=lambda x: x[1], reverse=True)


def extract_year_female(stat, year):
    answer = []
    statistics_for_girls = {}
    girls_dict = stat['statistics_for_girls']

    for i in girls_dict[year].keys():
        if i in statistics_for_girls.keys():
            statistics_for_girls[i] += girls_dict[year][i]
        else:
            statistics_for_girls[i] = girls_dict[year][i]

    for year in statistics_for_girls:
        answer.append((year, statistics_for_girls[year]))

    return sorted(answer, key=lambda x: x[1], reverse=True)


if __name__ == 'main':
    pass
