# camero

A minimal multi-platform, multi-audio/video inputs, and cloud-friendly webcam  security system based on motion detection

### Download binaries

You can download the a precompiled boundle here: [camero-win10-amd64.exe](https://drive.google.com/file/d/18FpUGbcIDvspxPux_FETAQSe_cIaxVAV/view?usp=sharing)

### Install from source

Install the video recorder with the commands

```bash
python -mpip install imutils
python -mpip install opencv-python
```

You can also install [PyAudio](https://pypi.org/project/PyAudio/) in order to record audio. 
The installation is not straightforward. However, if you do not manage to install it, Camero will still work, but it wont record audio.

To install `pyaudio` on **Debian Linux** run:
```bash
sudo apt-get install python-pyaudio python3-pyaudio 
pip install pyaudio
```

To install `pyaudio` on **Apple OS X** use [HomeBrew](https://brew.sh/index_it) and run:
```bash
brew install portaudio
pip install pyaudio
``` 

To install `pyaudio` on  **Windows:**

Download a wheel for your system (`pXX` is the python version) from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio and install it with pip. For instance you have a 64bit system with python3.7 then **download** the file `PyAudio‑0.2.11‑cp36‑cp36m‑win_amd64.whl` and, on the same folder run `pip install PyAudio‑0.2.11‑cp39‑cp39‑win_amd64.whl`.

