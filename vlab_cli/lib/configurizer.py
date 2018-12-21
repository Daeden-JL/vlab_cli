# -*- coding: UTF-8 -*-
"""
This module is for reading/writing the vLab configuration file.

The vLab CLI uses a very basic INI format, and looks like::

    [SCP]
    agent=winscp
    location=C:\\some\\path\\WinSCP.exe

    [SSH]
    agent=putty
    location=C:\\some\\path\\putty.exe

    [BROWSER]
    agent=firefox
    location=C:\\some\\path\\firefox.exe

    [RDP]
    agent=mstsc
    location=C:\\some\\path\\mstsc.exe
"""
import os
import platform
import configparser


CONFIG_DIR = os.path.join(os.path.expanduser('~'), '.vlab')
CONFIG_FILE = os.path.join(CONFIG_DIR, 'config.ini')
CONFIG_SECTIONS = {'SSH', 'RDP', 'BROWSER', 'SCP'}

def _get_platform_progs():
    base = ['chrome', 'firefox']
    this_os = platform.system().lower()
    if this_os == 'windows':
        base += ['putty', 'mstsc', 'winscp']
    else:
        base += ['gnome-terminal', 'remmina', 'scp']
    return base

SUPPORTED_PROGS = _get_platform_progs()


def get_config():
    """Load vLab CLI config

    :Returns: configparser.ConfigParser or None
    """
    try:
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)
    except Exception:
        config = None
    return config


def set_config(info):
    """Save the configuration values to disk. Supplied info must be nested dictionary.

    :Returns: None

    :Raises: ValueError

    :param info: The mapping of sections and it's key/value configs
    :type info: Dictionary
    """
    sections = set(info.keys())
    if not CONFIG_SECTIONS == sections:
        error = 'vLab Config missing section(s): {}'.format(CONFIG_SECTIONS - sections)
        raise ValueError(error)

    config = configparser.ConfigParser()
    for section, values in info.items():
        config[section] = values
    with open(CONFIG_FILE, 'w') as the_file:
        config.write(the_file)


def find_programs():
    """Walk the filesystem to find the software needed for ``vlab connnect``

    :Returns: Dictionary
    """
    this_os = platform.system().lower()
    if this_os == 'windows':
        search_root = 'C:\\'
        support_programs = {'putty.exe', 'mstsc.exe', 'firefox.exe', 'chrome.exe', 'winscp.exe'}
    else:
        search_root = '/'
        support_programs = {'gnome-terminal', 'remmina', 'firefox', 'chrome', 'scp'}

    found_programs = {}
    for root, dirs, files in os.walk(search_root):
        for the_file in files:
            if the_file.lower() in support_programs:
                agent = os.path.splitext(the_file)[0] # remove file extension
                location = os.path.join(root, the_file)
                found_programs[agent] = location
    return found_programs
