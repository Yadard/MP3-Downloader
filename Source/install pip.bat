@ECHO OFF
call conda create -n MP3
call conda activate MP3
call python -m pip install moviepy
call python -m pip install mutagen
call python -m pip install git+https://github.com/nficano/pytube
cd "C:\Users\Cliente\Desktop\Programing\Python\MP3 Downloader (mobile)"
call cls
python main.py
call conda deactivate MP3
PAUSE
