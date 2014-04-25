"""Basic facilities for playing music"""


import mpd


def play(arg):
    raise NotImplementedError(repr(arg))


def mpd_client(server=None, port=None):
    """Connect to mpd on that server at that port"""
    server = server if server else 'localhost'
    port = port if port else 6600
    client = mpd.MPDClient()
    client.timeout = 1
    client.idletimeout = None
    client.connect(server, port)
    return client


def toggle(client):
    """If paused play, and vice versa"""
    state = client.status()['state']
    print state
    if state == 'pause':
        client.play()
    else:
        client.pause()
    state = client.status()['state']
    print state


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
