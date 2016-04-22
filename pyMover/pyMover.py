# -*- coding: utf8 -*-
import shutil
import glob
import os
import time

destinations = dict()
to_be_deleted = []
src = []
file_counter = 0
folder_counter = 0
verbose_mode = False
sep = os.sep


# Reads the resource file, and initializes the scripts file types,
# destinations and the files which needs to be deleted.
def init_script(res_file):
    with open(res_file, 'r') as res:
        resources = res.readlines()
        res.close()
    for i in resources:
        if i.startswith('#'):
            continue
        elif i.startswith('.'):
            x = i.split()
            destinations[x[0]] = x[1].replace('/', sep)
        elif i.startswith('d'):
            to_be_deleted.append(i)
        else:
            if i.__contains__('\n'):
                i = i.replace('\n', '')
            src.append(i)


# Finds the specified files, and calls the move_file() method.
def lookup_files():
    for path in src:
        if verbose_mode:
            print('looking up the files in', path)
        for file in glob.iglob(path + sep + '*.*', recursive=True):
            if verbose_mode:
                print('found', file)
            pre, ext = os.path.splitext(file)
            if ext in to_be_deleted:
                os.remove(file)
            # Makes sure that system files isn't moved
            elif pre.startswith('.'):
                continue
            else:
                if ext in destinations.keys():
                    move_file(file, destinations[ext])
                else:
                    move_file(file, destinations['.*'])


# Moves the files to their destination,
# specified in the resource file.
def move_file(source, dst):
    # Creates the dst path, if it doesn't exist.
    if not os.path.exists(dst):
        os.makedirs(dst)
    # Copies the file to the destination,
    # and removes it from the source,
    # to avoid duplicates, and leftovers.
    shutil.copy(source, dst)
    os.remove(source)
    if verbose_mode:
        print('moved', source, 'to', dst)
    global file_counter
    file_counter += 1


# Moves folders to a default destination,
# specified in the resource file.
def move_dirs():
    global folder_counter
    for path in src:
        # Moves the files inside the folders to
        # specified default directory.
        for directory in os.listdir(path):
            if not directory.startswith('.'):
                folder_counter += 1
                if verbose_mode:
                    print('found', directory)
                shutil.copytree(path + directory,
                                destinations['.folder'] + directory)
                shutil.rmtree(path + directory)


# Runs the script.
def run(arg='/Users/thomaslemqvist/PycharmProjects/3.5 scripts/PyMover/instruction_set.txt'):
    source = arg
    if len(arg) > 2:
        if str(arg[2]).lower() == '-v':
            global verbose_mode
            verbose_mode = True
    start = time.time()
    init_script(source)
    lookup_files()
    move_dirs()
    end = time.time()
    elapsed = end - start
    message = ''
    if (file_counter == 1):
        message = message + str(file_counter) + ' file '
    else:
        message = message + str(file_counter) + ' files '
    message = message + 'was moved and '
    if folder_counter == 1:
        message = message + str(folder_counter) + ' folder '
    else:
        message = message + str(folder_counter) + ' folders '
    message = message + 'was moved\n' + str(elapsed) + ' sec. elapsed'
    print(message)
    return message


# run()
