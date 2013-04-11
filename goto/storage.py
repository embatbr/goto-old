# coding: utf-8
import os
import re
import codecs
from configparser import UnicodeConfigParser, NoOptionError


HOME_DIR = os.path.expanduser("~")
STORAGE_DIR = '%s/.goto' % HOME_DIR
LABEL_STORAGE_FILE = 'labels'
LABEL_STORAGE_PATH = os.path.join(STORAGE_DIR, LABEL_STORAGE_FILE)
LABELS_SECTION = u'labels'
STACK_STORAGE_FILE = 'stack'
STACK_STORAGE_PATH = os.path.join(STORAGE_DIR, STACK_STORAGE_FILE)
STACK_SECTION = u'stack'

LABEL_SIZE = 32

LABEL_RE = re.compile(r'^[^\s/]+$', re.UNICODE)


class Storage(object):
    def __init__(self, goto_dir=STORAGE_DIR, label_filename=LABEL_STORAGE_PATH,
        labels_section=LABELS_SECTION, stack_filename=STACK_STORAGE_PATH,
        stack_section=STACK_SECTION):
        """__init__"""
        self.goto_dir = goto_dir
        self.parser = UnicodeConfigParser()
        self.label_filename = label_filename
        self.labels_section = labels_section
        self.stack_filename = stack_filename
        self.stack_section = stack_section


    ########## FILE MANIPULATION ##########

    def _persist(self, filename):
        """Refreshs the file with the last changes."""
        if not os.path.exists(self.goto_dir):
            os.makedirs(self.goto_dir)
        with codecs.open(filename, 'w', encoding='utf-8') as f:
            self.parser.write(f)


    def _create(self, filename, section):
        """
        Creates the label file and put a default session where the labels will
        be stored.
        """
        self.parser.add_section(section)
        self._persist(filename)


    def open(self, filename):
        """Loads the parser with data from the label file."""
        with codecs.open(filename, 'r', encoding='utf-8') as f:
            self.parser.readfp(f)


    def open_or_create(self):
        """
        Tries to open label and stack files, if an error occurs, create the file.
        """
        # label file
        try:
            self.open(self.label_filename)
        except IOError:
            self._create(self.label_filename, self.labels_section)
            self.open(self.label_filename)

        # stack file
        # try:
        #     self.open(self.stack_filename)
        # except IOError:
        #     self._create(self.stack_filename, self.stack_section)
        #     self.open(self.stack_filename)


    ########## LABEL MANIPULATION ##########

    def get(self, label):
        """Returns the path of a label."""
        return self.parser.get(self.labels_section, label)


    def get_all(self):
        """Returns a dictionary with all labels and paths."""
        return {
            label:path for label, path
                in self.parser.items(self.labels_section)
        }


    def replace(self, label, path):
        """
        Replaces the path from a label. The label is created if it not exists.
        """
        if len(label) > LABEL_SIZE:
            raise LabelTooLongError()

        if not LABEL_RE.match(label):
            raise LabelInvalidFormatError()

        self.parser.set(self.labels_section, label, path)
        self._persist(self.label_filename)


    def add(self, label, path):
        """
        Adds a label-path entry in the label file. If the label exists, an
        Exception is raised.
        """
        if self.parser.has_option(self.labels_section, label):
            raise LabelAlreadyExistsError()

        self.replace(label, path)


    def remove(self, label):
        """Removes a label and it's path."""
        self.parser.remove_option(self.labels_section, label)
        self._persist(self.label_filename)


    ########## STACK MANIPULATION ##########

    def push(self, label):
        print 'PUSHED label', label

    def pop(self, ntimes=1):
        pass


class LabelAlreadyExistsError(Exception):
    pass

class LabelTooLongError(Exception):
    pass

class LabelInvalidFormatError(Exception):
    pass
