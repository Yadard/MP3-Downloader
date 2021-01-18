from typing import Dict

import pytube
from tqdm import tqdm
from pytube import monostate

bar = None


def progressBar(stream, chunk, bytes_remaining):
    global bar
    bar.update(stream.filesize - bytes_remaining)


vid = pytube.YouTube("https://www.youtube.com/watch?v=m_7JMmBW-Zc", on_progress_callback=progressBar)
bar = tqdm(total=vid.streams.first().filesize, position=0, leave=False, unit_scale=True, unit='it')
bar.set_description("downloading :")
vid.streams.first().download()
