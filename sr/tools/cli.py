from __future__ import print_function

import argparse
import os
import sys
import subprocess

from sr.tools import __path__


def get_commands_directory():
    """Return the directory at which commands will be found."""
    return os.path.join(__path__[0], "cmds")


def find_commands(filter_private=False, commands_dir=None):
    """
    Recursively find commands and return a dictionary mapping name to full file
    path.
    """
    if commands_dir is None:
        commands_dir = get_commands_directory()

    cmds = {}
    for d in os.listdir(commands_dir):
        if d in [".git"]:
            continue

        path = os.path.join(commands_dir, d)

        if os.path.isdir(path):
            # Go through the files in this subdir
            for f in os.listdir(path):
                if f == "sr":
                    continue

                fp = os.path.join(path, f)

                if os.path.isfile(fp) and os.access(fp, os.X_OK):
                    if filter_private and (f[0] == "_" or f[-1] == "~"):
                        continue

                    cmds[f] = fp

    return cmds


def main():
    commands = find_commands(filter_private=True)

    parser = argparse.ArgumentParser(description='Student Robotics tools')
    parser.add_argument('command', choices=sorted(commands.keys()),
                        help='command to invoke')
    parser.add_argument('args', nargs='*',
                        help='arguments to pass to the command')
    args = parser.parse_args()

    cmdline = [args.command] + args.args
    if os.name == 'nt':
        # this is hacky, and will be replaced with modules
        subprocess.call(["python", commands[args.command]] + cmdline[2:])
    else:
        os.execv(commands[args.command], cmdline)
