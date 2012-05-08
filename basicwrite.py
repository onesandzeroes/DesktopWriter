"""
Functions to create and edit a .desktop file.
"""
import re
import tempfile

class DesktopFile:
    # Regular expression to find a key line could probably be a lot
    # better, but should work for now.
    key_line = re.compile('\S+=\S+')
    # You can only define one of 'OnlyShowIn' or 'NotShowIn', write
    # some checks for this
    valid_keys = ['Type', 'Version', 'Name', 'GenericName', 'NoDisplay',
                  'Comment', 'Icon', 'Hidden', 'OnlyShowIn', 'TryExec',
                  'Exec', 'Path', 'Terminal', 'Actions', 'MimeType',
                  'Categories', 'Keywords', 'StartupNotify' 'StartupNotify',
                  'StartupWMClass', 'URL']
    def __init__(self, filename):
        self.old = open(filename, 'r')
        self.entry_dict = {}
        self.populate_keys()
    def edit_key(self, key, value):
        if not key in self.valid_keys:
            print('Not a valid key type!')
        self.entry_dict[key] = value
    def find_current_key(self, key):
        pass
    def populate_keys(self):
        # List comprehension to find all lines containing a key=value pair
        key_lines = [line for line in self.old if self.key_line.match(line)]
        for line in key_lines:
            split_line = line.split('=')
            current_key = split_line[0]
            current_val = split_line[1].rstrip()
            self.entry_dict[current_key] = current_val

if __name__ == '__main__':
    des = DesktopFile('desuratest.desktop')
    print(des.entry_dict)
