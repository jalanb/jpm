"""Handle the mpd_service for jpm"""


import os
import sys
import commands


try:
    from sh import amixer  # pylint: disable-msg=no-name-in-module
except ImportError:
    amixer = None


def _mpd_service(start_string, display=False):
    """Run the service command for the mpd daemon as root"""
    os_status, output = commands.getstatusoutput(
        '/usr/bin/sudo /usr/sbin/service mpd %s' % start_string)
    if display:
        print output
    elif os_status != os.EX_OK:
        print >> sys.stderr, output
    else:
        unmute()


def status():
    """Show the status of the mpd daemon"""
    _mpd_service('status', display=True)


def stop():
    """Stop the mpd daemon"""
    _mpd_service('stop')


def start():
    """Start the mpd daemon"""
    _mpd_service('start')


def restart():
    """Restart mpd's daemon"""
    _mpd_service('restart')


def unmute():
    """Use alsa mixer to unmute channels

    This is probably machine-specific
    """
    if not amixer:
        print >> sys.stderr, 'Could not import amixer'
        return
    channel_names = ['Master', 'Front', 'Headphone']
    channels = [','.join([c, '0']) for c in channel_names]
    _ = [amixer.sset(channel, 'unmute') for channel in channels]


def mpd_log():
    with open('/var/log/mpd/mpd.log') as stream:
        for line in stream:
            print line.rstrip()


def mpd_conf():
    print 'sudo vim /etc/mpd.conf'
