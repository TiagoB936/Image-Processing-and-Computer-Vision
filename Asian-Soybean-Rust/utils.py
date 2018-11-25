# import the necessary packages
#
# The following functions is from authorship of Adrian Rosebrock
# from pyimagesearch blog:
#		centroid_histogram
#		plot_colors
#
# The following functionns is from my authorship:
#		infest_percent

import numpy as np
import cv2

def centroid_histogram(clt):
	# grab the number of different clusters and create a histogram
	# based on the number of pixels assigned to each cluster
	numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
	(hist, _) = np.histogram(clt.labels_, bins = numLabels)

	# normalize the histogram, such that it sums to one
	hist = hist.astype("float")
	hist /= hist.sum()

	# return the histogram
	return hist

def plot_colors(hist, centroids):
	# initialize the bar chart representing the relative frequency
	# of each of the colors
	bar = np.zeros((50, 300, 3), dtype = "uint8")
	startX = 0

	# loop over the percentage of each cluster and the color of
	# each cluster
	for (percent, color) in zip(hist, centroids):
          # plot the relative percentage of each cluster
          endX = startX + (percent * 300)
          cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
                        color.astype("uint8").tolist(), -1)
          startX = endX

	# return the bar chart
	return bar

def infest_percent(hist, centroids, thresh_health, thresh_warning):
  gray_x_percent = {}
  hist_cntr = 0  
  
  	#Convert all colors to grayscale  
  for color in centroids:
      color_uint8 = color.astype("uint8")
      B = color_uint8[0]
      G = color_uint8[1]
      R = color_uint8[2]
      gray_value = (0.21*R + 0.72*G + 0.07*B).astype("uint8")
      #add to the dictionary of percentage x color
      gray_x_percent[gray_value] = hist[hist_cntr]
      hist_cntr = hist_cntr + 1
  
  #general overview is the final diagnosis of the leaf
  general_overview = 0  

  # For each element resulted from K Means, compares de grayscale color value
  # to a set of thresholds choosen by the user, indicating healthy, warning
  # or dangerous conditions for an infected plant.
  # This done, the program generates a final diagnosis in gereal_overview, that
  # consists of a weighted average of the conditions previously explained.
  for elem in gray_x_percent:
    if elem <= thresh_health:
      print("The leaf is " + str(gray_x_percent[elem]*100) + "% in healthy conditions")
      general_overview = general_overview + gray_x_percent[elem]*0.2
    if elem > thresh_health and elem <= thresh_warning:
      print("The leaf is " + str(gray_x_percent[elem]*100) + "% in warning conditions")
      general_overview = general_overview + gray_x_percent[elem]*0.3
    if elem > thresh_warning:
      print("The leaf is " + str(gray_x_percent[elem]*100) + "% in dangerous conditions")
      general_overview = general_overview + gray_x_percent[elem]*0.5
    
  print("The leaf is " + str(general_overview*100) + "% infected")
  
  return gray_x_percent