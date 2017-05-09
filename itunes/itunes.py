"""Facilities for handling iTunes

I used to listen through iTunes on various Macs
    but I stopped liking the UI at Lion (iTunes 10)
So I need some methods to read all the data thence
    and write it to a new format

Other info would be nice to have
    but I must gather the ratings!
"""

from pathlib import Path
import plistlib


def read_itunes_library(path_to_lib):
    path = Path(path_to_lib)
    assert path.is_file()
    return plistlib.readPlist(path)  # pylint: disable=deprecated-method

local_lib = ('/Users/jab/Downloads/jab.ook/HD/Users/jab/'
             'Music/iTunes/iTunes Music Library.xml')
plist = read_itunes_library(local_lib)
