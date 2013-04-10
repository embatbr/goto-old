# coding: utf-8


"""Implementation of command 'goto'."""


import os
import sys
import locale
import argparse
import subprocess

from storage import Storage, NoOptionError, LABEL_SIZE


storage = Storage()
language, encoding = locale.getdefaultlocale()


def format_label(label):
    return label + (LABEL_SIZE - len(label)) * u' '


def list_labels():
    labels = storage.get_all()
    for label, path in labels.iteritems():
        s = u'%s  %s' % (format_label(label), path)
        print s.encode(encoding)


def list_target_content(label):
    try:
        target = storage.get(label)
        subprocess.call('ls %s' % target, shell=True)
    except NoOptionError:
        sys.stderr.write('%s is not a valid label.\n' % label)
        sys.exit(1)


def change_directory(label):
    try:
        path = storage.get(label)
        if not os.path.isdir(path):
            raise DanglingLabelError()
        print '<PATH>'
        print path.encode(encoding)
    except NoOptionError:
        sys.stderr.write('%s is not a valid label.\n' % label)
        sys.exit(1)
    except DanglingLabelError:
        storage.remove(label)
        sys.stderr.write('%s is not a valid path. label %s was removed.\n' %
            (path, label))
        sys.exit(1)


def main():
    """Entrypoint for the `goto` utility."""
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.set_defaults(mode='')
    group.add_argument('-l', '--list', action='store_const', dest='mode',
                            const='list', help='list the target of a label')
    parser.add_argument('label', nargs='?', help='name of the label')
    args = parser.parse_args()

    if not args.label and args.mode in ['list']:
        parser.error('can\'t %s without specify a label.' % args.mode)

    storage.open_or_create()

    if args.mode == 'list':
        list_target_content(args.label)
    elif args.label:
        label = unicode(args.label, encoding)
        change_directory(label)
    else:
        list_labels()


class DanglingLabelError(Exception):
    pass
