import pytube
from pytube import exceptions
from os import getcwd, system
from time import time, sleep
from os.path import join
from datetime import datetime
import requests
from moviepy.editor import *
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TALB, TOPE
from shutil import rmtree
import threading


# TODO implement checker for already installed musics

def get_current_date():
    x = str(datetime.today()).split('-')
    return f'{x[1]}-{x[2][:2]}-{x[0]}'


def set_output(home, type='MP4s'):
    root = join(home, type)
    if not os.path.isdir(root):
        os.mkdir(root)
    path = join(root, get_current_date())
    if not os.path.isdir(path):
        os.mkdir(path)
    return path


def download_mp4(video: pytube.YouTube):
    stream = video.streams.get_by_itag(140)
    if " - " in video.title:
        filename_prefix = ""
    else:
        filename_prefix = f"{video.author.replace('- Topic', '')} - "
    output_path = stream.download(filename=video.title, filename_prefix=filename_prefix,
                                  output_path=set_output(getcwd()))
    return output_path, video


def convert_to_mp3(input_MP4: str):
    output_MP3 = input_MP4.replace(".mp4", ".mp3").replace("MP4s", "MP3s")
    set_output(getcwd(), type='MP3s')

    audioclip = AudioFileClip(input_MP4)
    audioclip.write_audiofile(output_MP3, verbose=False, logger=None)

    audioclip.close()
    return output_MP3


def set_cover(output_path, video: pytube.YouTube, playlist: str):
    file = MP3(output_path, ID3=ID3)
    try:
        file.add_tags()
    except:
        pass
    img_data = requests.get(video.thumbnail_url).content
    file.tags.add(APIC(encoding=3, mime='image/jpeg', type=3, data=img_data))
    if playlist is not None:
        file.tags.add(TALB(encoding=3, text=playlist))
    file.tags.add(TOPE(encoding=3, text=output_path.split('\\')[-1].split('-')[0][:-1]))
    file.save(v2_version=3)


def work(vid, title="Unnamed mix", isLast=True, usingThreads=False):
    name = threading.currentThread().name
    start = time()
    print(f"{name} is downloading")
    if usingThreads:
        sleep(0.5)
    MP4_info = tuple(download_mp4(vid))
    if isinstance(MP4_info, tuple):
        output_path = convert_to_mp3(MP4_info[0])
        set_cover(output_path, MP4_info[1], title)
        if os.path.isfile(output_path):
            print(f"{name} finished download\nthis download took {round(time()-start)}s\n")
            if isLast:
                rmtree(MP4_info[0].replace("\\{}".format(MP4_info[0].split('\\')[-1]), ""))


def work_handler(url, title):
    if "playlist" in url:
        isLast = False
        try:
            playlist = pytube.Playlist(url)
        except (exceptions.VideoUnavailable, exceptions.VideoRegionBlocked, exceptions.VideoPrivate):
            return -1
        for i in range(len(playlist)):  # TODO does it help not getting blocked by youtube?
            vid = pytube.YouTube(playlist[i])
            if i == len(playlist) - 1:
                isLast = True
            threading.Thread(name=vid.title, target=work, args=(vid, playlist.title, isLast, True)).start()
        print("\n"*2 + "=" * 50 + '\n')
    else:
        try:
            vid = pytube.YouTube(url)
            work(vid, title=title)
        except (exceptions.VideoUnavailable, exceptions.VideoRegionBlocked, exceptions.VideoPrivate):
            return -1


if __name__ == "__main__":
    url = input('url:')
    album = input("album name:")
    system("cls")
    x = work_handler(url, album)
