"""Handle music files for jpm

Presumed to be *.mp3 until further notice
"""


def get_art(path):
    from mutagen.id3 import ID3
    frames = ID3(path)
    try:
        pic = frames.getall("APIC")[0]
        group, ext = pic.mime.split('/', 1)
        if group != 'image':
            return None, None
        return pic.data, ext
    except:  # pylint: disable=bare-except
        pass
    return None, None