import argparse, os, sys, numpy as np, datetime, imutils, imutils.video, time, datetime, cv2, configparser, wave
__version__ = 0.1


print('\nWelcome to Camero ver ',__version__)
print('Author: Antonio Ragagnin\n')

#
# read [DEFAULT] section of INI file and stores it in the dictionary `conf`
# data will be then read as, for instance, conf['video']['output_codec']
try:
    conf = configparser.ConfigParser()
    conf.read('camero.ini')
except Exception as e:
    print('\nError loading camero.ini:\n')
    raise

#
# find audio devices capable of recording and add them to the list `pyaudo_recorders`
#
pyaudo_recorders = []
try:
    #try to import pyaudio
    import pyaudio
    #extract integer values of audio_device_indexes from the respective INI key
    audio_device_indexes = map(int, conf['audio']['device_indexes'].split(','))
    audio_chunk_size = conf['audio'].getint('chunk_size')
    #initialise PyAudio
    pyaudio_o = pyaudio.PyAudio()
    #get number of devices
    pyaudio_numdevices =  pyaudio_o.get_host_api_info_by_index(0).get('deviceCount')
    print('\nPyAudio found %d audio devices:', pyaudio_numdevices)
    for i in range(0, pyaudio_numdevices):
        # for each devie we check if we can use it as input device, es. we check number of input channels
        device_info = pyaudio_o.get_device_info_by_host_api_device_index(0, i)
        device_input_channels = (device_info).get('maxInputChannels')
        print("    Device id:", i, " ", device_info.get('name'), " (channels: ",device_input_channels)
        if i in audio_device_indexes and device_input_channels>0:
            stream = pyaudio_o.open(format=pyaudio.paInt16,
                    channels=device_input_channels,
                    rate=44100,
                    input=True,
                    frames_per_buffer=1024,
                    input_device_index=i)
            pyaudo_recorders.append({"stream":stream,"buffer":None, "i":i, "channels":device_input_channels})
            print("       Opened for recording (actual recording will start only on motio-detection).")
    pyaudio_active = True
except Exception as e:
    # if we fail to record audio, we just say it and go on with the program
    # audio recording is not a vital part of security monitoring
    print(e)
    print('\nPyAudio not found. We keep going anyway.\n')
    pyaudio_active = False

#
# here below we find avaialbe webcams and grab the ones specified in device_indexes
# the dictionary `cams` will contains the relative objects
cams = {}
icams = [icam for icam in map(int, conf['video']['device_indexes'].split(','))]
print('\nSearching for webcams with device-id', icams)
icam = -1
while True:
    icam+=1
    try:
        cap = cv2.VideoCapture(icam)
        vs  = imutils.video.VideoStream(icam).start()
        if cap is None or  not cap.isOpened():
            break
        if icam in icams:
            cam = {}
            cam['frame_gray_prev'] =  None
            cam['writer_time'] = None
            cam['writer'] = None
            cam['vs'] =vs
            cams[icam] = cam
            print('    Webcam with id',icam,' is ready to be used.')
        else:
            print('    Webcam with id',icam,' is ignored as requested')
    except:
        raise
        break

