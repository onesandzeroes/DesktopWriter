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
                  'StartupWMClass', 'URL'
                  ]
    # Set the output directory to ./Output/ for now, change it to .local/share
    # /applications later
    output_dir = 'Output/'
    def __init__(self):
        self.entry_dict = {}
    def edit_key(self, key, value):
        if not key in self.valid_keys:
            print('Not a valid key type!')
        self.entry_dict[key] = value
    def find_current_key(self, key):
        pass
    def write_desk_file(self, out_filename):
        # This is the order of keys on the freedesktop.org example, seems like
        # a good standard to stick to for now
        order = ['Version', 'Type', 'Name', 'Comment', 'TryExec', 'Exec', 'Icon',
                 'MimeType', 'Actions'
                 ]
        out_filename = self.output_dir + out_filename
        out_file = open(out_filename, 'w')
        out_file.write('[Desktop Entry]' + '\n')
        for key in order:
            if self.entry_dict.get(key):
                out_file.write(key + '=' + self.entry_dict[key] + '\n')
            else:
                # Check for the most essential keys here, e.g. Name, Exec
                pass

class ExistingDesktop(DesktopFile):
    def __init__(self, filename):
        self.entry_dict = {}
        self.populate_keys()
    def populate_keys(self):
        """
        Add all the existing key/value pairs to the entry_dict
        """
        # List comprehension to find all lines containing a key=value pair
        key_lines = [line for line in self.old if self.key_line.match(line)]
        for line in key_lines:
            split_line = line.split('=')
            current_key = split_line[0]
            current_val = split_line[1].rstrip()
            self.entry_dict[current_key] = current_val

if __name__ == '__main__':
    des = DesktopFile('desuratest.desktop', from_old=True)
    print(des.entry_dict)
