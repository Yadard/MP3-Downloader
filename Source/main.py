import pytube
from os import getcwd, system
from time import time, sleep
from os.path import join
from datetime import datetime
import requests
from moviepy.editor import *
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TALB, TOPE
import threading

# TODO implement checker for already installed musics
count_thread_named = 0


def get_current_date():
    x = str(datetime.today()).split('-')
    return f'{x[1]}-{x[2][:2]}-{x[0]}'


def set_output(home, type='MP4s'):
    path = join(home, type, get_current_date())
    if not os.path.isdir(path):
        os.mkdir(path)
    return path


def download_mp4(video: pytube.YouTube):
    stream = video.streams.get_by_itag(140)
    start = time()
    if " - " in video.title:
        filename_prefix = ""
    else:
        filename_prefix = f"{video.author.replace('- Topic', '')} - "
    thread = threading.currentThread()
    thread.name = filename_prefix + video.title
    global count_thread_named
    count_thread_named += 1
    output_path = stream.download(filename=video.title, filename_prefix=filename_prefix,
                                  output_path=set_output(getcwd()))
    #print(f"download took {round(time() - start, 2)}s")
    return (output_path, video)


def convert_to_mp3(input_MP4: str):
    output_MP3 = input_MP4.replace(".mp4", ".mp3").replace("MP4s", "MP3s")
    set_output(getcwd(), type='MP3s')

    audioclip = AudioFileClip(input_MP4)
    audioclip.write_audiofile(output_MP3, verbose=False, logger=None)

    audioclip.close()
    #print(f'{threading.currentThread().name} done converting to MP3')
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


def work(url, title=None):
    sleep(2)
    try:
        vid = pytube.YouTube(url)
    except:
        return -1
    MP4_info = download_mp4(vid)
    if isinstance(MP4_info, tuple):
        output_path = convert_to_mp3(MP4_info[0])
        set_cover(output_path, MP4_info[1], title)
        if os.path.isfile(output_path):
            return output_path


def work_handler(url):
    outputs = list()
    using_threads = False
    if "playlist" in url:
        try:
            playlist = pytube.Playlist(url)
        except:
            return -1
        count_vids = len(playlist)
        manager = threading.Thread(name='manager', target=thread_manager, args=(count_vids,))
        manager.start()
        for i in range(count_vids):
            urls = playlist[i]  # TODO does it help not getting blocked by youtube?
            using_threads = True
            threading.Thread(target=lambda x, url, title: x.append(work(url, title=title)),
                             args=(outputs, urls, playlist.title)).start()
    else:
        outputs.append(work(url))
    if using_threads:
        manager.join()
    return outputs


def thread_manager(videos_count):
    run = False
    while True:
        if count_thread_named == videos_count:
            run = True
        if run:
            threads = threading.enumerate()
            start = threads[-1*(len(threads)-2):]
            os.system('cls')
            for thread in start:
                if 'pydevd' not in thread.name:
                    print(f"{thread.name} is downloading...")
            print('\n' + "=" * 50 + "\n")
            while len(start) > 0:
                for thread in start:
                    if thread not in threading.enumerate():
                        if thread.name != "MainThread" and thread.name != "manager":
                            print(f"\"{thread.name}\" finished download")
                            start.remove(thread)
                sleep(2)
            break


if __name__ == "__main__":
    x = work_handler(input(':'))
    os.system('cls')
    for item in x:
        print("{} @ {}".format(item.split("\\")[-1], item.replace(getcwd(), "home")))
