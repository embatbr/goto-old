# coding: utf-8


"""Implementation of command 'label'."""


import sys
import os
import locale
import argparse
import subprocess

from storage import Storage, NoOptionError


storage = Storage()
language, encoding = locale.getdefaultlocale()


def list_target_content(label):
    try:
        target = storage.get(label)
        subprocess.call('ls %s' % target, shell=True)
    except NoOptionError:
        sys.stderr.write('%s is not a valid label.\n' % label)
        sys.exit(1)


def main():
    """Entrypoint for the `list` utility."""
    parser = argparse.ArgumentParser()
    parser.add_argument('label', nargs='?', help='name of the label')

    args = parser.parse_args()
    storage.open_or_create()

    if not args.label:
        parser.error('can\'t list without specify a label.')

    args.label = unicode(args.label, encoding)
    list_target_content(args.label)