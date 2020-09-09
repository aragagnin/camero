# camero
Camero: A minimal multi-platform, multi-audio/video inputs, and cloud-friendly webcam  security system based on motion detection

### Install Video Recorder


```bash
python -mpip install imutils
python -mpip install opencv-python
```

### Install Audio Recorder

Note: If you do not manage to unstall [PyAudio](https://pypi.org/project/PyAudio/), Camero will still work, but it wont record audio.

On **Linux**:
```bash
sudo apt-get install python-pyaudio python3-pyaudio 
pip install pyaudio
```

On **Apple OS X** use [HomeBrew](https://brew.sh/index_it):
```bash
brew install portaudio
pip install pyaudio
``` 

On **Windows**:

Download a wheel for your system (`pXX` is the python version) from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio and install it with pip. For instance you have a 64bit system with python3.7 then **download** the file `PyAudio‑0.2.11‑cp36‑cp36m‑win_amd64.whl` and, on the same folder run `pip install PyAudio‑0.2.11‑cp39‑cp39‑win_amd64.whl`.
