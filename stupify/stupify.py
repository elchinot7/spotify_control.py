#!/usr/bin/env python
#-*- coding: utf-8 -*-
# -----------------------------------------------
#     File:         stupify.py
#     Author:       elchinot7
#     Email:        efraazu@gmail.com
#     Github:       https://github.com/elchinot7
#     Description:  Control spotify from terminal
#     Example:
#                  python stupify.py -o 'title'
# -----------------------------------------------
'''
stupify.py - Command tool for Spotify client
Author: elchinot7
'''
import sys
import optparse
import dbus

__version__ = "0.1"

def get_metadata():
    """
    http://stackoverflow.com/questions/33883360/get-spotify-currently-playing-track
    :returns: (str) Spotify title/album/artist

    """
    session_bus = dbus.SessionBus()
    spotify_bus = session_bus.get_object("org.mpris.MediaPlayer2.spotify",
                                         "/org/mpris/MediaPlayer2")
    spotify_properties = dbus.Interface(spotify_bus,
                                        "org.freedesktop.DBus.Properties")
    metadata = spotify_properties.Get("org.mpris.MediaPlayer2.Player", "Metadata")
    # The property Metadata behaves like a python dict
    # for key, value in metadata.items():
    #     print key, value
    return metadata

def get_info(key):
    """Get the Spotify info

    :key: (str) 'title'/'album'/'artist'/'artist-title'
    :returns: (str) Spotify Info

    """
    spoty_info = get_metadata()

    if key == 'title':
        return spoty_info['xesam:title']
    elif key == 'album':
        return spoty_info['xesam:album']
    elif key == 'artist':
        return spoty_info['xesam:artist'][0]
    elif key == 'artist-title':
        return spoty_info['xesam:artist'][0] + '-' + spoty_info['xesam:title']
    else:
        return "-"

def main(argv=None):
    """Get spotify info

    'title' : get the title
    'album' : get the album
    'artist' : get the artist
    """
    if not argv:
        argv = sys.argv
    # Parse command line options
    usage = "%prog -o [options] \n" + __doc__
    parser = optparse.OptionParser(usage=usage, version=__version__)

    parser.add_option("-o", "--output", action='store', dest='key',
                      default="artist-title",
                      type="string",
                      metavar="STRING",
                      help="get the playing spotify title/album/artist \
                      [default:'artist-title']")
    (options, args) = parser.parse_args(args=argv[1:])

    try:
        print get_info(options.key)
    except Exception, e:
        print "-"

if __name__ == "__main__":
    main()
