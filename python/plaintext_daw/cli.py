import os
import sys

import yaml

from plaintext_daw.resource_manager import ResourceManager

from .gui import gui
from .models import Song


def print_usage():
    print("Usage:")
    print("  plaintext-daw render <FILE>: render project file to wav")
    print("  plaintext-daw gui:           open a GUI")


def cli_entry_point(args=sys.argv):
    if len(args) >= 2:
        if args[1] == 'gui':
            exit(gui())
        elif args[1] == 'render':
            if len(args) >= 3:
                config_path = args[2]
                if not os.path.exists(config_path):
                    print("Error: %s not found" % config_path, file=sys.stderr)
                    sys.exit(1)
                # Load config
                rm = ResourceManager(os.path.dirname(config_path))
                config = rm.get_config_from_file(os.path.basename(config_path))
                song = rm.get_song(config)
                # Render song to file
                song.render('song.wav')
            else:
                print_usage()
        else:
            print_usage()
    else:
        print_usage()
