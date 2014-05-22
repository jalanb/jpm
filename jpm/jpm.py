"""Basic facilities for playing music"""


import os
import mpd


from dotsite.decorators import memoize


def _state(client):
    return client.status()['state']


def _state_is_not(client, string):
    return _state(client) != string


@memoize
def mpd_client(server=None, port=None):
    """Connect to mpd on that server at that port"""
    server = server if server else 'localhost'
    port = port if port else 6600
    client = mpd.MPDClient()
    client.timeout = 1
    client.idletimeout = None
    client.connect(server, port)
    return client


def pause(client):
    """If not already paused pause"""
    if _state_is_not(client, 'pause'):
        client.pause()


def play(client):
    """If not already playing play"""
    if _state_is_not(client, 'play'):
        client.play()


def toggle(client):
    """If paused play, and vice versa"""
    if _state_is_not(client, 'pause'):
        client.pause()
    else:
        client.play()


def path_to_current(client):
    return client.currentsong()['file']


def current_album(client):
    title = client.currentsong()['title']
    album = client.currentsong()['album']
    artist = client.currentsong()['artist']
    path = client.currentsong()['file']
    if path.startswith('Compilations'):
        tracks = client.find('album', album)
    else:
        tracks = client.find('album', album, 'artist', artist)
    other_tracks = [t for t in tracks if t['title'] != title]
    other_titles = [t['title'] for t in other_tracks]
    return artist, album, title, other_titles


def format_current_album(client):
    artist, album, title, other_titles = current_album(client)
    other_string = ''
    if other_titles:
        other_string = 'Others:%s' % '\n\t'.join([''] + other_titles)
    return '''
    Artist: %s
     Album: %s
     Track: %s
    %s''' % (artist, album, title, other_string)


def current_art(client):
    relative_path = client.currentsong()['file']
    root = os.path.expanduser('~/media/music')
    path = os.path.join(root, relative_path)
    return get_art(path)


def get_art(path):
    from mutagen.id3 import ID3
    frames = ID3(path)
    try:
        pic = frames.getall("APIC")[0]
        group, ext = pic.mime.split('/', 1)
        if group != 'image':
            return None, None
        return pic.data, ext
    except:  # pylint: disable-msg=W0702
        pass
    return None, None
