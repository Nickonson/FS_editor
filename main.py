import os

import winreg as wrg
import argparse
import shutil


parser = argparse.ArgumentParser()


# Mode Options

modeGroup = parser.add_mutually_exclusive_group()

modeGroup.required = True

modeGroup.add_argument('-f', '--filesystem',
                       help='File Management Mode', action="store_true")

modeGroup.add_argument('-r', '--registry',
                       help='Windows Registry Management Mode', action="store_true")


parser.add_argument("path", help="path to the file or registry key to manage")


# Action Options
actionGroup = parser.add_argument_group('Actions')
actionGroup.add_argument(
    '-c', '--copy', help='copy file to another destination')
actionGroup.add_argument(
    '-w', '--write', help='write file contents')
actionGroup.add_argument(
    '-R', '--Rename', help='rename file to specified name')

actionGroup.add_argument(
    '-p', '--print', help='print file contents', action="store_true")
actionGroup.add_argument(
    '-t', '--touch', help='create file or registry key', action="store_true")
actionGroup.add_argument(
    '-d', '--delete', help='remove file or registry key', action="store_true")

args = parser.parse_args()

# Program Begin
if args.filesystem:

    if args.copy:

        print('Copying file ' + args.copy + ' to ' + args.path)

        shutil.copy2(args.copy, args.path)

    elif args.write:

        print('Writing "' + args.write + '" to ' + args.path)

        with open(args.path, mode='w') as file:

            n = file.write(args.write)

            print('Written', n, 'symbols')

    elif args.print:

        print('Printing contents of file ' + args.path + ':')

        with open(args.path, 'r') as file:
            print(file.read())

    elif args.Rename:

        print('Renaming file ' + args.Rename + ' to ' + args.path)

        shutil.move(args.Rename, args.path,)

    elif args.touch:

        file = open(args.path, 'a+')
        file.close()

    elif args.delete:

        os.remove(args.path)

elif args.registry:
    location = wrg.HKEY_CURRENT_USER
    soft = wrg.OpenKeyEx(location, r"SOFTWARE\\")

    if args.touch:

        key = wrg.CreateKey(soft, args.path)
        if key:
            wrg.CloseKey(key)


    elif args.delete:

        with wrg.OpenKeyEx(soft, args.path, access=wrg.KEY_WRITE) as key:
            wrg.DeleteKey(soft, args.path)


    elif args.write:
        with wrg.OpenKeyEx(soft, args.path, access=wrg.KEY_SET_VALUE) as key:
            wrg.SetValue(key, args.path, wrg.REG_SZ, args.write)


    else:
        print('Selected options are not compatible with registry operations')


    if soft:
        soft.Close()
else:
    print("Wrong mode has chosen\n")