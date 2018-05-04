import os
import time
from pathlib import Path
from mutagen.easyid3 import EasyID3
import re;
import shutil

delay = 0.01
import_folder = "/Users/lucasmarguet/WorkPerso/Python/AudioOrganizer/Audio"
export_folder = "/Users/lucasmarguet/WorkPerso/Python/AudioOrganizer/Export"

fallback_artist = "Unknown Artist"
fallback_album = "Unknown Album"


## Setup
import_path = Path(import_folder + os.sep).resolve()
export_path = Path(export_folder).resolve()
export_path.mkdir(0o777, True, True)

print("Import path:", import_path)
print("Export path:", export_path)


def organize_files_with_extensions(path, extension):
    for file in import_path.glob("*." + extension):
        process_file(file)
        time.sleep(delay)
        print(os.linesep)


def process_file(file):
    # print("### Checking: ", os.path.basename(file))

    audio_file = EasyID3(file)
    base_name = get_file_name(file)

    extension = os.path.basename(file)
    extension = os.path.splitext(extension)[1]

    album = get_tag_from_audio(audio_file, "album", fallback_album);
    title = get_tag_from_audio(audio_file, "title", base_name)

    artist = get_tag_from_audio(audio_file, "artist", None)
    album_artist = get_tag_from_audio(audio_file, "albumartist", None)
    author =  get_tag_from_audio(audio_file, "author", None)

    artist = resolve_artist(album_artist, artist, author)

    destination = Path(export_folder).resolve()
    destination = destination.joinpath(artist)
    destination = destination.joinpath(album)
    destination.mkdir(0o777, True, True)

    destination_file = str(destination) + os.sep + title + extension
    print(destination_file)

    shutil.copy2(file, destination_file)

    print('%-40s %-40s %-40s' % (artist, album, title))


def resolve_artist(album_artist, artist, author):
    return artist if artist != None else album_artist if album_artist != None else author if author != None else fallback_artist


def get_file_name(file):
    base_name = os.path.basename(file)
    base_name = os.path.splitext(base_name)[0]
    base_name = char_filter(base_name)
    return base_name


def get_tag_from_audio(audio, tag, fallback):
    if (tag in audio):
        return char_filter(str(audio[tag]))
    else:
        return fallback


def char_filter(myString):
    set = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 -'
    return ''.join([c for c in myString if c in set])


######### organize
organize_files_with_extensions(import_path, "mp3")
