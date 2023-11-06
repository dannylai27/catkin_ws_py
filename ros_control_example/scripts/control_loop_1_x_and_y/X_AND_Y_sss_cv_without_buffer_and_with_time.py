#!/usr/bin/env python
# coding=utf-8
import rospy
from rospy_tutorials.msg import Floats
import numpy as np
import cv2 as cv
import Queue,threading, time		#queue with q instead of Q in python 3... io ho il 2.7


#bufferless VideoCapture
class VideoCapture:

  def __init__(self, name):
    self.cap = cv.VideoCapture(name)
    self.q = Queue.Queue()
    t = threading.Thread(target=self._reader)
    t.daemon = True
    t.start()

  # read frames as soon as they are available, keeping only most recent one
  def _reader(self):
    while True:
      ret, frame = self.cap.read()
      if not ret:
        break
      if not self.q.empty():
        try:
          self.q.get_nowait()   # discard previous (unprocessed) frame
        except queue.Empty:
          pass
      self.q.put(frame)

  def read(self):
    return self.q.get()


# IN C++
#cv::VideoCapture cap;
#cap.set(CV_CAP_PROP_BUFFERSIZE, 3); // internal buffer will now store only 3 frames

    #cap.set(cv.CAP_PROP_BUFFERSIZE, 1)
    #VIDEOIO ERROR: V4L2: setting property #38 is not supported
    #we use an alternative solution with threads to give only the last image captured



def circle_detector():
    # ROS publisher init
    pub = rospy.Publisher('detecting_point', Floats, queue_size=1)
    rospy.init_node('CV', anonymous=True)
    rate = rospy.Rate(40) # 40hz
    points = Floats()

    #cap = cv.VideoCapture("/dev/video1") #/dev/video0 for the embedded camera #/dev/video1 for the external camer
    #cap = cv.VideoCapture("/dev/video1")
    #cap = cv.VideoCapture("/dev/video0")
    #cap_1 = VideoCapture()  #senza cv. perchè chiamiamo la classe da noi creata senza buffer
    #cap = cap_1("/dev/video0")
    #cap = cv.VideoCapture(1)  #0 for the embedded webcam

    #cap = VideoCapture("/dev/video0")
    cap = VideoCapture("/dev/video1")

    #if not cap.isOpened():
    #    print("Cannot open camera")
    #    exit()
        
    while not rospy.is_shutdown():
        # Capture frame-by-frame
        #ret, frame = cap.read()
        # if frame is read correctly ret is True
        #if not ret:
        #    print("Can't receive frame (stream end?). Exiting ...")
        #    break
        # Our operations on the frame come here
	t = rospy.Time.now()

        frame = cap.read()
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # Smooth the image
        gray = cv.medianBlur(gray, 5)

        # Call the circle detection
        rows = gray.shape[0]
        circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, rows / 8,
                                   param1=100, param2=30,
                                   minRadius=50, maxRadius=80)
        if circles is not None:
            target = circles[0][0]
	    target_list = target.tolist()
            points.data = [target_list[0],target_list[1],target_list[2],t.secs, t.nsecs]
            rospy.loginfo(points)
            pub.publish(points)
            rate.sleep()

	else:
            points.data = [1000.0, 0.0, 0.0, t.secs, t.nsecs] # [x y radius seconds nanoseconds]
            rospy.loginfo(points)
            pub.publish(points)
            rate.sleep()

	
    # Draw circle
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                center = (i[0], i[1])
                # circle center
                cv.circle(frame, center, 1, (0, 100, 100), 3)
                # circle outline
                radius = i[2]
                cv.circle(frame, center, radius, (255, 0, 255), 3)

        # Display the resulting frame
        cv.imshow('detected circle', frame)
        

        
        
        if cv.waitKey(1) == ord('q'):
            break
        
        
        
       
    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    try:
        circle_detector()
    except rospy.ROSInterruptException:
        pass
