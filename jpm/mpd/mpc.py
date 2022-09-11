"""Access mpd through the python client"""


import os
import mpd  # despite the name, this has a client


from jpm.files import get_art


class Mpc(mpd.MPDClient):
    def __init__(self):
        super(Mpc, self).__init__()
        self.server = 'localhost'
        self.port = 6600
        self.mpc = None
        self.connect_locally()

    def connect_locally(self):
        self.connect_to('localhost', 6600)

    def connect_to(self, server, port):
        server = server if server else self.server
        port = port if port else self.port
        self.mpc = mpd.MPDClient()
        self.mpc.timeout = 1
        self.mpc.idletimeout = None
        self.mpc.connect(server, port)

    def prev(self):
        self.mpc.previous()

    def _state(self):
        try:
            return self.mpc.status()['state']
        except mpd.ConnectionError:
            return "Disconnected"

    def state_is_not(self, string):
        return self._state() != string

    def current(self):
        print self.format_current_album()

    def play(self):
        """If not already playing play"""
        if self.state_is_not('play'):
            self.mpc.play()

    def toggle(self):
        """If paused play, and vice versa"""
        if self.state_is_not('pause'):
            self.mpc.pause()
        else:
            self.play()

    def path_to_current(self):
        return self.mpc.currentsong()['file']

    def current_album(self):
        try:
            current_song = self.mpc.currentsong()
        except mpd.ConnectionError:
            return None, None, None, []
        title = current_song.get('title', None)
        album = current_song.get('album', None)
        artist = current_song.get('artist', None)
        path = current_song.get('file', None)
        if path:
            if path.startswith('Compilations'):
                tracks = self.mpc.find('album', album)
            else:
                tracks = self.mpc.find('album', album, 'artist', artist)
        else:
            tracks = []
        other_tracks = [t for t in tracks if t['title'] != title]
        other_titles = [t['title'] for t in other_tracks]
        return artist, album, title, other_titles

    def format_current_album(self):
        artist, album, title, other_titles = self.current_album()
        other_string = ''
        if other_titles:
            other_string = 'Others:%s' % '\n\t'.join([''] + other_titles)
        return '''
        Artist: %s
         Album: %s
         Track: %s
        %s''' % (artist, album, title, other_string)

    def current_art(self):
        relative_path = self.mpc.currentsong()['file']
        root = os.path.expanduser('~/media/music')
        path = os.path.join(root, relative_path)
        return get_art(path)
