# import the necessary packages
from imutils.video import VideoStream
import argparse
import numpy as np
import datetime
import imutils
import time
import numpy
import datetime
import cv2



icams=[0,1]
threshold = 1000
width=500
fps=10
output='out.mp4'
output_codec = 'MJPG'
output_min_seconds = 30
fourcc =  cv2.VideoWriter_fourcc(*output_codec) #cv2.cv.FOURCC(codec=codec)#cv2.VideoWriter_fourcc(codec)
quit = False

cams = {}

for icam in icams:
  cam = cams[icam]={}
  cam['frame_gray_prev'] =  None
  cam['writer_time'] = None
  cam['writer'] = None
  cam['vs']  =VideoStream(icam).start()
  
while not quit:
  for icam in icams:
    cam = cams[icam]
    frame = cam['vs'].read()     #cam['vs'].read()
    frame = imutils.resize(frame, width=width)
    cv2.imshow("Security Feed %d"%icam  , frame)
      
    if frame is None:
      break
    
    frame_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    frame_gray = cv2.GaussianBlur(frame_gray,(25,25),0)
    frame_gray_prev = cam['frame_gray_prev']
    writer_time = cam['writer_time']
    
    if  frame_gray_prev is not None:
      frame_delta = cv2.absdiff(frame_gray_prev, frame_gray)
      frame_threshold = cv2.threshold(frame_delta, 30, 255, cv2.THRESH_BINARY)[1]  
      now = time.time()
      over = np.sum(frame_threshold)>threshold
      if over or (writer_time is not None and  now<=(writer_time+output_min_seconds)): 
        (h, w) = frame.shape[:2]
       
        if cam['writer'] is None:
          name = output+datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
          print('I start record ',name)
          cam['writer']  = cv2.VideoWriter(
            '%s_cam%d_%s'%(name,icam, output),
            fourcc, fps,(w, h), True
           )
        if over:
          cam['writer_time'] = now
        cam['writer'].write(frame)
      elif cam['writer'] is not None:
        print('I close record ')
        cam['writer'].release()
        cam['writer_time'] =   None 
        cam['writer'] = None
        
    cam['frame_gray_prev'] = frame_gray
   
    key = cv2.waitKey(1) & 0xFF
    # if the `q` key is pressed, break from the lop
    if key == ord("q"):
      quit = True
      
cv2.destroyAllWindows()
for icam in icams:
  cam['vs'].stop()
  if cam['writer'] is not None:
    cam['writer'].release()
    
