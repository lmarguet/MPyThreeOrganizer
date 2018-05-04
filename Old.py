import glob2
import eyed3
import os
import shutil
import time
from tinytag import TinyTag


delay = 0.01
export_folder = "/Export"

### create folder
def create_folder(folder):
    directory =  folder + "/"
    print("     Moving to folder: " + directory)
    os.makedirs(os.path.dirname(directory), exist_ok=True)

### move MP3
def reorganise_mp3(file):
    print("### Checking: " + file)
    tag = TinyTag.get(file)

    artist = tag.artist
    album = tag.album
    album_artist = tag.albumartist

    path = export_folder + "/"
    if (artist == None) and (album_artist != None):
        artist = album_artist

    if artist != None:
        print("     Artist: " + artist)
        path += artist

    if album != None:
        print("     Album: " + album)
        path += "/" + album

    # path = os.getcwd() + path
    # create_folder(path)
    # shutil.copy2(file, path)
    print("     ## Complete! ##")


### main
files = glob2.glob('*.mp3')
for file in files:
    reorganise_mp3(file)
    print("\n")
    time.sleep(delay)
