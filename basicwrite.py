"""
Functions to create and edit a .desktop file.
"""
import re

class DesktopFile:
    # Regular expression to find a key line could probably be a lot
    # better, but should work for now.
    key_line = re.compile('\S+=\S+')
    def __init__(self, filename, from_usr=False):
        self.fileobj = open(filename, 'ra')
        self.entry_dict = {}
    def edit_key(self, key, value):
        self.entry_dict[key] = value
    def find_current_key(self, key):
        pass
    def populate_keys(self):
        for line in self.fileobj:
            if key_line.match(line):
                split_line = line.split('=')
                current_key = split_line[0]
                current_val = split_line[1]

