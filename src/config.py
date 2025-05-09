"""
DEPRECATED
"""

import configparser

def get_enabled_state():
    config = configparser.ConfigParser()
    config.read('config/config.ini')
    return config.getboolean('Settings', 'enabled')

def get_version():
    config = configparser.ConfigParser()
    config.read('config/config.ini')
    return config.get('Settings', 'version')

def get_timeout():
    config = configparser.ConfigParser()
    config.read('config/config.ini')
    return config.getint('Settings', 'timeout')

def change_enabled_state(state: bool):
    config = configparser.ConfigParser()
    config.read('config/config.ini')
    config.set('Settings', 'enabled', str(state))
    with open('config/config.ini', 'w') as configfile:
        config.write(configfile)