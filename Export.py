import os
import time
from pathlib import Path
from mutagen.easyid3 import EasyID3
import shutil

delay = 0.01
import_folder = "C:/Users/Lucas/Music/Jenni/"
# import_folder = "C:/Users\Lucas\Work\Python\MPyThreeOrganizer-master\Audio"
export_folder = "C:/Users/Lucas/Music/JenniExport"
unresolved_folder = "C:/Users/Lucas/Music/JenniSortme"

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
    global num_files_processed
    global num_errors

    num_files_processed += 1

    print("### Checking: ", os.path.basename(file))
    base_name = get_file_name(file)
    extension = os.path.basename(file)
    extension = os.path.splitext(extension)[1]

    try:
        audio_file = EasyID3(str(file))
    except:
        print("Error")
        move_file_to(file, unresolved_folder)
        num_errors += 1
        return


    album = get_tag_from_audio(audio_file, "album", fallback_album);
    title = get_tag_from_audio(audio_file, "title", base_name)

    artist = get_tag_from_audio(audio_file, "artist", None)
    album_artist = get_tag_from_audio(audio_file, "albumartist", None)
    author =  get_tag_from_audio(audio_file, "author", None)

    artist = resolve_artist(album_artist, artist, author)
    artist = strip_enclosing_whitespaces(artist)
    album = strip_enclosing_whitespaces(album)
    title = strip_enclosing_whitespaces(title)

    destination = Path(export_folder).resolve()
    destination = destination.joinpath(artist)
    destination = destination.joinpath(album)
    destination.resolve()
    destination.mkdir(0o777, True, True)

    destination_file = str(destination) + os.sep + title + extension

    move_file_to(file, destination_file)

    print('%-40s %-40s %-40s %-100s' % (artist, album, title, destination_file))


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
organize_files_with_extensions(import_path, "m4a")



print("Num processed: {0}  Num errors: {1}".format(num_files_processed, num_errors))
