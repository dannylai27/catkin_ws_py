#!/usr/bin/env python3
import rospy
from rospy_tutorials.msg import Floats
import numpy as np
import cv2 as cv

def circle_detector():
    # ROS publisher init
    pub = rospy.Publisher('detecting_point', Floats, queue_size=10)
    rospy.init_node('CV', anonymous=True)
    rate = rospy.Rate(25) # 25hz
    points = Floats()
    img_width = 640.0
    img_height = 480.0

    cap = cv.VideoCapture(2)
    cap.set(3, img_width)


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
        gray = cv.medianBlur(gray, 5)
        rows = gray.shape[0]
        # HoughCircles detection
        circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, rows / 8,
                                   param1=100, param2=30,
                                   minRadius=20, maxRadius=40)
                                   
        # Publish circle information
        if circles is not None:
            target = circles[0][0]
            target = target.tolist()
            points.data = [target[0] - img_width/2, target[1] - img_height/2, 0]
            rospy.loginfo(points)
            pub.publish(points)
            rate.sleep()
        else:
            points.data = [1000, 1000, 0]
            print("no detection")
            # rospy.loginfo(points)
            # pub.publish(points)
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
