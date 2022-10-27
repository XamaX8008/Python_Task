import sys
import re
from urllib import request, parse, error


def get_content(name):
    try:
        link = 'https://ru.wikipedia.org/wiki/' + parse.quote(name)
        page = request.urlopen(link)
        result = page.read().decode(
            page.headers.get_content_charset()).replace('\n', '')
        return result
    except error.HTTPError:
        return None
    except error.URLError:
        return None


def extract_content(page):
    if page is None:
        return (0, 0)

    result = \
        re.search(
            r'<div id="content" class="mw-body" role="main">(.*)</div><div '
            r'id="mw-navigation">',
            page)

    if result is not None:
        return result.start(), result.end()
    else:
        return (0, 0)


def extract_links(page, begin, end):
    links = re.findall(
        r'[Hh][Rr][Ee][Ff]=[\"\']/[Ww][Ii][Kk][Ii]/([\w%\(\)\_\,]*)[\"\']',
        page[begin:end])
    result = []

    for i in links:
        i = parse.unquote(i)
        if i is not None and i not in result:
            result.append(i)

    return result


def get_way(jump_table, finish):
    jump_list = [finish]
    tmp_site = finish

    while tmp_site in jump_table.keys():
        tmp_site = jump_table[tmp_site]
        jump_list.insert(0, tmp_site)

    return jump_list


def find_chain(start, finish):
    if start == finish:
        return [start]

    start = start.replace(' ', '_')
    finish = finish.replace(' ', '_')

    used_links = [start]
    jump_table = {}
    queue = [start]

    while queue:
        link = queue.pop(0)
        content = get_content(link)

        if content is None:
            continue

        start, end = extract_content(content)
        links = extract_links(content, start, end)

        for i in links:
            if i not in used_links:
                queue.append(i)
                jump_table[i] = link
                used_links.append(i)
            if i == finish:
                return get_way(jump_table, finish)


def main():
    args = sys.argv
    if len(args) == 3:
        start = args[1]
        end = args[2]
        chain = find_chain(start, end)
        if chain is not None:
            print(chain)
    else:
        return None


if __name__ == '__main__':
    main()
