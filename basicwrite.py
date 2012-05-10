"""
Functions to create and edit a .desktop file.
"""
import re
import tempfile

class DesktopFile:
    """
    Creates and stores the key/value pairs necessary for a desktop entry
    """
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
        self.quicklist = {}
        self.has_quicklist = False
    def check_keys(self):
        for key in self.entry_dict:
            if not key in self.valid_keys:
                print(key + ' is not a valid key type!')
    def write_desk_file(self, out_filename):
        """ 
        Takes the key/value pairs in entry_dict and writes a new desktop file
        to out_filename
        """
        # This is the order of keys on the freedesktop.org example, seems like
        # a good standard to stick to for now
        order = ['Version', 'Type', 'Name', 'Comment', 
                'TryExec', 'Exec', 'Icon', 'MimeType'
                 ]
        out_filename = self.output_dir + out_filename
        self.out_file = open(out_filename, 'w')
        self.out_file.write('[Desktop Entry]' + '\n')
        for key in order:
            if self.entry_dict.get(key):
                self.out_file.write(key + '=' + self.entry_dict[key] + '\n')
            else:
                # Check for the most essential keys here, e.g. Name, Exec
                pass
        if self.has_quicklist:
            self.write_quicklist()
    def add_quicklist_action(self, action, name, command):
        if not self.has_quicklist:
            self.has_quicklist = True
        self.quicklist[action] = {'Name': name, 'Exec': command}
    def write_quicklist(self):
        self.out_file.write('Actions=')
        for action in self.quicklist:
            self.out_file.write(action + ';')
        self.out_file.write('\n\n')
        for action in self.quicklist:
            self.out_file.write('[Desktop Action ' + action + ']\n')
            self.write_quick_action(self.quicklist[action])
    def write_quick_action(self, action):
        for key in action:
            self.out_file.write(key + '=' + action[key] + '\n')
        self.out_file.write('OnlyShowIn=Unity;')
        self.out_file.write('\n')



class ExistingDesktop(DesktopFile):
    """
    Subclass of DesktopFile to be used when you're copying/editing an existing
    desktop entry
    """
    def __init__(self, filename):
        DesktopFile.__init__(self)
        self.old = open(filename)
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
    des = ExistingDesktop('desuratest.desktop')
    des.add_quicklist_action('Force', 'Force the client to update', 'desura --force')
    print(des.entry_dict)
    des.write_desk_file('desuranew.desktop')
