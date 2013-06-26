#!python
from subprocess import call, check_output
from time import sleep
from os import getpid

# Set of (protocol, local port) tuples.
watched = {('tcp4', 5900)}
sleep_time = 5  # sleep time between checks in seconds
applications = '/Users/davidmitchel/Applications'
notifier = '/terminal-notifier.app/Contents/MacOS/terminal-notifier'

while True:
    # Check if any of the watched services is running.
    netstat = check_output(
        ['/usr/sbin/netstat', '-p', 'tcp', '-n'],
        universal_newlines=True).split('\n')

    for line in netstat[2:-1]:
        items = line.split()
        proto = items[0]
        port = int(items[3].split('.')[-1])
        if (proto, port) in watched:
            # found = "Found {} connection from {} to port {}"
            #   .format(proto, items[4], port)
            found = "You've got mail!"
            call(
                [''.join([applications, notifier]),
                 '-execute', ''.join(["kill -9 ", str(getpid())]),
                 '-message', found])
    sleep(sleep_time)
