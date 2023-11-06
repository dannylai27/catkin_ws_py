#!/usr/bin/env python
import rospy
from rospy_tutorials.msg import Floats
import numpy as np
import cv2 as cv
import time

def circle_detector():
    # ROS publisher init
    pub = rospy.Publisher('detecting_point', Floats, queue_size=1)
    rospy.init_node('CV', anonymous=True)
    rate = rospy.Rate(40) # 40hz
    points = Floats()

    #cap = cv.VideoCapture("/dev/video1") #/dev/video0 for the embedded camera #/dev/video1 for the external camer
    #cap = cv.VideoCapture("/dev/video0")
    cap = cv.VideoCapture("/dev/video1")
    #cap = cv.VideoCapture(1)  #0 for the embedded webcam

    cap.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc(*'MJPG'))
    cap.set(3, 640.0)

    if not cap.isOpened():
        print("Cannot open camera")
        exit()
        
    while not rospy.is_shutdown():
        # Capture frame-by-frame
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        # Our operations on the frame come here
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # Smooth the image
        gray = cv.medianBlur(gray, 5)

        # Call the circle detection
        rows = gray.shape[0]
        circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, rows / 8,
                                   param1=100, param2=30,
                                   minRadius=50, maxRadius=80)
	t = rospy.Time.now()

        if circles is not None:
            target = circles[0][0]
            target_list = target.tolist()
            points.data = [target_list[0],target_list[1],target_list[2],t.secs, t.nsecs]	    
            rospy.loginfo(points)
            pub.publish(points)
            rate.sleep()

	else:
            points.data = [1000.0, 0.0, 0.0, t.secs, t.nsecs]
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
