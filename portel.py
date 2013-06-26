#!python
import subprocess
from time import sleep

# Set of (protocol, local port) tuples.
watched = {('tcp4', 5900)}
sleep_time = 5  # sleep time between checks in seconds

while True:
    """ Check if any of the watched services is running. """
    netstat = subprocess.check_output(
        ['/usr/sbin/netstat', '-p', 'tcp', '-n'],
        universal_newlines=True).split('\n')

    for line in netstat[2:-1]:
        items = line.split()
        proto = items[0]
        port = int(items[3].split('.')[4])
        if (proto, port) in watched:
            # found = "Found {} connection from {} to port {}".format(proto, items[4], port)
            found = "You've got mail!"
            subprocess.call(['/Users/davidmitchel/Applications/terminal-notifier.app/Contents/MacOS/terminal-notifier', '-message', found])
    sleep(sleep_time)
