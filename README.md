# camero

A minimal multi-platform motion-detection based security program capable of recording multiple audio/video sources.

**camero targets the DIY community who needs a security camera software and yet doesn't trust the tools available on the net.** For this reason camero has an extremely simple source code (~200 line including exaustive comments) in order for everyone with few programming skills to check it and possibly edit it. camero is vapable of having such small code base because it makes wise use of the best, reliable and well known libraries around:

- Audio capture is done with [PortAudio](http://audioport.org) through [PyAudio](https://people.csail.mit.edu/hubert/pyaudio/), while video is captured with [imutils](https://github.com/jrosebr1/imutils)
- Motion detection is performed with [OpenCV](https://docs.opencv.org/master/d1/dfb/intro.html)
- Audio outstream and mixing with video are done with [ffmpeg](https://ffmpeg.org)
- Even if camero doesn't provide its own cloud uploading capabilities (e.g. to check the cam when  you are not at home), you can just save videos on a cloud-mounted filesystem or folder (e.g. Dropbox folder) to have them automatically uploaded on the net.

### Download binaries

Binaries exist only for Windows10 intel64bit architecture: [camero-rc29b962-win-amd64.exe](https://drive.google.com/file/d/1wMkS8kcDpPYoT-4IEiH6XBLqGXJE6zCD/view?usp=sharing)
You also need a config ini file (here a sample one: [camero.ini](https://github.com/aragagnin/camero/blob/master/camero.ini))

For all other acrhitectures you need to download [camero.py](https://github.com/aragagnin/camero/blob/master/camero.py) and run it with `python`. Check  sections below to see how to install the requirements. 

### Install from source

Install the video recorder with the commands

```bash
python -mpip install imutils
python -mpip install opencv-python
```

You can also install [PyAudio](https://pypi.org/project/PyAudio/) in order to record audio. 
The installation is not straightforward. However, if you do not manage to install it, Camero will still work, but it wont record audio.

To install `pyaudio` on **Debian Linux** or Raspberry PI (Raspbian) os, run:
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

Download a pre-compiled wheel for your architecture (`pXX` is the python version) from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio and install it with pip. For instance you have a 64bit system with python3.7 then **download** the file `PyAudio‑0.2.11‑cp36‑cp36m‑win_amd64.whl` and, on the same folder run `pip install PyAudio‑0.2.11‑cp39‑cp39‑win_amd64.whl`.

### Resources

Here online resources I used to produce this tool:

- Basic tutorial on motion detection and camera capture: https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/
- How to record audio from pyaudio: https://stackoverflow.com/questions/36894315/how-to-select-a-specific-input-device-with-pyaudio
- How to install PyAudio on windows: https://stackoverflow.com/questions/51992375/python-package-installation-issues-pyaudio-portaudio
- How to deal with wave files: https://stackoverflow.com/questions/35970282/what-are-chunks-samples-and-frames-when-using-pyaudio
- How to add a `press enter to return` command when running camero on Windows:   https://stackoverflow.com/questions/404744/determining-application-path-in-a-python-exe-generated-by-pyinstaller

### Todo

- camero should read commands from the filesystem. For instance, if I am not at home and want to look at all cameras, I may start camero on a Dropbox folder and then remotely adds a file that sends said command
- the config file should have hooks: e.g. send an email on motion detection

