import difflib
import email

from bs4 import BeautifulSoup


FILES = ('det_01.txt', 'det_02.txt', 'det_03.txt')


def load_mail_from_file(fname):
    with open(fname, 'rb') as fp:
        msg = email.message_from_string(fp.read())
    return msg


def get_html_from_mail(msg):
    for part in msg.walk():
        pass
    html = part.get_payload(decode=True)
    soup = BeautifulSoup(html, 'html.parser')
    return soup.prettify()


def get_diff(a, b):
    lines_a = a.splitlines(1)
    lines_b = b.splitlines(1)

    d = difflib.Differ()
    lines = list(d.compare(lines_a, lines_b))

    result = []
    changes_a = []
    changes_b = []

    for line in lines:
        if line.startswith('- '):
            if changes_b:
                result.append((changes_a, changes_b))
                changes_a = []
                changes_b = []
            changes_a.append(line[2:])
        elif line.startswith('+ '):
            changes_b.append(line[2:])

    return result


def create_template(a, b):
    template = a
    replaces = get_diff(a, b)

    for block_a, block_b in replaces:
        print "--------------------"
        print 'a >> {}'.format(block_a)
        print 'a >> {}'.format(block_b)
        print "--------------------"
        field_name = raw_input('Field name? (Enter or XXX to ignore): ')
        print "--------------------"
        print

        if not field_name:
            field_name = 'XXX'
        field_tag = '[[' + field_name + ']]\n'

        template = template.replace(''.join(block_a), field_tag)

    return template


def extract_fields(template, content):
    diff = get_diff(template, content)

    results = {}
    for keys, values in diff:
        for i in range(len(keys)):
            key = keys[i]
            if key.startswith('[['):
                key = key[2:-3]
                if key != 'XXX':
                    val = values[i]
                    val = val.strip()
                    results[key] = val
    return results


def print_report(data):
    for fname, fields in data.items():
        print '------------------------------'
        print fname
        print '------------------------------'
        for k, v in fields.items():
            print ' - {}: {}'.format(k.encode('utf-8'), v.encode('utf-8'))
        print '------------------------------'
        print


def main():
    # Extract html from mails
    msg1 = load_mail_from_file('mail_01.txt')
    msg2 = load_mail_from_file('mail_02.txt')
    msg3 = load_mail_from_file('mail_03.txt')

    html1 = get_html_from_mail(msg1)
    html2 = get_html_from_mail(msg2)
    html3 = get_html_from_mail(msg3)

    # First step: Extract the template and ask for variable names
    template = create_template(html1, html2)

    # Second step: extract data from all mails
    results = {
        'mail_01.txt': extract_fields(template, html1),
        'mail_02.txt': extract_fields(template, html2),
        'mail_03.txt': extract_fields(template, html3),
    }

    print_report(results)


if __name__ == '__main__':
    main()
