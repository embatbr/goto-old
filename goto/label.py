# coding: utf-8


"""Implementation of command 'label'."""


import sys
import os
import re
import locale
import argparse

from storage import Storage, LabelAlreadyExistsError, LabelTooLongError, LabelInvalidFormatError, LABEL_SIZE


storage = Storage()
language, encoding = locale.getdefaultlocale()


def delete(label):
    try:
        storage.remove(label)
        print '%s label was deleted.' % label
    except:
        sys.stderr.write('%s is not a valid label.\n' % label)
        sys.exit(1)


def replace(label, path):
    try:
        storage.replace(label, path)
        print '%s label now points to %s.' % (label, path)
    except LabelTooLongError:
        sys.stderr.write('%s is too long. The size limit is %d characters.\n'
                                                        % (label, LABEL_SIZE))
    except LabelInvalidFormatError:
        sys.stderr.write('%s is not a valid label.\n' % label)

    sys.exit(1)


def add(label, path):
    try:
        storage.add(label, path)
        print '%s label points to %s.' % (label, path)
    except LabelAlreadyExistsError:
        sys.stderr.write('%s label already exists. Use --replace.\n' % label)
        sys.exit(1)
    except LabelTooLongError:
        sys.stderr.write('%s is too long. The size limit is %d characters.\n'
                                                        % (label, LABEL_SIZE))
    except LabelInvalidFormatError:
        sys.stderr.write('%s is not a valid label.\n' % label)

    sys.exit(1)


def main():
    """Entrypoint for the `label` utility."""
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.set_defaults(mode='insert')
    group.add_argument('-d', '--delete', action='store_const', dest='mode',
                            const='delete', help='delete an existing label')
    group.add_argument('-r', '--replace', action='store_const', dest='mode',
                            const='replace', help='replace an existing label')
    parser.add_argument('label', nargs='?', help='name of the label')
    parser.add_argument('target', nargs='?', help='path to the label targets')

    args = parser.parse_args()
    storage.open_or_create()

    if not args.label and args.mode in ['delete', 'replace']:
        parser.error('can\'t %s without specify a label.' % args.mode)

    curr_dir = args.target
    if curr_dir is None:
        curr_dir = unicode(os.getcwd(), encoding)
    if args.label:
        args.label = unicode(args.label, encoding)

    if args.mode == 'delete':
        delete(args.label)
    elif args.mode == 'replace':
        replace(args.label, curr_dir)
    else:
        if not args.label:
            args.label = curr_dir[curr_dir.rfind('/')+1:]
            args.label = re.sub(r'\s+', '_', args.label, flags=re.UNICODE)

        add(args.label, curr_dir)
