# This code was used in the national competitions of cubesats CubeDesign, 
# National Institute of Space Research, and is from authorship of Tiago
# Bachiega de Almeida and Zenith Aerospace - EESC.
#
# It receives an image of a representation of the Sun and of the Horizon Line, 
# taken in a simulated environment and processes the image trying to detect how 
# far the CubeSat is from pointing the Sun and the center of the line segment of
# the Horizon Line captured by the picamera.
#
# It's intended to be used in a Raspberry Pi

import cv2
import numpy as np

# Reads the image
img = cv2.imread('capture_1.jpg')

# Resizes the image in order to boost the processing
img_shape = img.shape
img_center_x = img_shape[1]/2
img_center_y = img_shape[0]/2

# Opening angle of the picamera
cam_angle = 160

# Output file
output_file = open("adc_cv.dat", "w")

# BGR to grayscale
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Finds the image contours
edges = cv2.Canny(imgGray,50,150,apertureSize = 3)

# Finds the lines in the image 
lines = cv2.HoughLines(edges,1,np.pi/180,10)

# Lines processing
if lines is not None: 
    for rho,theta in lines[0]:
        
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))
        
        # Limits the line length to
        # find it's center
        if x1 < 0:
            x1 = 0
            y1 = int(rho/b)
        if y1 < 0:
            y1 = 0
            x1 = int(rho/a)
        if x2 > img_shape[1]:
            x2 = img_shape[1]
            y2 = int((rho - x2*a)/b)
        if y2 > img_shape[0]:
            y2 = img_shape[0]
            x2 = int((rho - y2*b)/a)
    
    # Line center position
    pos_line = ((x1+x2)/2,(y1+y2)/2)
else:
    # Output if no line was found
    pos_line = (-1,-1)    

# Detects the circles
circles = cv2.HoughCircles(imgGray,cv2.HOUGH_GRADIENT,1,200, param1=10,param2=30,minRadius=2,maxRadius=100)

# Circles processin
if circles is not None:
    circles = np.uint16(np.around(circles))
    # Gets the biggest circle
    circles_s = sorted(circles, key=lambda tup: tup[:,2])
    # Gets the biggest circle coordinates and radius
    x_c = circles_s[0][0][0]
    y_c = circles_s[0][0][1]
    r_c = circles_s[0][0][2]
    
    # Circle center
    pos_circle = (x_c, y_c)
    
    # Angle difference between the direction that the CubeSat
    # is pointing and the Sun center
    sun_dif_angle = x_c*cam_angle/img_shape[1]
    sun_dif_angle = sun_dif_angle - cam_angle/2
else:
    # No circle was found
    pos_circle = (-1,-1)
    sun_dif_angle = -360

# Saves the data into a file
output_file.write(str(pos_line[0]).zfill(8))
output_file.write("\n")
output_file.write(str(pos_line[1]).zfill(8))
output_file.write("\n")
output_file.write(str(pos_circle[0]).zfill(8))
output_file.write("\n")
output_file.write(str(pos_circle[1]).zfill(8))
output_file.write("\n")
output_file.write(str(round(sun_dif_angle,4)).zfill(8))
output_file.write("\n")
output_file.close()