# we grab data from the INI file
fourcc =  cv2.VideoWriter_fourcc(*conf['video']['output_codec'])
threshold = conf['video'].getint('diff_threshold')
show_feed = conf['misc']['show_feed']
output_prefix = conf['misc']['output_prefix']
fps = conf['video'].getint('fps')
ffmpeg_path = conf['misc']['ffmpeg_path']
ffmpeg_use = conf['misc']['ffmpeg_use']
output_min_seconds = conf['video'].getint('output_min_seconds')
recording_count = 0
# quit will be set to true on keypress of key `q. Two quit variables
# allow for an extra iteration where we can safely save movies
quit_ask = False
quit = False
while not quit:
    print('new iteration')
    if quit_ask:
        print('Last iteration! we will save everyting now!')
        quit = True
    # if any cam is recording then we grab audio from PyAudio
    if recording_count>0:
        for a in pyaudo_recorders:
            print('read chunk')
            a['buffer'] = a['stream'].read(audio_chunk_size)
            print('read chunk done' )
    # we loop over cams and check for motion detections
    for icam in cams:
        cam = cams[icam]
        frame = cam['vs'].read()     #cam['vs'].read()
        if frame is None:
            # if the camera failed, we skip this frame and hope for the best on the next one!
            continue

        frame = imutils.resize(frame, width=conf['video'].getint('width'))
        if show_feed:
            cv2.imshow("Security Feed %d"%icam  , frame)

        # we check for motion as in
        # https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/
        frame_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        frame_gray = cv2.GaussianBlur(frame_gray,(25,25),0)
        frame_gray_prev = cam['frame_gray_prev']
        writer_time = cam['writer_time']

        if  frame_gray_prev is not None:
            frame_delta = cv2.absdiff(frame_gray_prev, frame_gray)
            frame_threshold = cv2.threshold(frame_delta, 30, 255, cv2.THRESH_BINARY)[1]
            now = time.time()
            over = np.sum(frame_threshold)>threshold
            # we check if we found motion
            if not quit_ask and (over or (writer_time is not None and  now<=(writer_time+output_min_seconds))):
                (h, w) = frame.shape[:2]
                # start a new video if we didn't do it
                if cam['writer'] is None:
                    now_str = output_prefix+datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
                    print ('Motion detected in camera ',icam, ' with timestamp', now_str)
                    if pyaudio_active and recording_count==0:
                        print('Start recording audio streams')
                        for i,a in enumerate(pyaudo_recorders):
                            a['stream'].start_stream()

                    recording_count+=1
                    # we save now_str so we can save WAV file with same timing
                    cam['now_str'] = now_str
                    cam['name'] = '%s_cam%d.mp4'%(now_str,icam)
                    cam['writer']  = cv2.VideoWriter(
                        cam['name'],
                        fourcc, fps,(w, h), True
                        )
                    cam['audio_frames'] = [[] for i in range(len(pyaudo_recorders))]
                if over:
                    # we save the time so we can keep recording for a number of output_min_seconds
                    # even after motion finished
                    cam['writer_time'] = now

                for i in range(len(pyaudo_recorders)):
                    # we check we if we have sound already this iteration
                    if pyaudo_recorders[i]['buffer'] is not None:
                        cam['audio_frames'][i].append(pyaudo_recorders[i]['buffer'])

                cam['writer'].write(frame)

            elif cam['writer'] is not None:
                recording_count-=1

                print('I stop recording video ')
                cam['writer'].release()
                cam['writer_time'] =   None
                cam['writer'] = None
                if recording_count==0:
                    print('I stop recording voice as recording_count==0 ')
                for i,a in enumerate(pyaudo_recorders):
                    if recording_count==0:
                        stream.stop_stream()
                    wf = wave.open('%s_cam%d_mic%d.wav'%(cam['now_str'],icam,i), 'wb')
                    wf.setnchannels(a['channels'])
                    wf.setsampwidth(pyaudio_o.get_sample_size(pyaudio.paInt16))
                    wf.setframerate(44100)
                    wf.writeframes(b''.join(cam['audio_frames'][i]))
                    wf.close()
                if pyaudio_active and ffmpeg_use:
                    # we cook the ffmpeg command to merge audios and videos in one file
                    # don't worry, we print it too!
                    ffmpeg_command = ffmpeg_path + ' ' + (
                        (' '.join( ['-i %s'%'%s_cam%d_mic%d.wav'%(cam['now_str'],icam,i) for i,a in enumerate(pyaudo_recorders)]))+
                        (' -i  %s_cam%d.mp4'%(now_str,icam))+' '+
                        (' '.join(['-map %d'%(i) for i,a in enumerate(pyaudo_recorders)]))+
                        (' -map %d'%(len(pyaudo_recorders)))+
                        ('  -c copy %s_cam%d_mixed.mkv'%(cam['now_str'],icam)))
                    print('Going to execute ')
                    print(ffmpeg_command)
                    os.system(ffmpeg_command)
        cam['frame_gray_prev'] = frame_gray

        key = cv2.waitKey(1) & 0xFF
        # if the `q` key is pressed, break from the lop
        if key == ord("q"):
          quit_ask = True

cv2.destroyAllWindows()

for icam in cams:
    cam = cams[icam]
    cam['vs'].stop()
    if cam['writer'] is not None:
        cam['writer'].release()

for i,a in enumerate(pyaudo_recorders):
    a['stream'].stop_stream()
    a['stream'].close()
    pyaudio_o.terminate()

print('\nAll resources deallocated.\n')
