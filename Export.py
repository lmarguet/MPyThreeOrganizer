import os
import time
from pathlib import Path
from mutagen.easyid3 import EasyID3
import shutil
import sys
from tinytag import TinyTag

delay = 0.01
# import_folder = "C:/Users/Lucas/Music/Jenni/"
import_folder = "C:/Users\Lucas\Work\Python\MPyThreeOrganizer\Audio"
# export_folder = "C:/Users/Lucas/Music/JenniExport"
export_folder = "C:/Users\Lucas\Work\Python\MPyThreeOrganizer\Export"
# unresolved_folder = "C:/Users/Lucas/Music/JenniSortme"
unresolved_folder = "C:/Users\Lucas\Work\Python\MPyThreeOrganizer\Error"

fallback_artist = "Unknown Artist"
fallback_album = "Unknown Album"


## Setup
num_files_processed = 0
num_errors = 0

import_path = Path(import_folder + os.sep).resolve()

export_path = Path(export_folder).resolve()
export_path.mkdir(0o777, True, True)

unresolved_path = Path(unresolved_folder).resolve()
unresolved_path.mkdir(0o777, True, True)


print("Import path:", import_path)
print("Export path:", export_path)


def organize_files_with_extensions(path, extension):
    for file in import_path.glob("*." + extension):
        process_file(file)
        time.sleep(delay)
        print(os.linesep)


def move_file_to(file, unresolved_folder):
    try:
        shutil.copy2(file, unresolved_folder)
        os.remove(file)
    except:
        print("Cant not move {0}".format(file))
    return


def process_file(file):
    print("### Checking: ", os.path.basename(file))

    global num_files_processed
    global num_errors
    num_files_processed += 1

    base_name = get_file_name(file)
    extension = os.path.basename(file)
    extension = os.path.splitext(extension)[1]

    try:
        audio_info = get_audio_info(str(file), base_name, extension)
    except:
        print(sys.exc_info())
        move_file_to(file, unresolved_folder)
        num_errors += 1
        return

    artist = audio_info[0]
    album = audio_info[1]
    title = audio_info[2]

    destination_file = create_destination_file_path(album, artist, title, extension)

    move_file_to(file, destination_file)

    print('%-40s %-40s %-40s %-100s' % (artist, album, title, destination_file))

def get_audio_info(path, base_name, extension):
    if extension == ".mp3":
        return  get_MP3_info(path, base_name)
    if extension == ".m4a":
        return  get_M4A_info(path, base_name)

    raise ValueError('Format not supported: {0}'.format(extension))


def get_MP3_info(path, base_name):
    audio_file = EasyID3(path)

    album = get_tag_from_ID3(audio_file, "album", fallback_album)
    album = filter_tag_string(album)

    title = get_tag_from_ID3(audio_file, "title", base_name)
    title = filter_tag_string(title)

    artist = get_tag_from_ID3(audio_file, "artist", None)
    album_artist = get_tag_from_ID3(audio_file, "albumartist", None)
    author = get_tag_from_ID3(audio_file, "author", None)

    artist = resolve_artist(album_artist, artist, author)
    artist = filter_tag_string(artist)

    return (artist, album, title)


def get_M4A_info(path, base_name):
    tag = TinyTag.get(path)
    album = tag.album if tag.album else fallback_album
    album = filter_tag_string(album)

    title = tag.title if tag.title else base_name
    title = filter_tag_string(title)

    artist = tag.artist
    album_artist = tag.albumartist

    artist = resolve_artist(album_artist, artist, None)
    artist = filter_tag_string(artist)

    return (artist, album, title)


def filter_tag_string(tag_field):
    tag_field = char_filter(tag_field)
    return strip_enclosing_whitespaces(tag_field)


def create_destination_file_path(album, artist, title, extension):
    destination = Path(export_folder).resolve()
    destination = destination.joinpath(artist)
    destination = destination.joinpath(album)
    destination.resolve()
    destination.mkdir(0o777, True, True)
    destination_file = str(destination) + os.sep + title + extension
    return destination_file


def strip_enclosing_whitespaces(value):
    value = value.rstrip()
    value = value.lstrip()
    return value


def resolve_artist(album_artist, artist, author):
    return artist if artist != None else album_artist if album_artist != None else author if author != None else fallback_artist


def get_file_name(file):
    base_name = os.path.basename(file)
    base_name = os.path.splitext(base_name)[0]
    base_name = char_filter(base_name)
    return base_name


def get_tag_from_ID3(audio, tag, fallback):
    if (tag in audio):
        return str(audio[tag])
    else:
        return fallback


def char_filter(myString):
    set = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 -&'
    return ''.join([c for c in myString if c in set])


######### organize
organize_files_with_extensions(import_path, "mp3")
organize_files_with_extensions(import_path, "m4a")



print("Num processed: {0}  Num errors: {1}".format(num_files_processed, num_errors))
