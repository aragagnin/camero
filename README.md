# camero
Camero: A minimal multi-platform, multi-audio/video inputs, and cloud-friendly webcam  security system based on motion detection

## Install Video Recorder


```python -mpip install imutils
python -mpip install opencv-python
```

## Install Audio Recorder

Note: If you do not manage to unstall [PyAudio](https://pypi.org/project/PyAudio/), Camero will still work, but it wont record audio.

On **Linux**:
```sudo apt-get install python-pyaudio python3-pyaudio 
pip install pyaudio
```

On **Apple OS X** use [HomeBrew](https://brew.sh/index_it):
```brew install portaudio
pip install pyaudio
``` 

On **Windows** you have two possibilities:

**Method 1:** You can install or you install Visual Studio (https://visualstudio.microsoft.com/it/downloads/) and run `python -mpip install pyaudio`.

**Method 2:** you can download a wheel for your system (`pXX` is the python version) from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio and install it with, for instance, `pip install PyAudio‑0.2.11‑cp39‑cp39‑win_amd64.whl`.
