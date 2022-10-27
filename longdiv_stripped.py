#!/usr/bin/env python3


def long_division(dividend, divider):
    '''
    Вернуть строку с процедурой деления «уголком» чисел dividend и divider.
    Формат вывода приведён на примерах ниже.
    '''

    answer = str(dividend) + "|" + str(divider) + "\n"
    result = str(dividend // divider)

    if result == "0":
        answer += str(dividend) + "|0"
        return answer

    subtracted_number = str(int(result[0]) * divider)
    margins = 0

    if int(str(dividend)[:len(subtracted_number)]) \
            - int(subtracted_number) < 0:
        margins += 1

    tmp_dividend = str(dividend)[:len(subtracted_number) + margins]
    answer += subtracted_number + " " * (
            len(str(dividend)) - len(subtracted_number)) + f"|{result}\n"
    remainder_of_division = str(int(tmp_dividend) - int(subtracted_number))

    if remainder_of_division == '0':
        remainder_of_division = ''

    margins += len(subtracted_number) - len(remainder_of_division)

    i = 1
    flag = False

    while i < len(result):
        if not flag:
            if remainder_of_division == "0":
                remainder_of_division = ""

            if result[i] != "0":
                subtracted_number = str(int(result[i]) * divider)
            else:
                remainder_of_division += str(dividend)[
                    len(remainder_of_division) + margins]
                i += 1
                continue

            tmp_dividend = remainder_of_division + str(dividend)[
                len(remainder_of_division) + margins]
            answer += margins * " " + tmp_dividend + "\n"
            flag = True
        else:
            if int(tmp_dividend[:len(subtracted_number)]) - int(
                    subtracted_number) < 0:
                margins += 1
            i -= 1
            answer += margins * " " + subtracted_number + "\n"
            remainder_of_division = str(
                int(tmp_dividend) - int(subtracted_number))
            flag = False
            count = 0
            margins += 1
            while len(subtracted_number) - len(
                    remainder_of_division) - count > 1:
                count += 1
                margins += 1
        i += 1

    if int(tmp_dividend[:len(subtracted_number)]) - int(subtracted_number) < 0:
        margins += 1

    if flag:
        answer += margins * " " + subtracted_number + "\n"
        count = 0

        while len(subtracted_number) - len(remainder_of_division) - count > 1:
            count += 1
            margins += 1

    remainder_of_division = str(dividend % divider)

    if remainder_of_division != "0":
        answer += (len(str(dividend)) - len(
            remainder_of_division)) * " " + remainder_of_division
    else:
        count = 0
        for i in reversed(str(dividend)):
            if i != "0":
                break
            count += 1

        counter = 0
        for i in reversed(subtracted_number):
            if i != "0":
                break
            counter += 1

        answer += (len(str(dividend)) - len(
            remainder_of_division) - count + counter) \
            * " " + remainder_of_division

    return answer


def main():
    # print(long_division(130, 24))
    # print()
    # print(long_division(1, 1))
    # print()
    # print(long_division(15, 3))
    # print()
    # print(long_division(3, 15))
    # print()
    # print(long_division(12345, 25))
    # print()
    # print(long_division(1234, 1423))
    # print()
    # print(long_division(87654532, 1))
    # print()
    # print(long_division(24600, 123))
    # print()
    # print(long_division(4567, 1234567))
    # print()
    print(long_division(246001, 123))
    # print()
    # print(long_division(100000, 50))
    # print()
    # print(long_division(47828649, 467))
    # print()
    # print(long_division(425934261694251, 12345678))


if __name__ == '__main__':
    main()
