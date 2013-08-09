#!/usr/bin/env python

"""
portell: tell on ports when a connection is made to them

Uses https://github.com/alloy/terminal-notifier for
notifications in OSX 10.8

@author: mitzip
@contact: http://github.com/mitzip/portell
@license: Public Domain
@version: 1.0.0
"""

from subprocess import call, check_output
from time import sleep
from os import getpid
from os.path import expanduser
from distutils.spawn import find_executable
import logging

logger = logging.getLogger()
hdlr = logging.FileHandler('portell.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.WARNING)

# Set of (protocol, local port) tuples.
watched = {('tcp4', 5900)}
sleep_time = 5  # sleep time between checks in seconds
applications = ''.join([expanduser('~'), '/Applications'])
notifier = '/terminal-notifier.app/Contents/MacOS/terminal-notifier'

while True:
    # Check if any of the watched services is running.
    netstat = check_output(
        [find_executable('netstat'), '-p', 'tcp', '-n'],
        universal_newlines=True).split('\n')

    for line in netstat[2:-1]:
        items = line.split()
        proto = items[0]
        port = int(items[3].split('.')[-1])
        if (proto, port) in watched:
            logger.warning(line)
            # found = "Found {} connection from {} to port {}"
            #   .format(proto, items[4], port)
            found = "You've got mail!"
            call(
                [''.join([applications, notifier]),
                 '-execute', ''.join(["kill -9 ", str(getpid())]),
                 '-message', found])
    sleep(sleep_time)
