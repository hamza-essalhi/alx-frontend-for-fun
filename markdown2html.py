#!/usr/bin/python3

"""
Markdown script using python.
"""
import sys
import os.path
import re
import hashlib

def process_heading(line):
    headings = line.lstrip('#')
    heading_num = len(line) - len(headings)
    if 1 <= heading_num <= 6:
        return '<h{0}>{1}</h{0}>\n'.format(heading_num, headings.strip())
    return line

def process_list(line, list_type, list_start, list_end):
    list_item = line.lstrip(list_type)
    list_num = len(line) - len(list_item)
    if not list_start:
        list_start = True
        return ('<{0}>\n<li>{1}</li>\n'.format(list_type, list_item), list_start)
    elif list_num:
        return ('<li>{}</li>\n'.format(list_item), list_start)
    else:
        return ('</{0}>\n'.format(list_type), False)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: ./markdown2html.py README.md README.html',
              file=sys.stderr)
        exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.isfile(input_file):
        print('Missing {}'.format(input_file), file=sys.stderr)
        exit(1)

    with open(input_file) as read:
        with open(output_file, 'w') as html:
            unordered_start, ordered_start, paragraph = False, False, False
            # bold syntax
            for line in read:
                line = line.replace('**', '<b>', 1)
                line = line.replace('**', '</b>', 1)
                line = line.replace('__', '<em>', 1)
                line = line.replace('__', '</em>', 1)

                # md5
                md5 = re.findall(r'\[\[.+?\]\]', line)
                md5_inside = re.findall(r'\[\[(.+?)\]\]', line)
                if md5:
                    line = line.replace(md5[0], hashlib.md5(
                        md5_inside[0].encode()).hexdigest())

                # remove the letter C
                remove_letter_c = re.findall(r'\(\(.+?\)\)', line)
                remove_c_more = re.findall(r'\(\((.+?)\)\)', line)
                if remove_letter_c:
                    remove_c_more = ''.join(
                        c for c in remove_c_more[0] if c not in 'Cc')
                    line = line.replace(remove_letter_c[0], remove_c_more)

                # process headings
                line = process_heading(line)

                # process unordered list
                if line.lstrip('-'):
                    line, unordered_start = process_list(line, 'ul', unordered_start, False)

                # process ordered list
                if line.lstrip('*'):
                    line, ordered_start = process_list(line, 'ol', ordered_start, False)

                # process paragraphs
                if not (line.startswith('#') or unordered_start or ordered_start):
                    if not paragraph and len(line) > 1:
                        line = '<p>\n' + line
                        paragraph = True
                    elif len(line) > 1:
                        line = '<br/>\n'
                    elif paragraph:
                        line = '</p>\n'
                        paragraph = False

                html.write(line)

            if unordered_start:
                html.write('</ul>\n')
            if ordered_start:
                html.write('</ol>\n')
            if paragraph:
                html.write('</p>\n')
    exit(0)
